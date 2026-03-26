
import rclpy
from rclpy.node import Node

class MissionNode(Node):

    def __init__(self):
        super().__init__('mission_node')
        self.timer = self.create_timer(0.5, self.loop)

    def loop(self):
        self.get_logger().info('Mission loop running...')

def main(args=None):
    rclpy.init(args=args)
    node = MissionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
