# main.py

import rclpy
from rclpy.node import Node
from core.gait.foothold_optimization import FootholdOptimization
from core.pinocchio_interface import PinocchioInterface
from core.reference_buffer import ReferenceBuffer

class FootholdOptimizationNode(Node):
    def __init__(self):
        super().__init__('foothold_optimization_node')

        # 声明参数
        self.declare_parameter('config_file', 'path/to/config.yaml')

        # 初始化PinocchioInterface和ReferenceBuffer
        urdf_path = self.get_parameter('urdf_file').value  # 假设有urdf_file参数
        pinocchio_interface = PinocchioInterface(urdf_path)
        reference_buffer = ReferenceBuffer()

        # 初始化FootholdOptimization
        self.foothold_optimizer = FootholdOptimization(
            node_handle=self,
            pinocchio_interface=pinocchio_interface,
            reference_buffer=reference_buffer
        )

        # 创建定时器，定期调用优化方法
        timer_period = 1.0  # 1秒
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info('Optimizing footholds...')
        self.foothold_optimizer.optimize()
        self.get_logger().info('Foothold optimization completed.')

def main(args=None):
    rclpy.init(args=args)
    node = FootholdOptimizationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
