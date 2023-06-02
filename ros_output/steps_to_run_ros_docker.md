# Steps to reproduce ROS docker implementation

- Pull the docker image using below command and execute the follwing command
    - ***docker pull parthipanr/nav_guide:latest***
    - docker run -it parthipanr/nav_guide:latest
    - cd 
    - cd ros2_ws
    - source /opt/ros/foxy/setup.bash
    - ./deploy.sh
    - source install/setup.bash
    - ros2 run nav_guide astar

- open a new terminal and connect to the same container of the image 'parthipanr/nav_guide:latest' use the below commands to connect to same container and follow the 'ROS execution steps' below that.
  - In the winodws/MAC termninal use below command to get the conatiner id
    - docker ps -a 
    - docker exec -it <continer_id> /bin/bash
- ROS execution steps
  - cd 
  - cd ros2_ws
  - source /opt/ros/foxy/setup.bash
  - source install/setup.bash
  - ros2 run nav_guide robot_controller
