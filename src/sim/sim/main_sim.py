# main_sim.py

import rclpy
from rclpy.node import Node
from .sim_publisher import SimPublisher, ActuatorCmdsBuffer
from .simulate import Simulate
import threading
import signal
import sys
import time
import mujoco
import yaml
import mujoco.viewer  # >>>> 新增

actuator_cmds_buffer= ActuatorCmdsBuffer()

def signal_handler(signum, frame):
    global stop_flag
    stop_flag = True
    print("Signal received, shutting down...")

def physics_loop(sim: Simulate):
    """
    执行物理仿真的主循环。
    """
    syncMisalign = 0.1  # maximum mis-alignment before re-sync (simulation seconds)
    simRefreshFraction = 0.7  # fraction of refresh available for simulation
    kErrorLength = 1024  # load error string length
    last_time = time.time()

    ctrlnoise = None

    while not sim.exitrequest.is_set():
        start_time = time.time()
        
        # 运行仿真
        if sim.run and (sim.m_ is not None) and (sim.d_ is not None):
            # 应用控制命令

            # 计算每次仿真步骤的更新频率
            elapsed_time = time.time() - start_time
            frequency = 1.0 / elapsed_time if elapsed_time > 0 else 0.0

            apply_ctrl(sim)
            sim.step()

        else: 
            time.sleep(0.001)  # 1 ms


        # 如果全局 stop_flag 变成 True，则要求退出
        if stop_flag:
            sim.exitrequest.set()
            rclpy.shutdown()

            break

    print("[Python Sim Main] Physics thread loop ended. Cleanup is needed.")
    # 在这里做类似于 free(ctrlnoise) / mj_deleteData / mj_deleteModel 的释放工作
    if sim.d_ is not None:
        mujoco.mj_resetData(sim.d_)
        sim.d_ = None
    if sim.m_ is not None:
        mujoco.mj_resetModel(sim.m_)
        sim.m_ = None

    print("[Python Sim Main] Physics thread fully terminated.")

def apply_ctrl(sim: Simulate):
    """
    应用控制命令到仿真数据。
    """ 
    buffer = sim.actuator_cmds_buffer
    with buffer.mtx:
        # print("buffer.actuators_name",buffer.actuators_name)
       
        if buffer is None:
            print("buffer is None")
            return 
        # print("sim.m_.nu",sim.m_.nu)
        if len(buffer.actuators_name) != sim.m_.nu:
            #print("len(buffer.actuators_name) != sim.m_.nu")
            return 
        for k in range(len(buffer.actuators_name)):
            actuator_name = buffer.actuators_name[k]
            actuator_id = mujoco.mj_name2id(sim.m_, mujoco.mjtObj.mjOBJ_ACTUATOR, actuator_name.encode('utf-8'))
            # print("actuator_name",actuator_name)
            if actuator_id == -1:
                sim.sim_publisher.get_logger().info(f"Actuator {actuator_name} not found in MuJoCo.")
                continue
            
            joint_id = mujoco.mj_name2id(sim.m_, mujoco.mjtObj.mjOBJ_JOINT, actuator_name.encode('utf-8'))
            # print("joint_id",joint_id)
            if joint_id == -1:
                sim.sim_publisher.get_logger().warn(f"Joint {actuator_name} does not exist.")
                continue
            
            qpos_id = sim.m_.jnt_qposadr[joint_id]
            qvel_id = sim.m_.jnt_dofadr[joint_id]
            
            # 计算控制命令
            sim.d_.ctrl[actuator_id] = (
                buffer.kp[k] * (buffer.pos[k] - sim.d_.qpos[qpos_id]) +
                buffer.kd[k] * (buffer.vel[k] - sim.d_.qvel[qvel_id]) +
                buffer.torque[k]
            )
            # print("sim.d_.ctrl[actuator_id]",sim.d_.ctrl[actuator_id])
            
            # 限制控制命令的范围
            sim.d_.ctrl[actuator_id] = max(-100.0, min(100.0, sim.d_.ctrl[actuator_id]))

    return 
    
def main(args=None):
    global stop_flag
    stop_flag = False

    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 初始化ROS 2
    rclpy.init(args=args)

    # 创建Simulate实例
    sim = Simulate()

    # 检查命令行参数是否提供了配置文件
    if len(sys.argv) > 1:
        config_yaml = sys.argv[1]
    else:
        print("Usage: python main_sim.py <config.yaml>")
        sys.exit(1)

    # 加载初始模型文件
    with open(config_yaml, 'r') as file:
        config_ = yaml.safe_load(file)
    model_file = config_["model"]["package"]
    from ament_index_python.packages import get_package_share_directory
    model_path = get_package_share_directory(model_file) + config_["model"]["xml"]
    sim.filename = model_path.encode('utf-8')
    sim.load_model(model_path)

    # 创建SimPublisher节点
    sim_publisher = SimPublisher(sim, config_yaml)
    # print("sim_publisher.actuator_cmds_buffer_",sim_publisher.actuator_cmds_buffer_.actuators_name)
    sim.sim_publisher = sim_publisher  # 让Simulate知道SimPublisher实例
    sim.actuator_cmds_buffer = sim_publisher.get_cmds_buffer()
    # sim.m_.opt.timestep = 0.001
    # print(f"Time step: {sim.m_.opt.timestep}")

    if sim.m_ is None:
        print(f"Failed to load model: {sim.load_error}")
        stop_flag = True
        sys.exit(1)
    # 启动物理仿真线程
    physics_thread = threading.Thread(target=physics_loop, args=(sim,), daemon=True)
    physics_thread.start()

    rclpy.spin(sim_publisher)    

    # 请求退出仿真
    stop_flag = True
    sim.exitrequest.set()
    sim.run = False

    # 等待物理仿真线程结束
    physics_thread.join()
        
    # 销毁节点并关闭ROS 2
    sim_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
