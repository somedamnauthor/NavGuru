import numpy as np
# np.random.seed(0)
from environment import environment 

import MAPS

def q_learning_route(STAGE, start, finish):

    STAGE = 1
    start = (0,0)
    finish = (9,9)

    np.random.seed(0)

    maps = np.array([[0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                        [0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
                        [0, -1, 0, 0, -1, 0, 0, 0, 0, 0],
                        [0, -1, -1, 0, 0, 0, -1, 0, 0, 0],
                        [-1, 0, -1, 0, 0, 0, -1, -1, -1, 0],
                        [-1, 0, -1, 0, 0, 0, -1, 0, 0, 0],
                        [-1, 0, 0, 0, 0, 0, -1, 0, 0, 0],
                        [-1, -1, -1, 0, 0, 0, -1, 0, 0, 0],
                        [-1, 0, 0, 0,- 1, 0, -1, 0, 0, 1]])

    # maps = MAPS.select_map(STAGE)
    # maps = np.array(maps) * -1
    # maps[finish[0]][finish[1]] = 1

    # print(maps)

    # maze_50[49][49] = 1

    # print(maze_20)
    env = environment(maps, start, finish)
    shortest_path = []

    x, y = maps.shape
    nb_states = x * y  
    nb_actions = len(env.actions)    
    qtable = np.zeros((nb_states, nb_actions))
    episodes = 20000
    alpha = 0.5
    gamma = 0.9
    epsilon = 0.1     
    epsilon_decay = 1/episodes
    shortest_path = q_train(env, qtable, episodes, alpha, gamma, epsilon, epsilon_decay,shortest_path)
    print(f"shortest_path {shortest_path}")

    return shortest_path
    # print(qtable)

def q_train(env, qtable, episodes, alpha, gamma, epsilon,epsilon_decay,shortest_path):
    
    for _ in range(episodes):        
        # if _ >= 1000:
        #     print(f"here ")

        print(f"episode {_}")

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
                # if _ >= 1000:
                #     print(f"shortest path {action}")    
            new_state, reward, done = env.step(action)  
            qtable[state,action] = qtable[state,action] + alpha * (reward + gamma * np.max(qtable[new_state]) - qtable[state,action])
            state = new_state
            path.append(env.pos)
        if env.success:    
            shortest_path = check_if_shortest(path, shortest_path)
        # if _ > 1000:
        #     print(f"shortest path {path}")
        # epsilon = max(epsilon - epsilon_decay, 0)  
    # print(path)    
    return shortest_path  

def check_if_shortest(path, shortest_path):
    if not shortest_path or len(path) < len(shortest_path):
        shortest_path = path   
        
    return shortest_path

if __name__ == '__main__':
    q_learning_route(STAGE=1, start=(0,0), finish=(9,9))    