import numpy as np
from environment import environment 
import MAPS


def qlearning_route(STAGE, start, finish):
    
    maps = MAPS.select_map(STAGE)
    for row in range(len(maps)):
        for i in range(len(maps[row])):
            maps[row][i] *= -1
             
    maps[finish[0]][finish[1]] = 1
    print(maps)
    
    maze = np.array(maps) 
    env = environment(maze, start, finish)
    shortest_path = []

    x, y = maze.shape
    nb_states = x * y  
    nb_actions = len(env.actions)    
    qtable = np.zeros((nb_states, nb_actions))
    episodes = 10000
    alpha = 0.5
    gamma = 0.9
    epsilon = 1.0         
    epsilon_decay = 0.001
    shortest_path = q_train(env, qtable, episodes, alpha, gamma, epsilon, epsilon_decay,shortest_path)
    print(f"shortest_path {shortest_path}")

def q_train(env, qtable, episodes, alpha, gamma, epsilon,epsilon_decay,shortest_path):
    for _ in range(episodes):
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
        # print(f"shortest path {shortest_path}")
        epsilon = max(epsilon - epsilon_decay, 0)  
    return shortest_path  

def check_if_shortest(path, shortest_path):
    if not shortest_path or len(path) < len(shortest_path):
        shortest_path = path   
        
    return shortest_path

if __name__ == '__main__':
    # main()    
    qlearning_route(STAGE=1, start=(0,0), finish=(11,11))
