import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import ast
from collections import defaultdict
from math import sqrt, pow
from queue import PriorityQueue

class ASTAR:

    def __init__(self, maps) -> None:
        self.maps = maps
        self.graph = defaultdict(list)
        self.dict = {}
        
    def set_map_value(self, x, y, value):
        self.maps[y][x] = value

    def addedge(self, x, y, cost):
        self.graph[x].append((y, cost))
        self.graph[y].append((x, cost))

    def create_edge(self):
        n = len(self.maps)
        for i in range(n):
            for j in range(n):
                if self.maps[i][j] == 0:
                    if i + 1 < n and self.maps[i+1][j] == 0:
                        self.addedge((i, j), (i+1, j), 1)
                    if j + 1 < n and self.maps[i][j+1] == 0:
                        self.addedge((i, j), (i, j+1), 1)
                    if j - 1 >= 0 and self.maps[i][j-1] == 0:
                        self.addedge((i, j), (i, j-1), 1)
                    if j + 1 < n and i + 1 < n and self.maps[i+1][j+1] == 0:
                        self.addedge((i, j), (i+1, j+1), sqrt(2))
                    if j - 1 >= 0 and i + 1 < n and self.maps[i+1][j-1] == 0:
                        self.addedge((i, j), (i+1, j-1), sqrt(2))

    def set_heuristic(self):
        n = len(self.maps)
        for i in range(n):
            for j in range(n):
                if self.maps[i][j] == 0:
                    self.dict[(i, j)] = round(sqrt(pow(n-i-1, 2) + pow(n-j-1, 2)), 2)

    def a_star_search(self, source, target):
            visited = []
            traced = {}
            route = []
            p_queue = PriorityQueue()
            p_queue.put((self.dict[source], source, 0, None))
            
            while p_queue.empty() == False:
                total_cost, current_node, prev_cost, prev_node = p_queue.get()

                if current_node not in visited:
                    visited.append(current_node)
                    traced[current_node] = prev_node
                    if current_node == target:
                        route.append(current_node)
                        while prev_node != None:
                            route.append(prev_node)
                            prev_node = traced[prev_node]
                        break

                    for node, cost in self.graph[current_node]:
                        total_cost = cost + prev_cost
                        p_queue.put((self.dict[node] + total_cost, node, total_cost, current_node))
            route.reverse()
            return visited, traced, route, total_cost

    def get_route(self, start, finish):
        self.create_edge()
        self.set_heuristic()
        visited, traced, route, total_cost = self.a_star_search(start, finish)
        return route

def astar_route(STAGE, start, finish):
    # maps = MAPS.select_map(STAGE)
    maps = STAGE
    astar = ASTAR(maps)
    route = astar.get_route(start, finish)
    # print(route)
    return(route)

class AStarNode(Node):
    def __init__(self):
        super().__init__('astar')
        self.sub = self.create_subscription(String, 'robot_command', self.listener_callback, 10)
        self.pub = self.create_publisher(String, 'astar_route', 10)
        self.route = []
        
    def listener_callback(self, msg):
        x = ast.literal_eval(msg.data)
        # self.get_logger().info('I heard: "%s"' % msg.data)
        print(f'Map we got for Astar:: {x[0]}, Start :{x[1]}, end:{x[2]}')
        self.route = astar_route(STAGE=x[0], start=x[1], finish=x[2])
        
        # sending route back to robot_controller
        msg = String()
        msg.data = str(self.route)
        self.pub.publish(msg)
        
def main(args=None):
    rclpy.init(args=args)
    astar_node = AStarNode()
    rclpy.spin(astar_node)
    astar_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
