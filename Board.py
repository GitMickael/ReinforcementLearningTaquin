import numpy as np
import matplotlib.pyplot as plt
import random
import pickle
from celluloid import Camera

class Board:
    # Hyper paramaters
    goal_reward = 200
    image = 0
    
    def __init__(self, max_iteration = 50):
        self.max_iteration = max_iteration
        self.final = np.array([k for k in range(1,9)]+[0]).reshape(3, 3)
        self.initialize(max_iteration)
        
    

    def initialize(self, max_iteration = 50):
        self.board = np.array([k for k in range(1,9)]+[0]).reshape(3, 3)
        while self.goal_achieved():
            for i in range(max_iteration):
                action = self.get_random_action()
                self.do_action(action)
    
    def get_state(self):
        return str(tuple(map(tuple, self.board)))
    
    def show_board(self):
        #=====================#
        # Graphics parameters #
        #=====================#
        size = 4
        line_color = "black"
        text_color = "red"
        text_size = size * 12
        line_width = 1.5
        text_params = {
            'ha': 'center',
            'va': 'center',
            'family': 'sans-serif',
            'fontweight': 'bold'
        }

        #=================================#
        # Plot creation and configuration #
        #=================================#
        # Objects init
        fig, ax = plt.subplots()
        
        # Window limits
        plt.xlim(0, 3)
        plt.ylim(0,3)
        
        # Hide graduations on axes
        plt.xticks([])
        plt.yticks([])
        
        # Borders colors and width  
        [i.set_color(line_color) for i in ax.spines.values()]
        [x.set_linewidth(line_width) for x in ax.spines.values()]
        
        # Visual size of windows
        plt.gcf().set_size_inches(size, size)

        # Draw lines to make grid
                     
        plt.axvline(x=1, color= line_color, lw = 1.5)
        plt.axvline(x=2, color= line_color, lw = 1.5)
        plt.axhline(y=1, color= line_color, lw = 1.5)
        plt.axhline(y=2, color= line_color, lw = 1.5)
    
        # Draw numbers in 
        index = 0
        for x,j in enumerate(np.arange(2.5,-0.5,-1)):
            for y,i in enumerate(np.arange(0.5,3.5,1)):
                if self.board[x][y] != 0:
                    plt.text(i, j, str(self.board[x][y]), color= text_color, **text_params,size = text_size)
                index += 1

            # plt.plot()
            # camera.snap()



        #plot_array([k for k in range(0,9)])

        #for i in range(10):
        #    l = [k for k in range(9)]
        #    random.shuffle(l)
        #    plot_array(l)
        #animation = camera.animate(interval = 600, repeat = False)
        #animation.save('taquin.gif', writer = 'imagemagick')7
        self.image += 1
        plt.savefig(f"./Gif/{self.image}.png")
        plt.show()

    def get_possibles_actions(self):
        actions = ["haut","bas","gauche","droite"]
        
        i,j = self.get_empty_cell()
        
        if i == 0:
            actions.remove("haut")
        elif i == 2:
            actions.remove("bas")
        
        if j == 0:
            actions.remove("gauche")
        elif j == 2:
            actions.remove("droite")
            
        return(actions)
    
    def get_random_action(self):
        actions = self.get_possibles_actions()
        random.shuffle(actions)
        return(actions[0])
    
    
    def do_action(self, action):
        i, j = self.get_empty_cell()

        if action == "haut":
            self.board[i][j] = self.board[i - 1][j]
            self.board[i - 1][j] = 0

        elif action == "bas":
            self.board[i][j] = self.board[i + 1][j]
            self.board[i + 1][j] = 0

        elif action == "droite":
            self.board[i][j] = self.board[i][j + 1]
            self.board[i][j + 1] = 0

        elif action == "gauche":
            self.board[i][j] = self.board[i][j - 1]
            self.board[i][j - 1] = 0

    def get_empty_cell(self):
        
        i,j = np.where(self.board == 0)[0][0], np.where(self.board == 0)[1][0]
        
        return(i,j)
    
    def goal_achieved(self):
        return np.array_equal(self.board, self.final)
    
    def reward(self):
        if self.goal_achieved():
            return (self.goal_reward)
        else:
            return (0)
