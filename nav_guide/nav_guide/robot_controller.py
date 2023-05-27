import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import ast
from nav_guide.MAPS import select_map

class RobotControllerNode(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.declare_parameter('target_node', 'astar_route')
        self.target_node = self.get_parameter('target_node').get_parameter_value().string_value
        self.pub = self.create_publisher(String, 'robot_command', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)  
        # self.sub = self.create_subscription(String, 'qlearning_route', self.listener_callback, 10)
        self.sub = self.create_subscription(String, self.target_node, self.listener_callback, 10)
        
    def timer_callback(self):
        msg = String()
        map, start, goal = select_map(STAGE=4), (0,0), (49,49)
        msg.data = str([map, start, goal])
        self.pub.publish(msg)
        self.timer.cancel()
        
    def listener_callback(self, msg):
        x = ast.literal_eval(msg.data)
        print(f'Route found by {self.target_node} is {x}')
        
def main(args=None):
    rclpy.init(args=args)
    robot_controller_node = RobotControllerNode()
    rclpy.spin(robot_controller_node)
    robot_controller_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
