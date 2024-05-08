import torch
import torch.nn as nn
import torch.nn.functional as F
import os

class DQN(nn.Module):
    def __init__(self, input_layer_size=4, hidden_layer1_size=64, hidden_layer2_size=64, output_size=1):
        super().__init__()
        self.l1=nn.Linear(input_layer_size, hidden_layer1_size)
        self.l2=nn.Linear(hidden_layer1_size, hidden_layer2_size)
        self.l3=nn.Linear(hidden_layer2_size,output_size)

    def set_weight(self):
        for module in self.modules():
            if isinstance(module,nn.Linear):
                nn.init.kaiming_uniform_(module.weight, mode="fan_in", nonlinearity="relu")
                nn.init.zeros_(module.bias)

    def forward(self, x):
        x=F.relu(self.l1(x))
        x=F.relu(self.l2(x))
        x=self.l3(x)
        return x
    
    def save(self, file_name="model1.pth"):
        model_folder_path="./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name=os.path.join(model_folder_path,file_name)
        torch.save(self.state_dict(), file_name)