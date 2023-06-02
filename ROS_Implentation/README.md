# ROS Implementation of Path Planning Project
- You can pull our project's docker image with ROS integration using below docker command and follow the [ROS Implementaion guide](https://github.com/somedamnauthor/NavGuru/blob/master/ros_output/steps_to_run_ros_docker.md) to reproduce the ROS implementaion of the project.
  - ***docker pull parthipanr/nav_guide:latest***
- We have converted the different algorithm path finding algorithms and the robot_controller function into 4 nodes as described in the architecture below,
  ![ROS_arch](https://github.com/somedamnauthor/NavGuru/assets/21141134/fdfedfc3-877f-4a94-ad3b-43adc97bf435)
- Each node has recieves and uses the topic concept of the ROS to send request and response.
- The below video and screesnhots depicts the demo of ROS in our Project

  https://github.com/somedamnauthor/NavGuru/assets/21141134/8d3c93ac-4e51-4e60-9491-3d50b988d350

