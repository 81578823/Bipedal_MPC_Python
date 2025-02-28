import pinocchio
from rclpy.node import Node
import rclpy

rclpy.init()

node = Node("test")

print("time", node.get_clock().now().nanoseconds*1e-9)
print("time", node.get_clock().now().seconds_nanoseconds()[0])
dir(pinocchio)
