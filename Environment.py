import pygame
import numpy as np
import pprint as pp
import configuration as cf
import random
import time 

class Snake:
    def __init__(self):
        # Load Configs 
        self.state = []
        self.exit = False
        self.direction = "Up"
        self.reset()
        self.initGraphics()

    def step(self,action):
        '''
        Updates the game state after performing the action of the player.

        Input:
        Action - Action that the player takes.
        '''
        # Internal counter for maximum number of iterations
        if self.ticker == cf.maxIt: 
            self.exit = True
        self.ticker += 1

        # Convert action to directional change of snake head
        change = self.compute_change(action)

        # Add the new snake head position 
        self.snakeBody.append(self.snakeBody[-1]+change)

        # Remove the last element of the tail
        self.snakeBody.pop(0)

        # Detect collision with itself or edge of board.
        self.detect_collision()

        # Update the state variable (Snakes "Observation" of the world)
        self.update_state()

        # Detect if snakehead is on the apple ie it reached goal.
        if np.all(self.apple == self.snakeBody[-1]):
            # Spawn new apple
            self.apple = np.random.randint([0,0],[cf.width,cf.height],(2,))
            self.score += 10

    def update_state(self):
        """
        This is what the snake "observes"
        1) Position of the snake head
        2) Position of the apple
        """
        self.state = [*self.snakeBody[-1],*self.apple]


    def compute_change(self,action):
        if self.direction=="Up":
            if action==0: # Do nothing and go straight.
                return np.array([0,-1])
            if action==1: # Move relative left.
                self.direction = "Left"
                return np.array([-1,0])
            if action==2: # Move relative right.
                self.direction = "Right"
                return np.array([1,0])

        if self.direction=="Down":
            if action==0: # Do nothing and go straight.
                self.direction = "Down"
                return np.array([0,1])
            if action==1: # Move relative left.
                self.direction = "Right"
                return np.array([1,0])
            if action==2: # Move relative right.
                self.direction = "Left"
                return np.array([-1,0])
       
        if self.direction=="Left":
            if action==0: # Do nothing and go straight.
                self.direction = "Left"
                return np.array([-1,0])
            if action==1: # Move relative left.
                self.direction = "Down"
                return np.array([0,1])
            if action==2: # Move relative right.
                self.direction = "Up"
                return np.array([0,-1])

        if self.direction=="Right":
            if action==0: # Do nothing and go straight.
                self.direction="Right"
                return np.array([1,0])
            if action==1: # Move relative left.
                self.direction="Up"
                return np.array([0,-1])
            if action==2: # Move relative right.
                self.direction="Down"
                return np.array([0,1])

    def detect_collision(self):
        """
        Detects collision of either snake with itself or with edge of board.
        
        """
        # Detect collision with edge of board
        if not cf.width-1 > self.snakeBody[-1][0] > 0 or not cf.height-1 > self.snakeBody[-1][1] > 0:
            self.exit = True
        # Detect collision with snake itself
        if self.snakeBody[-1] in self.snakeBody[:-1]:
            self.exit = True 

    def reset(self):
        '''
        Resets the game to its initial state, so a new simulation can be run.
        '''
        # Start position + snakeStart
        self.snakeBody = []
        self.ticker = 1
        self.score = 0
        self.snakeBody = []

        # Spawn Apple
        self.apple = np.random.randint([0,0],[cf.width,cf.height],(2,))
        # Spawn Snake
        self.snakeBody.append(np.random.randint([0,0],[cf.width,cf.height],(2,)))

    def initGraphics(self):
        self.clock = pygame.time.Clock()
        # pygame.init()
        self.gameDisplay = pygame.display.set_mode((10*cf.display_width,
                                                    10*cf.display_height))
        pygame.display.set_caption('Slither')

    def updateGraphics(self):
        self.gameDisplay.fill(cf.white)
        for coords in self.snakeBody:
            pygame.draw.rect(self.gameDisplay,
                            cf.green,
                            [10*coords[0],
                            10*coords[1],
                            10*cf.block_size,
                            10*cf.block_size])

        pygame.draw.rect(self.gameDisplay,
                            cf.red,
                            [10*self.apple[0],
                            10*self.apple[1],
                            10*cf.apple_size,
                            10*cf.apple_size])
        self.clock.tick(cf.speed)
        pygame.display.update()


class Agent:
    def __init__(self):
        # Load bot 
        # Load Agent Configs 
        # Load 
        pass

    def move(self, state):
        """
        Given the state of the game, return an action 

        Input:
        State - What the player "observes" in this step.
        
        Output:
        Action - the action that the player takes given the state
        """
        return 2

class GameEngine():
    def __init__(self, env, agent):
        if env=="Snake":
            self.env=Snake()
        self.agent=agent

    def run(self):
        while not self.env.exit:
            action = self.agent.move(self.env.state)
            self.env.step(action)
            self.env.updateGraphics()
            time.sleep(1)

if __name__ == "__main__":
    agent = Agent()
    game = GameEngine(env="Snake", agent=agent)
    game.run()