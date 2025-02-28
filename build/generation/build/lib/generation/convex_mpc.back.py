# convex_mpc.py

import threading
import time
from typing import Optional, List, Dict
import yaml
import numpy as np
# import osqp
import scipy.sparse as sparse
# import rclpy
from rclpy.node import Node
from core.gait.mode_schedule import ModeSchedule
from core.trajectory.cubic_spline_trajectory import CubicSplineTrajectory, CubicSplineInterpolation,BoundaryType,SplineType
from pinocchio import SE3
from core.trajectory.reference_buffer import ReferenceBuffer
from .pinocchio_interface import PinocchioInterface 
from core.gait.motion_phase_definition import mode_number_to_stance_leg
import pinocchio as pin
from hpipm_python import *
from hpipm_python.common import *
# import ctypes as ct  # 通常的导入方式
# from scipy.linalg import block_diag
# from pydrake.all import MathematicalProgram, Solve
# from qpsolvers import solve_qp

vector3_t = np.ndarray 
scalar_t = float

class ConvexMPC:
    """
    ConvexMPC 类用于执行基于凸优化的模型预测控制（Model Predictive Control, MPC）。
    """

    def __init__(self, nodeHandle: Node,
                 pinocchioInterface_ptr: PinocchioInterface,
                 referenceBuffer: ReferenceBuffer):
        """
        初始化ConvexMPC实例。

        Args:
            nodeHandle (Node): ROS 2节点句柄。
            pinocchioInterface_ptr (PinocchioInterface): Pinocchio接口实例。
            referenceBuffer (ReferenceBuffer): 参考缓冲区实例。
        """
        self.nodeHandle_ = nodeHandle
        self.pinocchioInterface_ptr_ = pinocchioInterface_ptr
        self.referenceBuffer_ = referenceBuffer

        # 读取配置文件路径
        config_file = self.nodeHandle_.get_parameter("/config_file").value
        with open(config_file, 'r') as file:
            config_ = yaml.safe_load(file)

        # 加载模型相关参数
        self.foot_names: List[str] = config_["model"]["foot_names"]
        self.base_name: str = config_["model"]["base_name"]
        self.dt_ = 0.05
        self.freq_ = config_["generation"]["frequency"]
        self.h_des: scalar_t = 0.58  # 默认高度目标

        # 物理参数
        self.grav_: scalar_t = 9.81
        self.mu_: scalar_t = 0.5
        self.total_mass_: scalar_t = self.pinocchioInterface_ptr_.total_mass()
        self.Ig_ = np.zeros((3, 3))  # 需要根据实际情况初始化

        # 权重矩阵初始化
        self.weight_ = np.zeros((12, 12))
        np.fill_diagonal(self.weight_, [10, 10, 40, 0.2, 0.2, 0.1, 4, 4, 4, 0.1, 0.1, 0.1])

        # 初始化优化器设置
        self.solver_settings = {
            "warm_start": False,
            "eps_abs": 1e-4,
            "eps_rel": 1e-4,
            "max_iter": 30,
        }

        # 初始化速度和偏航角命令
        self.vel_cmd = np.zeros(3)
        self.yawd_ = 0.0

        # 起始状态
        self.rpy_start = np.zeros(3)
        self.pos_start = np.zeros(3)
        self.first_run = True
        self.t0 = self.nodeHandle_.get_clock().now().nanoseconds*1e-9
        self.x_des=[]

        self.nodeHandle_.get_logger().info("ConvexMPC: Construction done")

    def __del__(self):
        """
        析构函数。
        """
        pass

    def setVelCmd(self, vd: vector3_t, yawd: scalar_t):
        """
        设置速度命令和偏航角速度。

        Args:
            vd (vector3_t): 速度命令。
            yawd (scalar_t): 偏航角速度。
        """
        self.vel_cmd = vd
        # print("vd",vd)
        self.yawd_ = yawd

    def setHeightCmd(self, h: scalar_t):
        """
        设置高度命令。

        Args:
            h (scalar_t): 目标高度。
        """
        self.h_des = h

    def generateTrajRef(self):
        """
        生成轨迹参考。
        """
        t_now = self.nodeHandle_.get_clock().now().nanoseconds*1e-9
        base_pose_m: SE3 = self.pinocchioInterface_ptr_.getFramePose(self.base_name)

        if self.first_run:
            self.first_run = False
            self.pos_start = base_pose_m.translation.copy()
            self.pos_start[2] = self.h_des
            rpy_start_rot = self.toEulerAngles(base_pose_m.rotation)
            self.rpy_start = np.array([0.0, 0.0, rpy_start_rot[2]])
        else:
            rpy_c = self.toEulerAngles(base_pose_m.rotation)
            if np.linalg.norm(self.computeEulerAngleErr(rpy_c, self.rpy_start)) < 0.3:
                self.rpy_start += self.dt_ * np.array([0.0, 0.0, self.yawd_])
            self.rpy_start[:2] = 0.0

            vel_des = base_pose_m.rotation @ self.vel_cmd
            self.pos_start[:2] += self.dt_ * vel_des[:2]
            self.pos_start[2] = self.h_des

        time_array = []
        rpy_t = []
        pos_t = []
        horizon_time = self.referenceBuffer_.getModeSchedule().duration()
        N = int(horizon_time / 0.05)

        for k in range(N):
            time_array.append(t_now + 0.05 * k)
            rpy_k = self.rpy_start.copy()
            rpy_k[2] += 0.05 * k * self.yawd_
            rpy_t.append(rpy_k)

            # print("rpy_k",rpy_k)
            # print("self.toRotationMatrix(rpy_k)",self.toRotationMatrix(rpy_k))
            # print("self.vel_cmd",self.vel_cmd)

            vel_des = self.toRotationMatrix(rpy_k) @ self.vel_cmd
            pos_k = self.pos_start + 0.05 * k * vel_des
            pos_k[2] = self.h_des
            pos_t.append(pos_k)

        # 拟合位置轨迹
        cubicspline_pos = CubicSplineTrajectory(3, SplineType.CSPLINE)
        cubicspline_pos.set_boundary(
            BoundaryType.FIRST_DERIV,
            base_pose_m.rotation @ self.vel_cmd,
            BoundaryType.SECOND_DERIV,
            np.zeros(3)
        )
        cubicspline_pos.fit(time_array, pos_t)
        self.referenceBuffer_.setIntegratedBasePosTraj(cubicspline_pos)

        # 拟合姿态轨迹
        cubicspline_rpy = CubicSplineTrajectory(3, SplineType.CSPLINE)
        cubicspline_rpy.set_boundary(
            BoundaryType.FIRST_DERIV,
            np.array([0.0, 0.0, self.yawd_]),
            BoundaryType.SECOND_DERIV,
            np.zeros(3)
        )
        cubicspline_rpy.fit(time_array, rpy_t)
        self.referenceBuffer_.setIntegratedBaseRpyTraj(cubicspline_rpy)

    def getDynamics(self, time_cur: scalar_t, k: int,
                   mode_schedule: ModeSchedule):
        """
        获取动力学模型。

        Args:
            time_cur (scalar_t): 当前时间。
            k (int): 时间步索引。
            mode_schedule (ModeSchedule): 当前步态模式。
        """
        time_k = time_cur + k * self.dt_
        pos_traj = self.referenceBuffer_.getIntegratedBasePosTraj()
        rpy_traj = self.referenceBuffer_.getIntegratedBaseRpyTraj()
        foot_traj = self.referenceBuffer_.getFootPosTraj()

        phase = (k * self.dt_) / mode_schedule.duration()
        contact_flag = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(phase)) 
        nf = len(self.foot_names)
        assert nf == len(contact_flag), "Foot names and contact flags size mismatch."

        base_pose = self.pinocchioInterface_ptr_.getFramePose(self.base_name)
        rpy_des = rpy_traj.evaluate(time_k)

        Rt = self.toRotationMatrix(rpy_des)
        Ig_t = Rt @ self.Ig_ @ Rt.T

        # 构建A和B矩阵
        A = np.eye(12)
        A[0:3, 3:6] = np.eye(3) * self.dt_
        A[6:9, 9:12] = self.dt_ * self.getJacobiFromOmegaToRPY(rpy_des)

        B = np.zeros((12, nf * 3))
        xc = phase * pos_traj.evaluate(time_k) + (1.0 - phase) * base_pose.translation

        for i, foot_name in enumerate(self.foot_names):
            if contact_flag[i]:
                pf_i = foot_traj[foot_name].evaluate(time_k)
                B[3:6, 3 * i:3 * i + 3] = (self.dt_ / self.total_mass_) * np.eye(3)
                skew_matrix = self.skew_matrix(self.dt_ * (pf_i - xc))
                B[9:12, 3 * i:3 * i + 3] = np.linalg.inv(Ig_t) @ skew_matrix

        b = np.zeros(12)
        b[5] += -self.dt_ * self.grav_

        # 构建优化问题的A, B, b
        ocp_k = {
            "A": A,
            "B": B,
            "b": b,
            "C": np.zeros((5 * nf, 12)),
            "D": np.zeros((5 * nf, 3 * nf)),
            "lg": np.zeros(5 * nf),
            "ug": np.zeros(5 * nf),
            "lg_mask": np.ones(5 * nf),
            "ug_mask": np.ones(5 * nf),
            "Q": self.weight_,
            "R": 1e-5 * np.eye(3 * nf),
            "S": np.zeros((3 * nf, 12)),
            "q": -self.weight_ @ np.zeros(12),  # x_des 需要在getCosts中设置
            "r": np.zeros(3 * nf),
            "H":B.transpose() @ self.weight_ @ B + 1e-5 * np.eye(3 * nf),
            "g":B.transpose() @ self.weight_ @ (A @  + b)
        }

        if k >= len(self.ocp_):
            self.ocp_ += [None] * (k - len(self.ocp_) + 1)

        self.ocp_[k]=ocp_k

    def getInequalityConstraints(self, k: int, N: int,
                                 mode_schedule: ModeSchedule):
        """
        获取不等式约束。

        Args:
            k (int): 时间步索引。
            N (int): 预测步长。
            mode_schedule (ModeSchedule): 当前步态模式。
        """
        # 此方法已在getDynamics中实现
        nf = len(self.foot_names)
        phase= (k * self.dt_) / mode_schedule.duration()
        contact_flag = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(phase))

        if k<N:
            mu = 1/ self.mu_  #!!!!
            Ci = np.array([[mu, 0, 1.],
                           [-mu, 0, 1.],
                           [0, mu, 1.],
                           [0, -mu, 1.],
                           [0, 0, 1.]])
            
            self.ocp_[k]["C"] = np.zeros((5 * nf, 12))
            self.ocp_[k]["D"] = np.zeros((5 * nf, 3 * nf))
            self.ocp_[k]["lg"] = np.zeros(5 * nf)
            self.ocp_[k]["ug"] = np.zeros(5 * nf)
            self.ocp_[k]["lg_mask"] = np.ones(5 * nf)
            self.ocp_[k]["ug_mask"] = np.ones(5 * nf)
            # qp_C = np.kron(np.identity(4 * self.horizon, dtype=np.float32), constraint_coef_matrix)

            for i in range(nf):
                self.ocp_[k]["D"][5 * i:5 * i + 5, 3 * i:3 * i + 3] = Ci    #qp_C
                self.ocp_[k]["ug"][5 * i + 4] = 400 if contact_flag[i] else 0.0
                self.ocp_[k]["ug_mask"][5 * i:5 * i + 4] = 0.0  # 前四个约束不受上界影响, if 1 then the constraint is active, if 0 then the constraint is not active
                self.ocp_[k]["ug"][5 * i:5 * i + 4] = np.inf

    def getCosts(self, time_cur: scalar_t, k: int, N: int,
                mode_schedule: ModeSchedule):
        """
        获取代价函数。

        Args:
            time_cur (scalar_t): 当前时间。
            k (int): 时间步索引。
            N (int): 预测步长。
            mode_schedule (ModeSchedule): 当前步态模式。
        """
        time_k = time_cur + (k + 1) * self.dt_
        pos_traj = self.referenceBuffer_.getIntegratedBasePosTraj()
        rpy_traj = self.referenceBuffer_.getIntegratedBaseRpyTraj()

        rpy_des = rpy_traj.evaluate(time_k) - rpy_traj.evaluate(time_cur) + self.rpy_start
        omega_des = self.getJacobiFromRPYToOmega(rpy_des) @ rpy_traj.derivative(time_k, 1)
        v_des = pos_traj.derivative(time_k, 1)

        x_des = np.hstack([pos_traj.evaluate(time_k), v_des, rpy_des, omega_des])

        self.x_des=np.concatenate([self.x_des,x_des])

        # 设置Q和q
        # print("len(self.ocp_)",len(self.ocp_))
        # print("k",k)
        self.ocp_[k]["Q"] = self.weight_
        self.ocp_[k]["S"] = np.zeros((3 * len(self.foot_names), 12))
        self.ocp_[k]["q"] = -self.weight_ @ x_des
        self.ocp_[k]["r"] = np.zeros(3 * len(self.foot_names))

        if k < N:
            self.ocp_[k]["R"] = 1e-5 * np.eye(3 * len(self.foot_names))
            phase = (k * self.dt_) / mode_schedule.duration()
            contact_flag = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(phase))
            nc = max(1, contact_flag.count(True))
            force_des_i = (self.total_mass_ / nc) * (np.array([0, 0, self.grav_]) + pos_traj.derivative(time_k, 2))
            force_des = np.zeros(3 * len(self.foot_names))
            for i, flag in enumerate(contact_flag):
                if flag:
                    force_des[3 * i:3 * i + 3] = force_des_i
            self.ocp_[k]["r"] = -self.ocp_[k]["R"] @ force_des

    def optimize(self):
        """
        执行优化过程。
        """
        # 预计算变量
        t_now = self.nodeHandle_.get_clock().now().nanoseconds*1e-9
        mode_schedule = self.referenceBuffer_.getModeSchedule()
        pos_traj = self.referenceBuffer_.getIntegratedBasePosTraj()
        foot_pos_traj = self.referenceBuffer_.getFootPosTraj()
        nf=len(self.foot_names)

        # 检查是否有足部轨迹
        if not foot_pos_traj or pos_traj is None or mode_schedule is None:
            return

        # 生成轨迹参考
        rpy_traj = self.referenceBuffer_.getIntegratedBaseRpyTraj()
        N = int(mode_schedule.duration() / self.dt_)
        
        pinocchio_interface = self.pinocchioInterface_ptr_  # 减少属性访问

        N=10

        # # 预分配数据结构
        self.ocp_ = [None] * N
        # self.solution_ = [None] * (N + 1)

        # self.ocp_ = [] 
        self.solution_ = []

        Ig_0 = pinocchio_interface.getData().Ig.inertia
        base_pose = pinocchio_interface.getFramePose(self.base_name)
        rotation_t = base_pose.rotation.transpose()
        self.Ig_ = rotation_t @ Ig_0 @ base_pose.rotation

        base_twist = self.pinocchioInterface_ptr_.getFrame6dVel_localWorldAligned(self.base_name)
        current_rpy_traj = rpy_traj.evaluate(t_now)
        rpy_m = self.toEulerAngles(base_pose.rotation)
        self.rpy_start = rpy_m - self.computeEulerAngleErr(rpy_m, current_rpy_traj)


        # 添加数据验证步骤
        for k in range(N):
            # 验证每个数据源的合法性
            self.getDynamics(t_now, k, mode_schedule) 
            self.getInequalityConstraints(k, N, mode_schedule) 
            self.getCosts(t_now, k, N, mode_schedule)

        
        if (len(self.solution_) == N+1 ) :
            self.solver_settings["warm_start"] = 1
        else:
            self.solver_settings["warm_start"] = 0
            # self.solution_.reshape(N+1,)

        # dims
        nx = len(self.ocp_[0]["A"][0])
        nu = len(self.ocp_[0]["B"][0])

        Sx = np.zeros((nx * N, nx), dtype=np.float32)
        Su = np.zeros((nx * N, nu * N), dtype=np.float32)

        power_of_A = [np.identity(nx, dtype=np.float32)]
        for k in range(N):
            power_of_A.append(power_of_A[k] @ self.ocp_[k]["A"])

        for k in range(N):
                Sx[nx*k:nx*(k+1), 0:nx] = power_of_A[k+1]

                for j in range(N):
                    if k >= j:
                        Su[nx*k : nx*(k+1), nu*j : nu*(j+1)] = power_of_A[k-j] @ self.ocp_[j]["B"]
        self.Qbar = np.kron(np.identity(N), self.weight_)
        self.Rbar = np.kron(np.identity(N), self.ocp_[0]["R"])
        b_block = np.concatenate([self.ocp_[k]["b"] for k in range(N)])


        xt=np.concatenate([base_pose.translation,base_twist.linear,rpy_m , base_twist.angular])
        qp_H = 2 * (Su.T @ self.Qbar @ Su + self.Rbar)
        # print("Sx.shape",Sx.shape)
        # print("xt.shape",np.array(xt).shape)
        # print("b_block.shape",b_block.shape)
        # print("self.x_des.shape",np.array(self.x_des).shape)
        qp_g = 2 * Su.T @ self.Qbar @ (Sx @ xt + b_block-self.x_des)
        qp_C = np.kron(np.identity(N, dtype=np.float32), self.ocp_[0]["D"])
        C_lb = np.zeros(nf * 5 * N, dtype=np.float32)
        C_ub = np.concatenate([self.ocp_[k]["ug"] for k in range(N)])

        # print("qp_C.shape",qp_C.shape)
        # print("C_lb.shape",C_lb.shape)
        # print("C_ub.shape",np.array(C_ub).shape)
        

        qp_problem = MathematicalProgram()
        contact_forces = qp_problem.NewContinuousVariables(nu*N, 'contact_forces')

        qp_problem.AddQuadraticCost(qp_H, qp_g, contact_forces)
        qp_problem.AddLinearConstraint(qp_C, C_lb, C_ub, contact_forces)

        result = Solve(qp_problem)
        # print("dir(result)",dir(result))
        # print("result.GetSolution(contact_forces).shape",result.GetSolution(contact_forces).shape)
        # print("result.get_x_val.shape",result.get_x_val().shape)
        x=xt

        for k in range(N):
                x = self.ocp_[k]["A"] @ x + self.ocp_[k]["B"] @ result.GetSolution(contact_forces)[nu*k:nu*(k+1)]
                u = result.GetSolution(contact_forces)[nu*0:nu*(0+1)]
                self.solution_.append({'x': x, 'u': u}) 
        self.x_des=[]

        # 拟合轨迹
        self.fitTraj(t_now, N)


        # if k<N:
        #     mu = 1/ self.mu_  #!!!!
        #     Ci = np.array([[mu, 0, 1.],
        #                    [-mu, 0, 1.],
        #                    [0, mu, 1.],
        #                    [0, -mu, 1.],
        #                    [0, 0, 1.]])
            
        #     self.ocp_[k]["C"] = np.zeros((5 * nf, 12))
        #     self.ocp_[k]["D"] = np.zeros((5 * nf, 3 * nf))
        #     self.ocp_[k]["lg"] = np.zeros(5 * nf)
        #     self.ocp_[k]["ug"] = np.zeros(5 * nf)
        #     self.ocp_[k]["lg_mask"] = np.ones(5 * nf)
        #     self.ocp_[k]["ug_mask"] = np.ones(5 * nf)
        #     # qp_C = np.kron(np.identity(4 * self.horizon, dtype=np.float32), constraint_coef_matrix)

        #     for i in range(nf):
        #         self.ocp_[k]["D"][5 * i:5 * i + 5, 3 * i:3 * i + 3] = Ci    #qp_C
        #         self.ocp_[k]["ug"][5 * i + 4] = 400 if contact_flag[i] else 0.0
        #         self.ocp_[k]["ug_mask"][5 * i:5 * i + 4] = 0.0  # 前四个约束不受上界影响, if 1 then the constraint is active, if 0 then the constraint is not active
        #         self.ocp_[k]["ug"][5 * i:5 * i + 4] = np.inf


        # A_block = np.concatenate([self.ocp_[k]["A"] for k in range(N)])
        # B_block = block_diag(*[self.ocp_[k]["B"] for k in range(N)])
        # Q_block = block_diag(*[self.ocp_[k]["Q"] for k in range(N)])
        # R_block = block_diag(*[self.ocp_[k]["R"] for k in range(N)])
        # lg_block = np.concatenate([self.ocp_[k]["lg"] for k in range(N)])
        # ug_block = np.concatenate([self.ocp_[k]["ug"] for k in range(N)])
        # ug_mask_block = np.concatenate([self.ocp_[k]["ug_mask"] for k in range(N)])

        # dim = hpipm_ocp_qp_dim(N)    # too slow

        # # dim.batch_set('nx', [nx]*N)  # 假设有批量设置方法
        # # dim.batch_set('nu', [nu]*(N-1))
        # dim.set('nx', nx, 0, N) # number of states
        # dim.set('nu', nu, 0, N-1) # number of inputs



        # # define flags
        # codegen_data = 0; # export qp data in the file dense_qp_data.c for use from C examples
        # warm_start = 0; # set to 1 to warm-start the primal variable


        # # dim


        
        # # print to shell
        # # dim.print_C_struct()
        # # codegen
        # if codegen_data:
        #     dim.codegen('dense_qp_data.c', 'w')

        # qp = hpipm_ocp_qp(dim)

        # # 预先生成所有参数的列表结构
        # # params = [
        # #     ('A', [ocp["A"] for ocp in self.ocp_]),
        # #     ('B', [ocp["B"] for ocp in self.ocp_]),
        # #     ('b', [ocp["b"] for ocp in self.ocp_]),
        # #     ('Q', [ocp["Q"] for ocp in self.ocp_]),
        # #     ('S', [ocp["S"] for ocp in self.ocp_]),
        # #     ('R', [ocp["R"] for ocp in self.ocp_]),
        # #     ('q', [ocp["q"] for ocp in self.ocp_]),
        # #     ('r', [ocp["r"] for ocp in self.ocp_]),
        # #     ('C', [ocp["C"] for ocp in self.ocp_]),
        # #     ('D', [ocp["D"] for ocp in self.ocp_]),
        # #     ('lg', [ocp["lg"] for ocp in self.ocp_]),
        # #     ('ug', [ocp["ug"] for ocp in self.ocp_]),
        # #     ('lg_mask', [ocp["lg_mask"] for ocp in self.ocp_]),
        # #     ('ug_mask', [ocp["ug_mask"] for ocp in self.ocp_])
        # # ]

        # # # 优化后的循环设置
        # # for param_name, param_list in params:
        # #     for k in range(N):
        # #         # 提前进行边界检查
        # #         if k >= len(param_list):
        # #             break
        # #         param_value = param_list[k]
                
        # #         # 跳过空值（假设某些参数可能为None）
        # #         if param_value is not None:  
        # #             # 使用低级接口避免类型检查开销
        # #             qp.set(param_name, param_value, k)
                    
        # #             # 对于矩阵参数使用内存视图优化
        # #             if isinstance(param_value, np.ndarray):
        # #                 qp.set(param_name, param_value.ctypes.data_as(ct.POINTER(ct.c_double)),k)
        # for k in range(N):
        #     qp.set('A', self.ocp_[k]["S"], k)
        #     qp.set('B', self.ocp_[k]["B"], k)
        #     qp.set('b', self.ocp_[k]["b"], k)
        #     qp.set('Q', self.ocp_[k]["Q"], k)
        #     qp.set('S', self.ocp_[k]["S"], k)
        #     qp.set('R', self.ocp_[k]["R"], k)
        #     qp.set('q', self.ocp_[k]["q"], k)
        #     qp.set('r', self.ocp_[k]["r"], k)
        #     qp.set('C', self.ocp_[k]["C"], k)
        #     qp.set('D', self.ocp_[k]["D"], k)
        #     qp.set('lg', self.ocp_[k]["lg"], k)
        #     qp.set('ug', self.ocp_[k]["ug"], k)
        #     qp.set('lg_mask', self.ocp_[k]["lg_mask"], k)
        #     qp.set('ug_mask', self.ocp_[k]["ug_mask"], k)
        
        # # print to shell
        # # qp.print_C_struct()
        # # codegen
        # if codegen_data:
        #     qp.codegen('ocp_qp_data.c', 'a')

        # # qp sol
        # qp_sol = hpipm_ocp_qp_sol(dim)

        # # set up solver arg
        # mode = 'speed_abs'
        # # mode = 'speed'
        # # mode = 'balance'
        # #mode = 'robust'
        # # create and set default arg based on mode
        # arg = hpipm_ocp_qp_solver_arg(dim, mode)

        # # create and set default arg based on mode
        # arg.set('iter_max', 30)
        # arg.set('alpha_min', 1e-8)
        # arg.set('mu0', 1e2)
        # arg.set('tol_stat', 1e-5)
        # arg.set('tol_eq', 1e-5)
        # arg.set('tol_ineq', 1e-4)
        # arg.set('tol_comp', 1e-4)
        # arg.set('reg_prim', 1e-12)
        # arg.set('pred_corr', 1)
        # arg.set('split_step', 1)
        # arg.set('warm_start', warm_start)       


        # # codegen
        # if codegen_data:
        #     arg.codegen('ocp_qp_data.c', 'a')

        # # solve qp
        # start_time = time.time()

        # solver = hpipm_ocp_qp_solver(dim, arg)
        # solver.solve(qp, qp_sol := hpipm_ocp_qp_sol(dim))
        # solver.solve(qp, qp_sol)

        # end_time = time.time()
        # print('solve time {:e}'.format(end_time-start_time))

        # for k in range(N):
        #     x = qp_sol.get('x', k)
        #     u = qp_sol.get('u', k)
        #     self.solution_.append({'x': x, 'u': u})

        # # 拟合轨迹
        # self.fitTraj(t_now, N)


    def fitTraj(self, time_cur: scalar_t, N: int):
        """
        拟合优化后的轨迹。

        Args:
            time_cur (scalar_t): 当前时间。
            N (int): 预测步长。
        """
        time_array = []
        base_pos_array = []
        base_vel_array = []
        base_rpy_array = []
        base_omega_array = []
        force_array = []

        for k in range(N):
            time_array.append(time_cur + k * self.dt_)
            base_pos_array.append(self.solution_[k]['x'][:3])
            base_vel_array.append(self.solution_[k]['x'][3:6])
            base_rpy_array.append(self.solution_[k]['x'][6:9])
            base_omega_array.append(self.solution_[k]['x'][9:12])
            force_array.append(self.solution_[k]['u'])

        # print("base_pos_array",base_pos_array)

        # 拟合位置轨迹
        base_pos_traj_ptr = CubicSplineTrajectory(
            3, SplineType.CSPLINE
        )
        base_pos_traj_ptr.set_boundary(
            BoundaryType.FIRST_DERIV,
            self.solution_[1]['x'][3:6],
            BoundaryType.FIRST_DERIV,
            self.solution_[-1]['x'][3:6]
        )
        base_pos_traj_ptr.fit(time_array, base_pos_array)
        self.referenceBuffer_.setOptimizedBasePosTraj(base_pos_traj_ptr)

        # 拟合速度轨迹
        base_vel_traj_ptr = CubicSplineTrajectory(
            3, SplineType.CSPLINE
        )
        base_vel_traj_ptr.set_boundary(
            BoundaryType.FIRST_DERIV,
            (self.solution_[1]['x'][3:6] - self.solution_[0]['x'][3:6]) / self.dt_,
            BoundaryType.FIRST_DERIV,
            (self.solution_[N - 1]['x'][3:6] - self.solution_[N - 2]['x'][3:6]) / self.dt_
        )
        base_vel_traj_ptr.fit(time_array, base_vel_array)
        self.referenceBuffer_.setOptimizedBaseVelTraj(base_vel_traj_ptr)

        # 拟合姿态轨迹
        base_rpy_traj_ptr = CubicSplineTrajectory(
            3, SplineType.CSPLINE_HERMITE
        )
        base_rpy_traj_ptr.set_boundary(
            BoundaryType.FIRST_DERIV,
            (self.solution_[1]['x'][6:9] - self.solution_[0]['x'][6:9]) / self.dt_,
            BoundaryType.FIRST_DERIV,
            (self.solution_[N - 1]['x'][6:9] - self.solution_[N - 2]['x'][6:9]) / self.dt_
        )
        base_rpy_traj_ptr.fit(time_array, base_rpy_array)
        self.referenceBuffer_.setOptimizedBaseRpyTraj(base_rpy_traj_ptr)

        # 拟合角速度轨迹
        base_omega_traj_ptr = CubicSplineTrajectory(
            3, SplineType.CSPLINE
        )
        base_omega_traj_ptr.set_boundary(
            BoundaryType.FIRST_DERIV,
            (self.solution_[1]['x'][9:12] - self.solution_[0]['x'][9:12]) / self.dt_,
            BoundaryType.FIRST_DERIV,
            (self.solution_[N - 1]['x'][9:12] - self.solution_[N - 2]['x'][9:12]) / self.dt_
        )
        base_omega_traj_ptr.fit(time_array, base_omega_array)
        self.referenceBuffer_.setOptimizedBaseOmegaTraj(base_omega_traj_ptr)

        # 拟合力轨迹
        force_traj_ptr = CubicSplineTrajectory(
            len(self.foot_names) * 3, SplineType.CSPLINE
        )
        force_traj_ptr.set_boundary(
            BoundaryType.FIRST_DERIV,
            np.zeros(len(self.foot_names) * 3),
            BoundaryType.FIRST_DERIV,
            np.zeros(len(self.foot_names) * 3)
        )
        force_traj_ptr.fit(time_array, force_array)
        self.referenceBuffer_.setOptimizedForceTraj(force_traj_ptr)

    def toEulerAngles(self, rotation_matrix: np.ndarray) -> vector3_t:
        """
        将旋转矩阵转换为欧拉角（ZYX顺序）。

        Args:
            rotation_matrix (np.ndarray): 旋转矩阵。

        Returns:
            vector3_t: 欧拉角。
        """
        # sy = np.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)
        # singular = sy < 1e-6

        # if not singular:
        #     x = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
        #     y = np.arctan2(-rotation_matrix[2, 0], sy)
        #     z = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
        # else:
        #     x = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
        #     y = np.arctan2(-rotation_matrix[2, 0], sy)
        #     z = 0

        return pin.rpy.matrixToRpy(rotation_matrix)

    def toRotationMatrix(self, rpy: vector3_t) -> np.ndarray:
        """
        将欧拉角（ZYX顺序）转换为旋转矩阵。

        Args:
            rpy (vector3_t): 欧拉角。

        Returns:
            np.ndarray: 旋转矩阵。
        """
        roll, pitch, yaw = rpy
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(roll), -np.sin(roll)],
            [0, np.sin(roll), np.cos(roll)]
        ])
        Ry = np.array([
            [np.cos(pitch), 0, np.sin(pitch)],
            [0, 1, 0],
            [-np.sin(pitch), 0, np.cos(pitch)]
        ])
        Rz = np.array([
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1]
        ])
        return Rz @ Ry @ Rx


    def computeEulerAngleErr(self,rpy_m: np.ndarray, rpy_d: np.ndarray) -> np.ndarray:
        """
        计算欧拉角误差并归一化，使其保持在 -pi 到 pi 之间。
        :param rpy_m: 当前的欧拉角（Roll, Pitch, Yaw）
        :param rpy_d: 目标欧拉角（Roll, Pitch, Yaw）
        :return: 欧拉角误差（归一化后的）
        """
        # 计算欧拉角误差
        rpy_err = rpy_m - rpy_d
        
        # 将误差归一化到 -pi 到 pi 之间
        while np.linalg.norm(rpy_err) > 1.5 * np.pi:
            for i in range(3):
                if abs(rpy_err[i]) > np.pi:
                    rpy_err[i] += (rpy_err[i] > 0) * -2.0 * np.pi + (rpy_err[i] < 0) * 2.0 * np.pi

        return rpy_err


    def skew_matrix(self, vec: vector3_t) -> np.ndarray:
        """
        生成向量的斜对称矩阵。

        Args:
            vec (vector3_t): 3D向量。

        Returns:
            np.ndarray: 斜对称矩阵。
        """
        return np.array([
            [0, -vec[2], vec[1]],
            [vec[2], 0, -vec[0]],
            [-vec[1], vec[0], 0]
        ])

    def getJacobiFromOmegaToRPY(self, rpy: vector3_t) -> np.ndarray:
        """
        根据欧拉角计算从角速度到欧拉角速度的雅可比矩阵。

        Args:
            rpy (vector3_t): 欧拉角。

        Returns:
            np.ndarray: 雅可比矩阵。
        """
        jacobian_inv = pin.rpy.computeRpyJacobianInverse(rpy, pin.LOCAL_WORLD_ALIGNED)

        return jacobian_inv

    def getJacobiFromRPYToOmega(self,rpy: vector3_t) -> np.ndarray:
        """
        计算从 RPY（Roll, Pitch, Yaw）到角速度（ω）的雅可比矩阵
        :param rpy: 一个长度为 3 的 numpy 数组，表示 Roll, Pitch, Yaw
        :return: 一个 3x3 的 numpy 数组，表示从 RPY 到角速度的雅可比矩阵
        """
        # 使用 Pinocchio 的 computeRpyJacobian 方法计算雅可比矩阵
        jacobian = pin.rpy.computeRpyJacobian(rpy, pin.LOCAL_WORLD_ALIGNED)
        
        return jacobian
