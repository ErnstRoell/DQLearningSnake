import pygame
import numpy as np
import pprint as pp
import configuration as cf
import random
import time 

random.seed(1993)
np.random.seed(1)

class SnakeEnv:
    def __init__(self):
        # Load Configs 
        self.state = []
        self.exit = False
        self.direction = "Up"
        self.reset()
        self.initGraphics()
        self.collision_flags={
                "apple": False,
                "wall": False,
                "snake": False
                }
        self.rewards={
                "apple": 100,
                "wall": -100,
                "snake": -100
                }


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
        self.detect_collisions()

        
        # Spawn new apple if agent hit apple.
        if self.collision_flags['apple']:
            self.apple = np.random.randint([0,0],[cf.width,cf.height],(2,))
            self.collision_flags['apple'] = False

        # Update the state variable (Snakes "Observation" of the world)
        self.update_state()


        self.update_reward()
        
        return self.state, self.reward, self.exit
    
    def update_reward(self):
        """
        Calculates the reward based on the current state of the game.
        """

        for key in self.collision_flags.keys():
            if self.collision_flags[key] and self.reward == 0:
                selfreward = self.rewards[key]
            elif self.collision_flags[key] and reward != 0:
                raise ValueError('Reward was nonzero and multiple collisions detected!')
            else:
                self.reward = 0  

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

    def detect_collisions(self):
        """
        Detects collision of either snake with itself, with edge of board or
        with the apple.
        """
        # Detect collision with edge of board
        if not cf.width-1 > self.snakeBody[-1][0] > -1 or not cf.height-1 > self.snakeBody[-1][1] > -1:
            self.exit = True
            self.collision_flags['wall']=True
        # Detect collision with snake itself
        if self.snakeBody[-1] in self.snakeBody[:-1]:
            self.exit = True 
            self.collision_flags['snake']=True
        
        # Detect if snakehead is on the apple ie it reached goal.
        if np.all(self.apple == self.snakeBody[-1]):
            self.collision_flags['apple']=True

    def reset(self):
        '''
        Resets the game to its initial state, so a new simulation can be run.
        '''
        # Start position + snakeStart
        self.snakeBody = []
        self.ticker = 1
        self.reward = 0
        self.score = 0
        self.snakeBody = []
        self.collision_flags={
                "apple": False,
                "wall": False,
                "snake": False
                }

        # Spawn Apple
        self.apple = np.random.randint([0,0],[cf.width,cf.height],(2,))
        # Spawn Snake
        self.snakeBody.append(np.random.randint([0,0],[cf.width,cf.height],(2,)))
        # Update State
        self.update_state()


    def initGraphics(self):
        self.clock = pygame.time.Clock()
        # pygame.init()
        self.gameDisplay = pygame.display.set_mode((10*cf.display_width,
                                                    10*cf.display_height))
        pygame.display.set_caption('Slither')

    def render(self):
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
    def __init__(self, bot):
        self.bot = bot
        # Load Agent Configs 
        # Load 

    def choose_action(self, state):
        """
        Given the state of the game, return an action 

        Input:
        State - What the player "observes" in this step.
        
        Output:
        Action - the action that the player takes given the state
        """
        
        return 2

class AutoBotAgent():
    def __init__(self):
        self.prev_state = None 
        self.direction = 0
        
    def choose_action(self,state):
        """
        Has some shitty logic, but makes an interesting bot.
        Depends on starting facing in the up direction.
        """
        snake_x,snake_y,apple_x,apple_y = state
        print(state, self.direction)
        action = 0

        if (snake_y-apple_y) < 0:
            print("Go Down")
            if not self.direction == 2:
                self.direction = (self.direction - 1) % 4
                action = 1 # Turn left
        elif (snake_y-apple_y) > 0:
            print("Go Up")
            if not self.direction == 0:
                self.direction = (self.direction - 1) % 4
                action = 1 # Turn left
        elif (snake_x-apple_x) < 0 and snake_y==apple_y:
            print("Left/Right")
            if self.direction == 2:
                self.direction = (self.direction - 1) % 4
                action = 1 # Turn left
            elif self.direction == 0:
                self.direction = (self.direction + 1) % 4
                action = 2 # Turn Right
        elif (snake_x-apple_x) > 0 and snake_y==apple_y:
            print('Left/Right')
            if self.direction == 2:
                self.direction = (self.direction + 1) % 4
                action = 2 # Turn left
            if self.direction == 0:
                self.direction = (self.direction - 1) % 4
                action = 1 # Turn left
        return action

class GameEngine():
    """ 
    This class will be implemented to automatically run the game with a
    particular agent and configurations. 
    """

    def __init__(self, env, agent):
        if env=="Snake":
            self.env=SnakeEnv()
        self.agent=agent

    def run(self):
        ticker = 1
        while not self.env.exit and ticker <300:
            action = self.agent.choose_action(self.env.state)
            self.env.step(action)
            self.env.render()
            time.sleep(.05)
            ticker += 1

if __name__ == "__main__":
    agent = AutoBotAgent()
    game = GameEngine("Snake", agent)
    game.run()
