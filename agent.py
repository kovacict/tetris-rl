from dqn import DQN
import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 1
        self.epsilon_decrement = 5e-4
        self.epsilon_final = 1e-3
        self.gamma = 0.9
        self.memory = deque(maxlen=100000)
        self.model = DQN()
        self.lr = 0.001
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def remember(self, state, reward, next_state, done):
        self.memory.append([state, reward, next_state, done])

    def reduce_epsilon(self):
        self.epsilon = self.epsilon - self.epsilon_decrement
        if self.epsilon <= self.epsilon_final:
            self.epsilon = self.epsilon_final

    def train(self):
        #if self.n_games<256:
            #return
        if len(self.memory) >= 512 :
            batch = random.sample(self.memory, 512)
        else:
            batch = self.memory

        state, reward, next_state, done = zip(*batch)

        #state = torch.tensor(np.array(state), dtype=torch.float)
        #next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        #reward = torch.tensor(np.array(reward), dtype=torch.float)

        state=torch.stack(tuple(s for s in state))
        #state=state.to(torch.float32)
        reward=torch.from_numpy(np.array(reward, dtype=np.float32)[:,None])
        next_state=torch.stack(tuple(next_s for next_s in next_state))
        #next_state=next_state.to(torch.float32)

        prediction = self.model(state)

        self.model.eval()

        next_prediction = self.model(next_state)

        self.model.train()
        target = torch.cat(
            tuple(
                reward if done else reward + self.gamma * prediction
                for reward, done, prediction in zip(reward, done, next_prediction)
            )
        )[:, None]
        
        
        self.optimizer.zero_grad()
        loss=self.criterion(target,prediction)
        loss.backward()
        self.optimizer.step()

    def decide_next_state(self, states):
        max_prediction=None
        next_state=None

        if random.random()<self.epsilon:
            next_state=random.choice(list(states))
        else:
            for state in states:
                value=self.model(states[state])
                if not max_prediction or value > max_prediction:
                    max_prediction=value
                    next_state=state

        return next_state