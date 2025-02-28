# whole_body_controller.py

import numpy as np
import yaml
# import rclpy
from rclpy.node import Node
# from typing import List, Dict
from .matrix_db import MatrixDB
from core.trajectory.reference_buffer import ReferenceBuffer
from core.misc.buffer import Buffer
# from scipy.linalg import block_diag
# import cvxopt
import pinocchio as pin
from generation.pinocchio_interface import PinocchioInterface
import proxsuite
# import scipy.sparse as spa
from core.gait.motion_phase_definition import mode_number_to_stance_leg



class ActuatorCommands:
    def __init__(self):
        self.Kp = np.array([])
        self.Kd = np.array([])
        self.pos = np.array([])
        self.vel = np.array([])
        self.torque = np.array([])

    def set_zero(self, n):
        self.Kp = np.zeros(n)
        self.Kd = np.zeros(n)
        self.pos = np.zeros(n)
        self.vel = np.zeros(n)
        self.torque = np.zeros(n)

    def __repr__(self):
        return (f"ActuatorCommands(Kp={self.Kp},\n"
                f"Kd={self.Kd},\n"
                f"pos={self.pos},\n"
                f"vel={self.vel},\n"
                f"torque={self.torque})")

class WholeBodyController:
    def __init__(self, node_handle: Node):
        self.node_handle = node_handle

        # Load configuration
        config_file = self.node_handle.get_parameter("/config_file").value
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        model_package = config["model"]["package"]
        urdf_relative_path = config["model"]["urdf"]
        urdf_path = self.get_urdf_path(model_package, urdf_relative_path)
        self.node_handle.get_logger().info(f"Model file: {urdf_path}")

        self.pinocchioInterface_ptr = PinocchioInterface(urdf_path)
        # self.pinocchio_model = self.pinocchioInterface_ptr.model_
        # self.pinocchio_data = self.pinocchioInterface_ptr.data_


        self.foot_names = config["model"]["foot_names"]
        for name in self.foot_names:
            self.node_handle.get_logger().info(f"Foot name: {name}")

        self.base_name = config["model"]["base_name"]
        self.actuated_joints_name = config["model"]["actuated_joints_name"]

        self.num_decision_vars = self.pinocchioInterface_ptr.nv() + 3 * len(self.foot_names) + len(self.actuated_joints_name)
        self.load_tasks_setting(verbose=False)

        self.reference_buffer: ReferenceBuffer = None
        self.mode_buffer: Buffer = Buffer()

        self.jc = np.array([])  # Contact Jacobian
        self.contact_flag = []
        self.num_contacts = 0

        self.weighed_task = MatrixDB("weighedTask")
        self.constraints = MatrixDB("constraints")

        self.dt = 0.002
        self.joint_acc = np.array([])
        self.actuator_commands = ActuatorCommands()
        

    def get_urdf_path(self, package: str, urdf_relative_path: str) -> str:
        from ament_index_python.packages import get_package_share_directory
        return get_package_share_directory(package) + urdf_relative_path

    def load_tasks_setting(self, verbose: bool = True):
        # Load task weights and parameters
        self.weight_momentum = np.zeros((6, 6))
        self.weight_base = np.zeros((6, 6))
        np.fill_diagonal(self.weight_base, 100)

        self.weight_swing_leg = np.zeros((3, 3))
        np.fill_diagonal(self.weight_swing_leg, 200)

        self.weight_contact_force = 1e-2
        self.friction_coeff = 0.5

        self.swing_kp = np.zeros((3, 3))
        np.fill_diagonal(self.swing_kp, 350)

        self.swing_kd = np.zeros((3, 3))
        np.fill_diagonal(self.swing_kd, 37)

        self.base_kp = np.zeros((6, 6))
        # np.fill_diagonal(self.base_kp, [30, 30, 60, 80, 80, 80])  # Option 1
        # np.fill_diagonal(self.base_kp, [60, 60, 100, 120, 120, 120])  # Option 2
        np.fill_diagonal(self.base_kp, [200, 200, 200, 320, 320, 320])  # Option 3

        self.base_kd = np.zeros((6, 6))
        # np.fill_diagonal(self.base_kd, [3.0, 3.0, 3.0, 10.0, 10.0, 10.0])  # Option 1
        # np.fill_diagonal(self.base_kd, [16.0, 16.0, 20.0, 20.0, 20.0, 20.0])  # Option 2
        np.fill_diagonal(self.base_kd, [16.0, 16.0, 20.0, 40.0, 40.0, 40.0])  # Option 3

        self.momentum_kp = np.zeros((6, 6))
        self.momentum_kd = np.zeros((6, 6))

        if verbose:
            self.node_handle.get_logger().info(f"Momentum Weights:\n{self.weight_momentum}")
            self.node_handle.get_logger().info(f"Base Weights:\n{self.weight_base}")
            self.node_handle.get_logger().info(f"Swing Leg Weights:\n{self.weight_swing_leg}")
            self.node_handle.get_logger().info(f"Contact Force Weight: {self.weight_contact_force}")
            self.node_handle.get_logger().info(f"Friction Coefficient: {self.friction_coeff}")
            self.node_handle.get_logger().info(f"Swing Leg Kp:\n{self.swing_kp}")
            self.node_handle.get_logger().info(f"Swing Leg Kd:\n{self.swing_kd}")
            self.node_handle.get_logger().info(f"Base Kp:\n{self.base_kp}")
            self.node_handle.get_logger().info(f"Base Kd:\n{self.base_kd}")
            self.node_handle.get_logger().info(f"Momentum Kp:\n{self.momentum_kp}")
            self.node_handle.get_logger().info(f"Momentum Kd:\n{self.momentum_kd}")

    def update_reference_buffer(self, reference_buffer: ReferenceBuffer):
        self.reference_buffer = reference_buffer

    def update_state(self, qpos_ptr: np.ndarray, qvel_ptr: np.ndarray):
        self.pinocchioInterface_ptr.updateRobotState(qpos_ptr, qvel_ptr)

    def optimize(self) -> ActuatorCommands:
        self.actuator_commands.set_zero(len(self.actuated_joints_name))

        if (self.reference_buffer is None or
            self.reference_buffer.getModeSchedule() is None or
            self.reference_buffer.getOptimizedForceTraj() is None or
            not self.reference_buffer.getFootPosTraj()):
            return self.actuator_commands

        self.formulate()

        H = self.weighed_task.A.T @ self.weighed_task.A
        np.fill_diagonal(H, H.diagonal() + 1e-12 * np.ones(self.num_decision_vars))
        g = -self.weighed_task.A.T @ self.weighed_task.b

        n = H.shape[0]

        n_eq = self.constraints.A.shape[0]
        n_in = self.constraints.C.shape[0]

        qp = qp = proxsuite.proxqp.dense.QP(n, n_eq, n_in)

        qp.init(H, g, self.constraints.A, self.constraints.b, self.constraints.C, self.constraints.lb, self.constraints.ub)


        qp.solve()

        # Solve QP

        solution = qp.results


        optimal_u = np.array(solution.x).flatten()
        self.actuator_commands.torque = optimal_u[-len(self.actuated_joints_name):]
        self.joint_acc = optimal_u[:self.pinocchioInterface_ptr.nv()][-len(self.actuated_joints_name):]
        self.differential_inv_kin()
        # else:
        #     self.joint_acc = np.zeros(len(self.actuated_joints_name))
        #     self.node_handle.get_logger().error("WholeBodyController: QP Solver failed.")
        #     self.actuator_commands.set_zero(len(self.actuated_joints_name))
        #     self.actuator_commands.Kd.fill(1.0)

        return self.actuator_commands

    def formulate(self):
        self.mode_buffer.push(self.reference_buffer.getModeSchedule().get_mode_from_phase(0.0))
        self.contact_flag = mode_number_to_stance_leg(self.mode_buffer.get())
        self.num_contacts = int(np.sum(self.contact_flag))

        self.update_contact_jacobi()

        self.constraints = (
            self.formulate_floating_base_euler_newton_equ() +
            self.formulate_torque_limits_task() +
            self.formulate_friction_cone_task() +
            self.formulate_maintain_contact_task()
        )
        self.weighed_task = (
            self.formulate_base_task() +
            self.formulate_swing_leg_task() +
            self.formulate_contact_force_task()
        )

    def find_closest(self, x_val: float) -> int:
        idx = np.searchsorted(self.pinocchioInterface_ptr.getModel().names, x_val) - 1
        idx = max(idx, 0)
        return idx

    def formulate_floating_base_euler_newton_equ(self) -> MatrixDB:
        euler_newton_equ = MatrixDB("eulerNewtonEqu")
        data = self.pinocchioInterface_ptr.getData()
        nv = self.pinocchioInterface_ptr.nv()
        na = len(self.actuated_joints_name)

        if nv != na + 6:
            raise ValueError("nv != actuatedDofNum + 6")

        S = np.zeros((nv, na))
        S[:6, :] = 0
        S[-na:, :] = np.eye(na)

        # 拼接矩阵
        A_combined = np.hstack([data.M, -self.jc.T, -S])
        euler_newton_equ.A = A_combined
        euler_newton_equ.b = -data.nle

        return euler_newton_equ

    def formulate_torque_limits_task(self) -> MatrixDB:
        limit_tau = MatrixDB(name="limit_tau")
        na = len(self.actuated_joints_name)
        limit_tau.C = np.zeros((na, self.num_decision_vars))
        limit_tau.C[-na:, -na:] = np.eye(na)
        limit_tau.lb = -self.pinocchioInterface_ptr.getModel().effortLimit[-na:]
        limit_tau.ub = self.pinocchioInterface_ptr.getModel().effortLimit[-na:]
        return limit_tau

    def formulate_maintain_contact_task(self) -> MatrixDB:
        contact_task = MatrixDB(name="contact_task")
        nc = len(self.foot_names)
        nv = self.pinocchioInterface_ptr.nv()
        contact_task.A = np.zeros((3 * self.num_contacts, self.num_decision_vars))
        contact_task.b = np.zeros(3 * self.num_contacts)
        j = 0
        for i in range(nc):
            if self.contact_flag[i]:
                contact_task.A[3*j:3*j+3, :nv] = self.jc[3*i:3*i+3, :]
                contact_task.b[3*j:3*j+3] = -self.pinocchioInterface_ptr.getFrame6dAcc_localWorldAligned(self.foot_names[i]).linear
                j += 1
        return contact_task

    def formulate_friction_cone_task(self) -> MatrixDB:
        friction_cone = MatrixDB("friction_cone")
        nc = len(self.foot_names)
        nv = self.pinocchioInterface_ptr.nv()
        j = 0

        friction_cone.A = np.zeros((3 * (nc - self.num_contacts), self.num_decision_vars))
        for i in range(nc):
            if not self.contact_flag[i]:
                friction_cone.A[3*j:3*j+3, nv + 3*i:nv + 3*i + 3] = np.eye(3)
                j += 1
        friction_cone.b = np.zeros(friction_cone.A.shape[0])

        friction_pyramidal = np.array([
            [0, 0, 1],
            [1, 0, -self.friction_coeff],
            [-1, 0, -self.friction_coeff],
            [0, 1, -self.friction_coeff],
            [0, -1, -self.friction_coeff]
        ])

        friction_cone.C = np.zeros((5 * self.num_contacts, self.num_decision_vars))
        friction_cone.ub = np.zeros(5 * self.num_contacts)
        friction_cone.lb = -1e16 * np.ones(5 * self.num_contacts)

        j = 0
        for i in range(nc):
            if self.contact_flag[i]:
                friction_cone.C[5*j:5*j+5, nv + 3*i:nv + 3*i + 3] = friction_pyramidal
                friction_cone.lb[5*j] = 0.0
                friction_cone.ub[5*j] = 400.0
                j += 1

        return friction_cone

    def formulate_base_task(self) -> MatrixDB:
        base_task = MatrixDB("base_task")
        nv = self.pinocchioInterface_ptr.nv()

        base_task.A = np.zeros((6, self.num_decision_vars))
        J = self.pinocchioInterface_ptr.getJacobia_local(self.base_name)
        base_task.A[:, :nv] = J

        acc_fb = np.zeros(6)
        pos_traj = self.reference_buffer.getIntegratedBasePosTraj()
        rpy_traj = self.reference_buffer.getIntegratedBaseRpyTraj()
        vel_traj = self.reference_buffer.getOptimizedBaseVelTraj()
        omega_traj = self.reference_buffer.getOptimizedBaseOmegaTraj()

        if pos_traj is not None and rpy_traj is not None and vel_traj is not None and omega_traj is not None:
            time_now = self.node_handle.get_clock().now().nanoseconds*1e-9 + self.dt
            base_pose = self.pinocchioInterface_ptr.getFramePose(self.base_name)
            base_twist = self.pinocchioInterface_ptr.getFrame6dVel_local(self.base_name)

            pose_ref = pin.SE3()
            pose_ref.rotation = self.to_rotation_matrix(rpy_traj.evaluate(time_now))
            pose_ref.translation = pos_traj.evaluate(time_now)

            spatial_vel_ref = np.hstack((
                base_pose.rotation.T @ vel_traj.evaluate(time_now),
                base_pose.rotation.T @ omega_traj.evaluate(time_now)
            ))
            spatial_acc_ref = np.hstack((
                base_pose.rotation.T @ vel_traj.derivative(time_now, 1),
                base_pose.rotation.T @ omega_traj.derivative(time_now, 1)
            ))

            pose_err = self.log6(base_pose.actInv(pose_ref)).vector
            vel_err = spatial_vel_ref - base_twist

            acc_fb = self.base_kp @ pose_err + self.base_kd @ vel_err + spatial_acc_ref
        else:
            acc_fb = np.zeros(6)

        base_task.b = acc_fb - self.pinocchioInterface_ptr.getFrame6dAcc_local(self.base_name)
        base_task.A = self.weight_base @ base_task.A
        base_task.b = self.weight_base @ base_task.b

        return base_task

    def formulate_swing_leg_task(self) -> MatrixDB:
        swing_task = MatrixDB("swing_task")
        nc = len(self.foot_names)
        nv = self.pinocchioInterface_ptr.nv()

        foot_traj = self.reference_buffer.getFootPosTraj()
        base_pos_traj = self.reference_buffer.getOptimizedBasePosTraj()

        if (nc - self.num_contacts) <= 0 or len(foot_traj) != nc or base_pos_traj is None:
            return swing_task

        t = self.node_handle.get_clock().now().nanoseconds*1e-9 + self.dt

        Qw = np.zeros((3 * (nc - self.num_contacts), 3 * (nc - self.num_contacts)))
        swing_task.A = np.zeros((3 * (nc - self.num_contacts), self.num_decision_vars))
        swing_task.b = np.zeros(3 * (nc - self.num_contacts))

        j = 0
        for i in range(nc):
            foot_name = self.foot_names[i]
            if not self.contact_flag[i]:
                Qw[3*j:3*j+3, 3*j:3*j+3] = self.weight_swing_leg
                traj = foot_traj[foot_name]
                pos_des = traj.evaluate(t)
                vel_des = traj.derivative(t, 1)
                acc_des = traj.derivative(t, 2)
                pos_m = self.pinocchioInterface_ptr.getFramePose(foot_name).translation
                vel_m = self.pinocchioInterface_ptr.getFrame6dVel_localWorldAligned(foot_name).linear

                pos_err = pos_des - pos_m
                vel_err = vel_des - vel_m
                accel_fb = self.swing_kp @ pos_err + self.swing_kd @ vel_err

                swing_task.A[3*j:3*j+3, :nv] = self.jc[3*i:3*i+3, :nv]
                swing_task.b[3*j:3*j+3] = -self.pinocchioInterface_ptr.getFrame6dAcc_localWorldAligned(foot_name).linear + accel_fb + acc_des
                j += 1

        swing_task.A[:, :6] = 0
        swing_task.A = Qw @ swing_task.A
        swing_task.b = Qw @ swing_task.b

        return swing_task

    def formulate_contact_force_task(self) -> MatrixDB:
        contact_force = MatrixDB("contact_force")
        nc = len(self.foot_names)
        nv = self.pinocchioInterface_ptr.nv()

        contact_force.A = np.zeros((3 * nc, self.num_decision_vars))
        contact_force.b = self.reference_buffer.getOptimizedForceTraj().evaluate(
            self.node_handle.get_clock().now().nanoseconds*1e-9
        )
        self.weight_contact_force = 50.0

        for i in range(nc):
            contact_force.A[3*i:3*i+3, nv + 3*i:nv + 3*i + 3] = np.eye(3)

        contact_force.A = self.weight_contact_force * contact_force.A
        contact_force.b = self.weight_contact_force * contact_force.b

        return contact_force

    def differential_inv_kin(self):
        """
        实现差分逆运动学控制。
        """
        foot_traj_array = self.reference_buffer.getFootPosTraj()
        pos_traj = self.reference_buffer.getOptimizedBasePosTraj()

        if not foot_traj_array or pos_traj is None:
            return

        nj = len(self.actuated_joints_name)
        nf = len(self.foot_names)
        contact_flag = mode_number_to_stance_leg(self.mode_buffer.get())
        self.num_contacts = int(np.sum(contact_flag))
        time_c = self.node_handle.get_clock().now().nanoseconds*1e-9 + self.dt

        base_pose = self.pinocchioInterface_ptr.getFramePose(self.base_name)
        base_twist = self.pinocchioInterface_ptr.getFrame6dVel_localWorldAligned(self.base_name)

        for k in range(nf):
            foot_name = self.foot_names[k]
            Jac_k = self.pinocchioInterface_ptr.getJacobia_localWorldAligned(foot_name)
            
            # Find indices where Jac_k[:, i + 6].head(3).norm() > 0.01
            idx = []
            for i in range(nj):
                col = Jac_k[:, i + 6]
                if np.linalg.norm(col[:3]) > 0.01:
                    idx.append(i)
            if len(idx) != 3:
                raise ValueError(f"Expected 3 active joints for foot {foot_name}, but got {len(idx)}.")

            if not contact_flag[k]:
                foot_traj = foot_traj_array[foot_name]
                if foot_traj is None:
                    continue  # 或者根据需求处理

                Js_ = Jac_k[:, [i + 6 for i in idx]][:3, :3]  # 选择相关列并截取前三行
                qpos_s = self.pinocchioInterface_ptr.qpos()[[7+i for i in idx]]
                # print("Js_:",Js_)
                # print("qpos_s:",qpos_s)
                J_inv = np.linalg.inv(Js_)

                # Desired positions and velocities
                pos_des = foot_traj.evaluate(time_c) - base_pose.translation
                vel_des = foot_traj.derivative(time_c, 1) - base_twist.linear

                # Current positions and velocities
                pos_m = self.pinocchioInterface_ptr.getFramePose(foot_name).translation - base_pose.translation
                vel_m = self.pinocchioInterface_ptr.getFrame6dVel_localWorldAligned(foot_name).linear - base_twist.linear

                # Position and velocity errors
                pos_err = pos_des - pos_m
                if np.linalg.norm(pos_err) > 0.1:
                    pos_err = 0.1 * pos_err / np.linalg.norm(pos_err)
                vel_err = vel_des - vel_m
                if np.linalg.norm(vel_err) > 0.5:
                    vel_err = 0.5 * vel_err / np.linalg.norm(vel_err) + vel_m

                # Control gains
                kp_val = 40.0
                kd_val = 2.0

                # Desired joint positions and velocities
                q_des = J_inv @ pos_err + qpos_s
                qd_des = J_inv @ vel_des

                # Update actuator commands
                for i in range(3):
                    joint_idx = idx[i]
                    self.actuator_commands.Kp[joint_idx] = kp_val
                    self.actuator_commands.Kd[joint_idx] = kd_val
                    self.actuator_commands.pos[joint_idx] = q_des[i]
                    self.actuator_commands.vel[joint_idx] = qd_des[i]
            else:
                if len(self.joint_acc) == nj:
                    jnt_pos = self.pinocchioInterface_ptr.qpos()[-nj:]
                    jnt_vel = self.pinocchioInterface_ptr.qvel()[-nj:]
                    for i in range(3):
                        joint_idx = idx[i]
                        self.actuator_commands.Kp[joint_idx] = 10.0
                        self.actuator_commands.Kd[joint_idx] = 0.1
                        self.actuator_commands.pos[joint_idx] = (
                            jnt_pos[joint_idx] + jnt_vel[joint_idx] * self.dt +
                            0.5 * (self.dt ** 2) * self.joint_acc[joint_idx]
                        )
                        self.actuator_commands.vel[joint_idx] = (
                            jnt_vel[joint_idx] + self.dt * self.joint_acc[joint_idx]
                        )
                else:
                    self.node_handle.get_logger().warn("Joint accelerations not available for contact update.")

    def simple_ctrl(self):
        t_now = self.node_handle.get_clock().now().nanoseconds*1e-9

        torque = (
            -self.jc[0:6, 6:12].T @ self.reference_buffer.getOptimizedForceTraj().evaluate(t_now) +
            self.pinocchioInterface_ptr.nle()[-6:]
        )
        self.actuator_commands.torque = torque

        for i in range(2):
            if self.contact_flag[i]:
                self.actuator_commands.Kp[3*i:3*i+3] = 0.0
                self.actuator_commands.Kd[3*i:3*i+3] = 0.0
                self.actuator_commands.pos[3*i:3*i+3] = self.pinocchioInterface_ptr.qpos()[3 * i + 7, 3 * i + 10]
                self.actuator_commands.vel[3*i:3*i+3] = 0.0
            else:
                foot_traj = self.reference_buffer.getFootPosTraj()
                base_vel_traj = self.reference_buffer.getOptimizedBaseVelTraj()

                foot_pos = self.pinocchioInterface_ptr.getFramePose(self.foot_names[i]).translation

                self.actuator_commands.Kp[3*i:3*i+3] = [30, 30, 30]
                self.actuator_commands.Kd[3*i:3*i+3] = [8.0, 8.0, 8.0]

                J_inv = np.linalg.inv(self.jc[3*i:3*i+3, 6 + i*3:6 + (i+1)*3])
                delta_q = J_inv @ (foot_traj[self.foot_names[i]].evaluate(t_now) - foot_pos)
                qd_des = J_inv @ (foot_traj[self.foot_names[i]].derivative(t_now, 1) - base_vel_traj.evaluate(t_now))

                self.actuator_commands.pos[3*i:3*i+3] = self.pinocchioInterface_ptr.qpos()[3 * i + 7:3 * i + 10] + delta_q
                self.actuator_commands.vel[3*i:3*i+3] = qd_des

    def update_contact_jacobi(self):
        nc = len(self.foot_names)
        nv = self.pinocchioInterface_ptr.nv()
        self.jc = np.zeros((3 * nc, nv))
        for i in range(nc):
            J = self.pinocchioInterface_ptr.getJacobia_localWorldAligned(self.foot_names[i])    
            self.jc[3*i:3*i+3, :] = J[:3, :]


    def log6(self, M):
        """
        Log map for SE(3) to se(3). Returns a twist (se3) associated with the rigid transformation.
        Args:
            M (np.ndarray): The 4x4 homogeneous transformation matrix.
        Returns:
            pin.Motion: The twist associated with the transformation.
        """
        # Create SE3 object from the 4x4 matrix M
        se3_obj = pin.SE3(M)
        
        # Compute the log (twist) of the SE3 transformation
        twist = pin.log6(se3_obj)
        
        return twist

    def to_rotation_matrix(self, rpy: np.ndarray) -> np.ndarray:
        """
        将 Roll-Pitch-Yaw 角转换为旋转矩阵。
        """
        return pin.rpy.rpyToMatrix(rpy)
