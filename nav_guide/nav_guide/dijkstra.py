import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import ast
from collections import defaultdict
from math import sqrt, pow
from queue import PriorityQueue
import numpy as np
# import matplotlib.pyplot as plt
# import MAPS

def valid_node(node, size_of_grid):
    if node[0] < 0 or node[0] >= size_of_grid:
        return False
    if node[1] < 0 or node[1] >= size_of_grid:
        return False
    return True

def up(node):
    return (node[0]-1,node[1])

def down(node):
    return (node[0]+1,node[1])

def left(node):
    return (node[0],node[1]-1)

def right(node):
    return (node[0],node[1]+1)

def upLeft(node):
    return (node[0]-1, node[1]-1)

def upRight(node):
    return (node[0]-1, node[1]+1)

def downLeft(node):
    return (node[0]+1, node[1]-1)

def downRight(node):
    return (node[0]+1, node[1]+1)

def backtrack(initial_node, desired_node, distances):
    path = [desired_node]
    size_of_grid = distances.shape[0]
    while True:
        potential_distances = []
        potential_nodes = []
        directions = [up,down,left,right,upLeft,upRight,downLeft,downRight]
        for direction in directions:
            node = direction(path[-1])
            if valid_node(node, size_of_grid):
                potential_nodes.append(node)
                potential_distances.append(distances[node[0],node[1]])
        least_distance_index = np.argmin(potential_distances)
        path.append(potential_nodes[least_distance_index])
        if path[-1][0] == initial_node[0] and path[-1][1] == initial_node[1]:
            break

    return list(reversed(path))

def dijkstra(initial_node, desired_node, obstacles):
    """Dijkstras algorithm for finding the shortest path between two nodes in a graph.

    Args:
        initial_node (list): [row,col] coordinates of the initial node
        desired_node (list): [row,col] coordinates of the desired node
        obstacles (array 2d): 2d numpy array that contains any obstacles as 1s and free space as 0s

    Returns:
        list[list]: list of list of nodes that form the shortest path
    """
    # initialize cost heuristic map
    obstacles = obstacles.copy()
    # obstacles should have very high cost, so we avoid them.
    obstacles *= 1000
    # normal tiles should have 1 cost (1 so we can backtrack)
    obstacles += np.ones(obstacles.shape)
    # source and destination are free
    obstacles[initial_node[0],initial_node[1]] = 0
    obstacles[desired_node[0],desired_node[1]] = 0

    # initialize maps for distances and visited nodes
    size_of_floor = obstacles.shape[0]

    # we only want to visit nodes once
    visited = np.zeros([size_of_floor,size_of_floor],bool)

    # initiate matrix to keep track of distance to source node
    # initial distance to nodes is infinity so we always get a lower actual distance
    distances = np.ones([size_of_floor,size_of_floor]) * np.inf
    # initial node has a distance of 0 to itself
    distances[initial_node[0],initial_node[1]] = 0

    # start algorithm
    current_node = [initial_node[0], initial_node[1]]
    while True:
        directions = [up, down, left, right, upLeft, upRight, downLeft, downRight]
        for direction in directions:
            potential_node = direction(current_node)
            if valid_node(potential_node, size_of_floor): # boundary checking
                if not visited[potential_node[0],potential_node[1]]: # check if we have visited this node before
                    # update distance to node
                    distance = distances[current_node[0], current_node[1]] + obstacles[potential_node[0],potential_node[1]]

                    # update distance if it is the shortest discovered
                    if distance < distances[potential_node[0],potential_node[1]]:
                        distances[potential_node[0],potential_node[1]] = distance


        # mark current node as visited
        visited[current_node[0]  ,current_node[1]] = True

        # select next node
        # by choosing the the shortest path so far
        t=distances.copy()
        # we don't want to visit nodes that have already been visited
        t[np.where(visited)]=np.inf
        # choose the shortest path
        node_index = np.argmin(t)

        # convert index to row,col.
        node_row = node_index//size_of_floor
        node_col = node_index%size_of_floor
        # update current node.
        current_node = (node_row, node_col)

        # stop if we have reached the desired node
        if current_node[0] == desired_node[0] and current_node[1]==desired_node[1]:
            break

    # backtrack to construct path
    return backtrack(initial_node,desired_node,distances)

def dijkstra_route(STAGE, start, finish):
    maps = STAGE
    obstacles = np.array(maps, dtype=float)
    path = dijkstra(start, finish, obstacles)
    # print(path)
    return path

class DijkstraNode(Node):
    def __init__(self):
        super().__init__('dijkstra')
        self.sub = self.create_subscription(String, 'robot_command', self.listener_callback, 10)
        self.pub = self.create_publisher(String, 'dijkstra_route', 10)
        self.route = []
        
    def listener_callback(self, msg):
        x = ast.literal_eval(msg.data)
        # self.get_logger().info('I heard: "%s"' % msg.data)
        print(f'Map we got for Dijkstra: {x[0]}, Start :{x[1]}, end:{x[2]}')
        self.route = dijkstra_route(STAGE=x[0], start=x[1], finish=x[2])
        
        # sending route back to robot_controller
        msg = String()
        msg.data = str(self.route)
        self.pub.publish(msg)
        
def main(args=None):
    rclpy.init(args=args)
    dijkstra_node = DijkstraNode()
    rclpy.spin(dijkstra_node)
    dijkstra_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
