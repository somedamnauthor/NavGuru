import random
import numpy as np
class environment:
    def __init__(self, env, start, goal, mistep_count = 10, penalty = -1):
        self.actions = [
            "left", "right","up", "down","left-up","left-down","right-up","right-down"]
        self.actions_coords = {
            0 : (0, 1), 1 : (0, -1), 2 : (-1, 0), 3 : (1, 0),
            4 : (-1, 1), 5 : (1, 1), 6 : (-1, -1), 7 : (1, -1)}
        self.env = env
        self.start = start
        self.goal = goal
        self.pos = start        
        self.pos_end = env.shape
        self.state = self.get_state(self.pos)
        self.reward = 0
        self.mistep_count = mistep_count * -1
        self.next_state = start
        self.penalty = penalty
        self.success = False
        

    def reset(self):
        self.pos = self.start
        self.reward = 0
        self.success = False
        return self.get_state(self.start)
    
    def get_state(self, pos):
        x, y = pos
        x_end, y_end = self.pos_end
        self.reward = 0
        return x * y_end +  y
    
    def step(self, action):
        done = False
        x, y = self.pos
        if self.actions[action] not in self.get_possible_actions(self.pos):
            self.reward += self.penalty
            return self.get_state(self.pos), self.reward , done
        else:
            act_x, act_y = self.actions_coords.get(action)        
            self.pos = (x + act_x, y + act_y)
            self.next_state = self.get_state(self.pos)
            self.reward += self.env[x + act_x][y + act_y]
            if self.reward < self.mistep_count : 
                done = True
            elif self.pos == self.goal:
                self.success = True
                done =True
            return self.next_state, self.reward , done

    def get_possible_actions(self, pos):

        actions = self.actions.copy()

        x, y = pos
        down  = x + 1
        up = x - 1
        left = y + 1
        right = y - 1
        x_end, y_end = self.pos_end

        if (left > y_end - 1):
            actions.remove("left")  
            actions.remove("left-down")
            actions.remove("left-up")
        if (right < 0):
            actions.remove("right")  
            actions.remove("right-down") 
            actions.remove("right-up")  
        if (up < 0):  
            actions.remove("up")
            if "left-up" in actions:actions.remove("left-up")
            if "right-up" in actions :actions.remove("right-up")
        if (down > x_end - 1):
            actions.remove("down") 
            if "left-down" in actions: actions.remove("left-down")
            if "right-down" in actions :actions.remove("right-down")

        return actions

    def action_sample(self):
        r_act = random.choice(self.get_possible_actions(self.pos))
        return self.actions.index(r_act)       
    

def main():
    maze = np.array([[0, 0, 0, 0, -1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0, 0],
            [0, 0, 0, 0, -1, 0, 1]])
       
    
    e = environment(maze,(1,0), (3, 6))
    x, y = maze.shape

    for _ in range(1000):
        action = e.action_sample()
        new_state, reward, done = e.step(action)


if __name__ == '__main__':
    main()    