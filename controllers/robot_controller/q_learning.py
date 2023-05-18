import numpy as np
from environment import environment 
import MAPS

def q_learning_route(STAGE, start, finish):

    np.random.seed(0)

    maps = MAPS.select_map(STAGE)
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
              
        # if verbose and episode % 100 == 0:          
        #     print(f" episode {episode} reward {reward}")
    # print(f"shortest_path {shortest_path}")
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

if __name__ == '__main__':
    q_learning_route(STAGE=4, start=(0,0), finish=(49,49))    
