import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import ast
from collections import defaultdict
from math import sqrt, pow
from queue import PriorityQueue

import numpy as np
from nav_guide.environment import environment 

def q_learning_route(STAGE, start, finish):
    np.random.seed(0)
    maps = STAGE
    maps = np.array(maps) * -1
    maps[finish[0]][finish[1]] = 1
    
    env = environment(maps, start, finish)
    shortest_path = []

    x, y = maps.shape
    nb_states = x * y  
    nb_actions = len(env.actions)    
    qtable = np.zeros((nb_states, nb_actions))
    episodes = 1000
    alpha = 0.01
    gamma = 0.9
    epsilon = 1     
    epsilon_decay = 1/episodes
    decay = True
    verbose =True
    shortest_path = q_train(env, qtable, episodes, alpha, gamma, epsilon, epsilon_decay, decay, shortest_path, verbose)
    return shortest_path

def q_train(env, qtable, episodes, alpha, gamma, epsilon,epsilon_decay,decay,shortest_path,verbose):
    
    for episode in range(episodes):    
        state = env.reset()
        done = False
        path = []
        path.append(env.pos)
        while not done:
            rnd = np.random.random()

            if rnd < epsilon:
                action = env.action_sample() 
            else:  
                action = np.argmax(qtable[state]) 
            new_state, reward, done = env.step(action)  
            qtable[state,action] = qtable[state,action] + alpha * (reward + gamma * np.max(qtable[new_state]) - qtable[state,action])
            state = new_state
            path.append(env.pos)
        if env.success:    
            shortest_path = check_if_shortest(path, shortest_path)
        if decay:    
            epsilon = max(epsilon - epsilon_decay, 0)  
    return shortest_path  

def check_if_shortest(path, shortest_path):
    if not shortest_path or len(path) < len(shortest_path):
        shortest_path = path          
    return shortest_path

def zero_to_one(arr):
    for x, row in enumerate(arr):
        for y, ele in enumerate(row):
            if(ele == 0):
                arr[x][y] = 1

    return arr 

class QLearningNode(Node):
    def __init__(self):
        super().__init__('qlearning')
        self.sub = self.create_subscription(String, 'robot_command', self.listener_callback, 10)
        self.pub = self.create_publisher(String, 'qlearning_route', 10)
        self.route = []
        
    def listener_callback(self, msg):
        x = ast.literal_eval(msg.data)
        # self.get_logger().info('I heard: "%s"' % msg.data)
        print(f'Map we got for QLearning:: {x[0]}, Start :{x[1]}, end:{x[2]}')
        self.route = q_learning_route(STAGE=x[0], start=x[1], finish=x[2])
        
        # sending route back to robot_controller
        msg = String()
        msg.data = str(self.route)
        self.pub.publish(msg)
        
def main(args=None):
    rclpy.init(args=args)
    qlearning_node = QLearningNode()
    rclpy.spin(qlearning_node)
    qlearning_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
