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
        if len(self.memory) >= 512:
            batch = random.sample(self.memory, 512)
        else:
            batch = self.memory
        target = []

        states, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(np.array(states), dtype=torch.float)  # ok
        next_states = torch.tensor(np.array(next_states), dtype=torch.float)  # ok
        rewards = torch.tensor(np.array(rewards)[:, None], dtype=torch.float)  # ok

        predictions = self.model(states)

        self.model.eval()

        next_prediction = self.model(next_states)

        for reward, done, prediction in zip(rewards, dones, next_prediction):
            if done:
                target.append(reward)
            else:
                target.append(reward + self.gamma * prediction)

        self.model.train()

        target = torch.stack(target)

        self.optimizer.zero_grad()
        loss = self.criterion(target, predictions)
        loss.backward()
        self.optimizer.step()

    def decide_next_state(self, states):
        max_prediction = None
        next_state = None

        if random.random() < self.epsilon:
            next_state = random.choice(list(states))
        else:
            for state in states:
                value = self.model(states[state])
                if not max_prediction or value > max_prediction:
                    max_prediction = value
                    next_state = state

        return next_state
