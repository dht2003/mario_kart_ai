import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from matplotlib.figure import Figure

INPUT_CHANNELS = 3
OUTPUT_SHAPE = 12


class Model(nn.Module):
    def __init__(self, p=0.2):
        super(Model, self).__init__()
        self.p = p
        self.conv1 = nn.Conv2d(INPUT_CHANNELS, 24, kernel_size=(5, 5), stride=(2, 2))
        self.conv2 = nn.Conv2d(24, 36, kernel_size=(5, 5), stride=(2, 2))
        self.conv3 = nn.Conv2d(36, 48, kernel_size=(5, 5), stride=(2, 2))
        self.conv4 = nn.Conv2d(48, 64, kernel_size=(3, 3))
        self.conv5 = nn.Conv2d(64, 64, kernel_size=(3, 3))
        self.fc1 = nn.Linear(207936, 100)
        self.fc2 = nn.Linear(100, 50)
        self.fc3 = nn.Linear(50, 10)
        self.fc4 = nn.Linear(10, OUTPUT_SHAPE)
        self.dropout = nn.Dropout(p)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, self.p)
        x = F.relu(self.fc2(x))
        x = F.dropout(x, self.p)
        x = F.relu(self.fc3(x))
        x = F.dropout(x, self.p)
        x = F.relu(self.fc4(x))
        return x
