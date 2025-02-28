# main.py

import rclpy
from rclpy.executors import MultiThreadedExecutor
from .motion_manager import MotionManager

def main(args=None):
    # 初始化ROS 2 Python客户端库
    rclpy.init(args=args)
        
    # 创建一个多线程执行器，使用4个线程
    executor = MultiThreadedExecutor(num_threads=4)
    
    try:
        # 初始化 MotionManager 的子模块
        node = MotionManager()

        # 将节点添加到执行器
        executor.add_node(node)
        
        # 启动执行器，开始处理回调
        executor.spin()
        
    except Exception as e:
        # 记录任何异常信息
        node.get_logger().error(f"Exception in main: {e}")
    
    finally:
        # 优雅地关闭执行器和节点
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
