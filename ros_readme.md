For the project NavGuide, steps to create the boilerplate for ROS,

* to run the ROS2 image (make sure you pulled the foxy flavour of the ros, or use the distro you pulled)

  * *docker run -it -d ros:foxy /bin/bash*
* create a workspace

  * *mkdir -p ~/ng_ws/src*
  * *cd ~/ng_ws/src*
* to create the package for the project

  * *ros2 pkg create --build-type ament_python `<project_name>`*
  * *cd `<project_name>`/`<project_name>`*
  * create a file '*my_node.p*y'

    * *`import rclpy
      from rclpy.node import Node
      from std_msgs.msg import String*

      *class MyNode(Node):
      def __init__(self):
      super().__init__('my_node')
      self.publisher_ = self.create_publisher(String, 'topic', 10)
      timer_period = 0.5  # seconds
      self.timer = self.create_timer(timer_period, self.timer_callback)*

      *def timer_callback(self):
      msg = String()
      msg.data = 'Hello, ROS 2!'
      self.publisher_.publish(msg)
      self.get_logger().info('Publishing: "%s"' % msg.data)*

      *def main(args=None):
      rclpy.init(args=args)
      node = MyNode()
      rclpy.spin(node)
      node.destroy_node()
      rclpy.shutdown()*

      *if __name__ == '__main__':
      main()
      `*
  * add below lines to the '*console_scripts*' array in the '*setup.py*'

    * '*my_node = `<project_name>`.my_node:main',*
  * run the below commands,

    * *cd ~/ros2_ws*
    * *colcon build* (remove everything excpet src folder when rebuilding)
    * *source install/setup.bash*
    * *ros2 run `<project_name>`my_node*  (this should print 'Publishing: "Hello, ROS 2!")
    * *source /opt/ros/foxy/setup.bash* (for 2nd terminal) (This is needed if you're running more than 1 node or service or topic)

  *Baseline version of ROS2 is done.*

*Docker commads to help:*

* *To run a docker image*
  * *docker run -it -d `<img_name>` /bin/bash*
* *To exit  a docker container*
  * *'exit'*
* *To check the services running*
  * *docker -ps -a*
* *To commit the changes*
  * *docker commit <container_id> <new_name>*
* *To see the list of Docker images*
  * *docker images*
* To run a new terminal of a contianer,
  * d*ocker exec -it /bin/bash*
