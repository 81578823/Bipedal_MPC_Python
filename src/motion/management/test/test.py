import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__("my_node")
        # 使用 create_timer 设置循环频率，每 0.1 秒调用一次回调函数（10 Hz）
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        # 这里是你需要执行的定时任务
        self.get_logger().info("Running at 10 Hz")

# 初始化并启动节点
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    # 关闭节点
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
