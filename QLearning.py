import json
from tqdm import tqdm
from Board import *
from collections import defaultdict
import imageio
import os
from copy import deepcopy
import logging

class QLearning():
    # Hyper paramaters
    lr = 0.01
    gamma = 0.95
    epsilon_range = (0.5,0.1)
    history = []
    
    # Paramètres interne
    max_iter = 10 # Nombre d'iteration maximale pour résoudre un Taquin
    
    def __init__(self):
        self.board = Board(500)
        self.q_matrix = defaultdict(lambda: {"haut": 0, "bas": 0, "gauche": 0, "droite": 0})
        
    def loadQmatrix(self,path_file):
        with open(path_file,'r',encoding = 'utf-8') as file:
            self.q_matrix = json.load(file)
        
    def saveQmatrix(self,path_file):
        q_matrix = {}
        for key, value in self.q_matrix.items():
            if value["haut"] != 0 or value["bas"] != 0 or value["gauche"] != 0 or value["droite"] != 0:
                q_matrix[key] = value
        with open(path_file,'w',encoding = 'utf-8') as file:
            json.dump(q_matrix,file)
        
    def q_value(self, state, action):
        try:
            return (self.q_matrix[state][action])
        except Exception as e:
            return(0)
            
    def max_q_value(self, state):
        max_q = -99999999

        for action in ["haut","bas","gauche","droite"]:
            q = self.q_value(state, action)
            if q > max_q:
                max_q = q
                best_action = action
            if max_q == 0:
                best_action = self.board.get_random_action()

        return max_q, best_action

    def epsilon_policy(self, epsilon):
        # Best move
        if random.uniform(0, 1) >= epsilon:
            max_q, action = self.max_q_value(self.board.get_state())
            return action
        # Random
        else:
            return self.board.get_random_action()
            
    def episode(self, epsilon):
        self.board.initialize()
        iter = 0
        
        history = []

        while not self.board.goal_achieved():
            action = self.epsilon_policy(epsilon)
            #print(self.board.board)
            old_state = self.board.get_state()
            #print(old_state)
            self.board.do_action(action)
            new_state = self.board.get_state()
            
            
            
            #print(new_state)
            #print("------------------------")
            max_q, best_action = self.max_q_value(new_state)
            reward = self.board.reward()
            history.append((old_state,new_state,action,reward))
            self.q_matrix[old_state][action] = reward + self.gamma * max_q

            if iter >= self.max_iter:
                self.board.initialize(100)
                iter = 0
                #logging.warning("Test")
                history = []
            else:
                iter += 1
        assert history != [], f"Erreur ! {history}"
        
        history = history[::-1]

        #logging.warning(len(history))
        #converged = False
        #while not converged:
        #    old_q_matrix = deepcopy(self.q_matrix)
        #    for (old_state,new_state,action,reward) in history:
        #        max_q, best_action = self.max_q_value(new_state)
        #        self.q_matrix[old_state][action] = reward + self.gamma * max_q
        #        #logging.warning((old_state,action,reward))
        #    break
            
        #    converged = self.converge(old_q_matrix)
                
        self.history += history
            
        # self.history = []
        
    def make_matrix_converge(self):
        converged = False
        while not converged:
            old_q_matrix = deepcopy(self.q_matrix)
            for (old_state,new_state,action,reward) in self.history:
                max_q, best_action = self.max_q_value(new_state)
                self.q_matrix[old_state][action] = reward + self.gamma * max_q
                #logging.warning((old_state,action,reward))
            break
            
            converged = self.converge(old_q_matrix)
        
    def converge(self,old_q_matrix):
        maxi = 0
        for key_1,value_1 in self.q_matrix.items():
            for key_2,value_2 in value_1.items():
                calc = abs(value_2 - old_q_matrix[key_1][key_2])
                #logging.warning(value_2)
                #logging.warning(old_q_matrix[key_1][key_2])
                #logging.warning(calc)  # will print a message to the console
                if calc > 0.01:
                    return(False)
                elif calc > maxi:
                    maxi = calc
        return(True)
            
    
    def learn_q(self, n):
        epsilons = np.linspace(self.epsilon_range[0], self.epsilon_range[1], num=n)

        for epsilon in tqdm(epsilons):
            self.episode(epsilon)

        #for i in range(20):
        #    print("Episode ", i + 1, "/", 20)
        #    self.episode(self.epsilon_range[1])
        #    print("Number iter :", self.evaluate())

    def run(self, max_iteration):
        self.board.initialize(max_iteration)
        self.board.image = 0
        print()
        print("Path :")
        self.board.show_board()

        while not self.board.goal_achieved():
            max_q, action = self.max_q_value(self.board.get_state())
            print("q value of best action:", max_q)
            print("best action:",action)
            self.board.do_action(action)
            self.board.show_board()

    def make_gif(self):
        # build gif
        with imageio.get_writer('taquin.gif', mode='I', duration=0.5) as writer:
            for i in range(1,self.board.image+1):
                image = imageio.imread(f"./Gif/{i}.png")
                writer.append_data(image)
        
        self.empty_gif_folder()

    def empty_gif_folder(self):
        for filename in os.listdir('./Gif'):
            if filename.endswith('.png'):
                os.remove('./Gif/' + filename)