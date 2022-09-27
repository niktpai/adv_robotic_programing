"""
MTRE 6100: ASSIGNMENT 5
Authors:  Devin Grace, Nikhil Pai
"""


import numpy as np
import matplotlib.pyplot as plt

class robotBase():

    def __init__(self):

        self.hallway = ['P0','P1','P2','P3']
        self.reset()
        
        self.transitionProbs(0.7, 0.2, 0.1) 
        self.sensorProbs(0.3, 0.8, 0.7, 0.2)


    def reset(self):
        self.belief_bar = 0.25 * np.ones(len(self.hallway))
        self.belief = 0.25 * np.ones(len(self.hallway))
        self.step = 0


    def transitionProbs(self, moves, stays, moves_2 = 0):
        self.prob_moves = moves
        self.prob_stays = stays
        self.prob_moves_2 = moves_2

    def sensorProbs(self, door_wall = 0, door_door = 0 , wall_wall = 0, wall_door = 0):
        self.prob_door_wall = door_wall
        self.prob_door_door = door_door

        self.prob_wall_wall = wall_wall
        self.prob_wall_door = wall_door

    def calcBelBar(self):
        '''
        Function that calculates the current belief bar / motion update
        '''
        # bel_bar = np.zeros(shape=belief.shape, dtype = "float64")
        for n in range(self.belief.shape[0]):
            if n == 0:
                self.belief_bar[n] = self.prob_stays *self.belief[n]
            elif n == 1:
                self.belief_bar[n] = self.prob_moves * self.belief[n-1] + self.prob_stays * self.belief[n]
            else:
                self.belief_bar[n] = self.prob_moves_2 * self.belief[n-2] + self.prob_moves * self.belief[n-1] + self.prob_stays *self.belief[n]
        

    def calcBel(self, prob1, prob2):
        '''
        Function that calculates the current belief bar / measurement update
        '''
        # bel = np.zeros(shape=belief_bar.shape, dtype = "float64")
        for n in range(self.belief_bar.shape[0]):
            if n%2 == 0:
                self.belief[n] = prob1 *self.belief_bar[n]
                
            elif n%2 ==1:
                self.belief[n] = prob2 *self.belief_bar[n]
        n = 1/sum(self.belief)        
        self.belief = self.belief * n

    def takeStep(self, sensor_assumption):
        """
        this will be called when control == 1
        """
        self.step += 1
        self.calcBelBar()
        if sensor_assumption == 'd':
            self.calcBel(self.prob_door_wall,self.prob_door_door)
        if sensor_assumption == 'w':
            self.calcBel(self.prob_wall_wall,self.prob_wall_door)
        

    def dispBeliefs(self):
        """
        this will be called to display the belief and belief bar graphs on the same figure
        """
        print(f'Belief bar:  {self.belief_bar}')
        print(f'Belief :  {self.belief}')
        fig,axes = plt.subplots(1,2 )

        axes[0].bar(self.hallway, self.belief_bar)
        axes[0].set_xlabel('Belief Bar')

        axes[1].bar(self.hallway, self.belief)
        axes[1].set_xlabel('Belief')

        fig.suptitle(f'Step {self.step} Belief bar and Belief Graphs')

        plt.draw()
        plt.pause(1)
        input("<Hit Enter To Exit Graph>")
        plt.close(fig)


    def stepAndDispBelief(self, sensor_input ):
        self.takeStep(sensor_input)
        self.dispBeliefs()

    def play(self):
        key = '0'
        while (key != 'q'):
            key = input(f"Press [1] to take step or [q] to quit or [r] to reset \n")
            if key == '1':
                assumption = input (f"What is sensor input? [d] for door or [w] for wall \n")
                self.stepAndDispBelief(assumption)
                key = '0'
            elif key =='r':
                self.reset()
                key = '0'
            elif key =='q':
                pass
            else:
                print("Input character not recognized!! Try again please.")

class robot2(robotBase):
    def __init__(self):
        super().__init__()

        self.transitionProbs(0.6, 0.2, 0.2) 
        self.sensorProbs(0.15, 0.85, 0.6, 0.4)

def main():
    robby_1 = robotBase()
    print("Controlling robot 1")
    robby_1.play()
    
    robby_2 = robotBase()
    print("Controlling robot 2")
    robby_2.play()


if __name__ == "__main__":
    main()
