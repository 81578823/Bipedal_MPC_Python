# core/sim/sim_publisher.py

import yaml
import threading
import time
from typing import Optional, List

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy
from sensor_msgs.msg import Imu, JointState
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
import numpy as np
from .simulate import Simulate

# 假设trans.msg和trans.srv已经通过ROS 2接口生成
from trans.msg import ActuatorCmds
from trans.srv import SimulationReset

# 假设mujoco Python绑定已安装
import mujoco
from core.core.misc.buffer import Buffer


import threading
from typing import List
import numpy as np
from core.core.types import scalar_t

class ActuatorCmdsBuffer:
    """
    ActuatorCmdsBuffer 类用于存储执行器命令，并确保线程安全。
    """
    def __init__(self):
        self.time: scalar_t = 0.0
        self.actuators_name: List[str] = []
        self.kp: List[scalar_t] = []
        self.pos: List[scalar_t] = []
        self.kd: List[scalar_t] = []
        self.vel: List[scalar_t] = []
        self.torque: List[scalar_t] = []
        self.mtx = threading.Lock()


class SimPublisher(Node):
    """
    SimPublisher 类用于发布模拟数据（IMU、JointState、Odometry等），
    订阅执行器命令，处理仿真重置请求，并管理模拟数据的发布频率。
    """
    
    def __init__(self, sim: 'Simulate', config_yaml: str):
        """
        初始化 SimPublisher 实例。
        
        Args:
            sim (Simulate): 仿真对象。
            config_yaml (str): 配置文件路径。
        """
        super().__init__('SimPublisher')
        self.sim_ = sim
        
        # 加载配置文件
        try:
            with open(config_yaml, 'r') as file:
                config_ = yaml.safe_load(file)
        except Exception as e:
            self.get_logger().error(f"Failed to load config file: {e}")
            raise e
        
        name_prefix = config_["global"]["topic_prefix"]
        model_package = config_["model"]["package"]
        from ament_index_python.packages import get_package_share_directory
        model_file = get_package_share_directory(model_package) + config_["model"]["xml"]
        
        # 设置仿真模型文件
        self.sim_.filename = model_file.encode('utf-8')  # 假设filename是bytes类型
        self.sim_.uiloadrequest += 1  # 假设uiloadrequest是一个原子计数器
        self.get_logger().info(f"model file: {model_file}")
        
        # 创建SimulationReset服务
        sim_reset_service = config_["global"]["service_names"]["sim_reset"]
        self.reset_service_ = self.create_service(
            SimulationReset,
            name_prefix + sim_reset_service,
            self.reset_callback
        )
        
        # 创建发布者
        qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE
        )
        
        imu_topic = config_["global"]["topic_names"]["imu"]
        self.imu_publisher_ = self.create_publisher(Imu, name_prefix + imu_topic, qos)
        
        joints_state_topic = config_["global"]["topic_names"]["joints_state"]
        self.joint_state_publisher_ = self.create_publisher(JointState, name_prefix + joints_state_topic, qos)
        
        odom_topic = config_["global"]["topic_names"]["odom"]
        self.odom_publisher_ = self.create_publisher(Odometry, name_prefix + odom_topic, qos)
        
        # 创建执行器命令订阅者
        actuators_cmds_topic = config_["global"]["topic_names"]["actuators_cmds"]
        self.actuator_cmd_subscription_ = self.create_subscription(
            ActuatorCmds,
            name_prefix + actuators_cmds_topic,
            self.actuator_cmd_callback,
            qos
        )
        
        # 初始化执行器命令缓冲区
        self.actuator_cmds_buffer_ = ActuatorCmdsBuffer()
        
        # 创建定时器列表
        self.timers_: List[rclpy.timer.Timer] = []
        
        # 设置IMU发布频率
        freq_imu = config_["simulation"]["frequency"]["imu"]
        imu_period = 1.0 / freq_imu
        self.timers_.append(self.create_timer(
            imu_period,
            self.imu_callback
        ))
        
        # 设置JointState发布频率
        freq_joints_state = config_["simulation"]["frequency"]["joints_state"]
        joints_state_period = 1.0 / freq_joints_state
        self.timers_.append(self.create_timer(
            joints_state_period,
            self.joint_callback
        ))
        
        # 设置Odometry发布频率
        freq_odom = config_["simulation"]["frequency"]["odom"]
        odom_period = 1.0 / freq_odom
        self.timers_.append(self.create_timer(
            odom_period,
            self.odom_callback
        ))
        
        # 设置丢弃旧消息的发布频率
        freq_drop_old_message = config_["simulation"]["frequency"]["drop_old_message"]
        drop_old_message_period = 1.0 / freq_drop_old_message
        self.timers_.append(self.create_timer(
            drop_old_message_period,
            self.drop_old_message
        ))
        
        # 可选：添加外部干扰的发布频率（目前注释掉）
        # freq_add_disturbance = config_["simulation"]["frequency"]["add_external_disturbance"]
        # if freq_add_disturbance > 0:
        #     add_disturbance_period = 1.0 / freq_add_disturbance
        #     self.timers_.append(self.create_timer(
        #         add_disturbance_period,
        #         self.add_external_disturbance
        #     ))
        
        self.get_logger().info("Start SimPublisher ...")
        
        # 设置噪声参数
        self.noise_acc = 0.3
        self.noise_gyro = 0.05
        self.noise_joint_vel = 0.3
    
    def reset_callback(self, request: SimulationReset.Request, response: SimulationReset.Response):
        """
        处理SimulationReset服务请求，重置仿真状态。
        
        Args:
            request (SimulationReset.Request): 服务请求。
            response (SimulationReset.Response): 服务响应。
        """
        while self.sim_.d_ is None and rclpy.ok():
            self.get_logger().info("Waiting for simulation data to be ready...")
            time.sleep(1)
        
        if self.sim_.d_ is not None:
            if request.header.frame_id != self.sim_.m_.names[0]:
                self.get_logger().error(f"reset request is not for {self.sim_.m_.names[0]}")
                response.is_success = False
            else:
                with self.sim_.mtx:
                    mujoco.mj_resetData(self.sim_.m_, self.sim_.d_)
                    # 设置基座位置和姿态
                    self.sim_.d_.qpos[0] = request.base_pose.position.x
                    self.sim_.d_.qpos[1] = request.base_pose.position.y
                    self.sim_.d_.qpos[2] = request.base_pose.position.z
                    self.sim_.d_.qpos[3] = request.base_pose.orientation.w
                    self.sim_.d_.qpos[4] = request.base_pose.orientation.x
                    self.sim_.d_.qpos[5] = request.base_pose.orientation.y
                    self.sim_.d_.qpos[6] = request.base_pose.orientation.z
                
                    # 设置关节位置
                    for i in range(len(request.joint_state.position)):
                        joint_name = request.joint_state.name[i]
                        joint_id = mujoco.mj_name2id(self.sim_.m_, mujoco.mjtObj.mjOBJ_JOINT, joint_name.encode('utf-8'))
                        if joint_id > -1:
                            qposadr = self.sim_.m_.jnt_qposadr[joint_id]
                            self.sim_.d_.qpos[qposadr] = request.joint_state.position[i]
                        else:
                            self.get_logger().warn(f"[Reset Request] joint {joint_name} does not exist")
                    
                    # 重置执行器命令
                    with self.actuator_cmds_buffer_.mtx:
                        for k in range(len(self.actuator_cmds_buffer_.actuators_name)):
                            self.actuator_cmds_buffer_.kp[k] = 0.0
                            self.actuator_cmds_buffer_.pos[k] = 0.0
                            self.actuator_cmds_buffer_.kd[k] = 0.0
                            self.actuator_cmds_buffer_.vel[k] = 0.0
                            self.actuator_cmds_buffer_.torque[k] = 0.0
                    
                response.is_success = True
                self.get_logger().info("reset robot state...")
        else:
            response.is_success = False
    
    def imu_callback(self):
        """
        发布IMU消息。
        """
        if self.sim_.d_ is not None:
            message = Imu()
            message.header.frame_id = self.sim_.m_.names[0]
            message.header.stamp = self.get_clock().now().to_msg()
            with self.sim_.mtx:
                acc_found = False
                gyro_found = False
                quat_found = False
                for i in range(self.sim_.m_.nsensor):
                    sensor_type = self.sim_.m_.sensor_type[i]
                    sensor_adr = self.sim_.m_.sensor_adr[i]
                    if sensor_type == mujoco.mjtSensor.mjSENS_ACCELEROMETER:
                        message.linear_acceleration.x = self.sim_.d_.sensordata[sensor_adr] + self.noise_acc * np.random.normal()
                        message.linear_acceleration.y = self.sim_.d_.sensordata[sensor_adr + 1] + self.noise_acc * np.random.normal()
                        message.linear_acceleration.z = self.sim_.d_.sensordata[sensor_adr + 2] + self.noise_acc * np.random.normal()
                        acc_found = True
                    elif sensor_type == mujoco.mjtSensor.mjSENS_FRAMEQUAT:
                        message.orientation.w = self.sim_.d_.sensordata[sensor_adr]
                        message.orientation.x = self.sim_.d_.sensordata[sensor_adr + 1]
                        message.orientation.y = self.sim_.d_.sensordata[sensor_adr + 2]
                        message.orientation.z = self.sim_.d_.sensordata[sensor_adr + 3]
                        quat_found = True
                    elif sensor_type == mujoco.mjtSensor.mjSENS_GYRO:
                        message.angular_velocity.x = self.sim_.d_.sensordata[sensor_adr] + self.noise_gyro * np.random.normal()
                        message.angular_velocity.y = self.sim_.d_.sensordata[sensor_adr + 1] + self.noise_gyro * np.random.normal()
                        message.angular_velocity.z = self.sim_.d_.sensordata[sensor_adr + 2] + self.noise_gyro * np.random.normal()
                        gyro_found = True
                if not acc_found:
                    self.get_logger().warn("Required acc sensor does not exist")
                if not quat_found:
                    self.get_logger().warn("Required quat sensor does not exist")
                if not gyro_found:
                    self.get_logger().warn("Required gyro sensor does not exist")
            self.imu_publisher_.publish(message)
    
    def odom_callback(self):
        """
        发布Odometry消息。
        """
        if self.sim_.d_ is not None:
            message = Odometry()
            with self.sim_.mtx:
                message.header.frame_id = self.sim_.m_.names[0]
                message.header.stamp = self.get_clock().now().to_msg()
                # 设置位置和姿态
                message.pose.pose.position.x = self.sim_.d_.qpos[0]
                message.pose.pose.position.y = self.sim_.d_.qpos[1]
                message.pose.pose.position.z = self.sim_.d_.qpos[2]
                message.pose.pose.orientation.w = self.sim_.d_.qpos[3]
                message.pose.pose.orientation.x = self.sim_.d_.qpos[4]
                message.pose.pose.orientation.y = self.sim_.d_.qpos[5]
                message.pose.pose.orientation.z = self.sim_.d_.qpos[6]
                # 设置线速度和角速度
                message.twist.twist.linear.x = self.sim_.d_.qvel[0]
                message.twist.twist.linear.y = self.sim_.d_.qvel[1]
                message.twist.twist.linear.z = self.sim_.d_.qvel[2]
                message.twist.twist.angular.x = self.sim_.d_.qvel[3]
                message.twist.twist.angular.y = self.sim_.d_.qvel[4]
                message.twist.twist.angular.z = self.sim_.d_.qvel[5]
            self.odom_publisher_.publish(message)
    
    def joint_callback(self):
        """
        发布JointState消息。
        """
        if self.sim_.d_ is not None:
            jointState = JointState()
            jointState.header.frame_id = self.sim_.m_.names[0]
            jointState.header.stamp = self.get_clock().now().to_msg()
            with self.sim_.mtx:
                for i in range(self.sim_.m_.njnt):
                    if self.sim_.m_.jnt_type[i] != mujoco.mjtJoint.mjJNT_FREE:
                        jnt_name = mujoco.mj_id2name(self.sim_.m_, mujoco.mjtObj.mjOBJ_JOINT, i).decode('utf-8')
                        jointState.name.append(jnt_name)
                        qpos = self.sim_.d_.qpos[self.sim_.m_.jnt_qposadr[i]]
                        jointState.position.append(qpos)
                        qvel = self.sim_.d_.qvel[self.sim_.m_.jnt_dofadr[i]] + self.noise_joint_vel * np.random.normal()
                        jointState.velocity.append(qvel)
                        torque = self.sim_.d_.qfrc_actuator[self.sim_.m_.jnt_dofadr[i]]
                        jointState.effort.append(torque)
            self.joint_state_publisher_.publish(jointState)
    
    def actuator_cmd_callback(self, msg: ActuatorCmds):
        """
        处理来自执行器命令的消息。
        
        Args:
            msg (ActuatorCmds): 执行器命令消息。
        """
        if self.sim_.d_ is not None:
            with self.actuator_cmds_buffer_.mtx:
                # 将ROS时间转换为秒（float）
                msg_time = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
                self.actuator_cmds_buffer_.time = msg_time
                self.actuator_cmds_buffer_.actuators_name = list(msg.names)
                self.actuator_cmds_buffer_.kp = list(msg.gain_p)
                self.actuator_cmds_buffer_.pos = list(msg.pos_des)
                self.actuator_cmds_buffer_.kd = list(msg.gaid_d)
                self.actuator_cmds_buffer_.vel = list(msg.vel_des)
                self.actuator_cmds_buffer_.torque = list(msg.feedforward_torque)
            # self.get_logger().info(f"subscribe actuator cmds {self.actuator_cmds_buffer_.time}")
    
    def drop_old_message(self):
        """
        丢弃旧的执行器命令消息，如果与当前时间的差距超过0.2秒。
        """
        with self.actuator_cmds_buffer_.mtx:
            current_time = self.get_clock().now().to_msg().sec + self.get_clock().now().to_msg().nanosec * 1e-9
            if abs(self.actuator_cmds_buffer_.time - current_time) > 0.2:
                for k in range(len(self.actuator_cmds_buffer_.actuators_name)):
                    self.actuator_cmds_buffer_.kp[k] = 0.0
                    self.actuator_cmds_buffer_.pos[k] = 0.0
                    self.actuator_cmds_buffer_.kd[k] = 0.0
                    self.actuator_cmds_buffer_.vel[k] = 0.0
                    self.actuator_cmds_buffer_.torque[k] = 0.0
    
    def add_external_disturbance(self):
        """
        添加外部干扰到仿真中。
        """
        with self.sim_.mtx:
            if self.sim_.d_ is None:
                return
            if self.sim_.d_.time < 15.0:
                self.added = False
                return
            elif getattr(self, 'added', False):
                return
            else:
                self.added = True
                self.sim_.d_.qvel[0] += 0.3
                self.sim_.d_.qvel[1] += 0.5
    
    def get_cmds_buffer(self) -> Optional[ActuatorCmdsBuffer]:
        """
        获取执行器命令缓冲区。
        
        Returns:
            Optional[ActuatorCmdsBuffer]: 执行器命令缓冲区。
        """
        return self.actuator_cmds_buffer_
