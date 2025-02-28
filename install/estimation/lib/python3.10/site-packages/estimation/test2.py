from motion_phase_definition import mode_number_to_stance_leg,stance_leg_to_mode_number,mode_number_to_string,string_to_mode_number
from leg_logic import get_time_of_next_lift_off
from rclpy.node import Node

class StateEstimationLKF:
    def __init__(self, node_handle: Node):
        self.node_handle = node_handle
        self.mode_number_to_stance_leg = mode_number_to_stance_leg()
        self.get_time_of_next_lift_off = get_time_of_next_lift_off

if __name__ == "__main__":
    kf=StateEstimationLKF
