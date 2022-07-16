import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models import resnet50

import torch.optim as optim
from matplotlib.figure import Figure

INPUT_CHANNELS = 3
OUTPUT_SHAPE = 12
SPLIT_POINT = 2


class NvidiaModel(nn.Module):
    def __init__(self, p=0.2):
        super(NvidiaModel, self).__init__()
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
        x = self.fc4(x)
        x = custom_activation(x)
        return x


class ResnetTransferModel(nn.Module):
    def __init__(self):
        super(ResnetTransferModel, self).__init__()
        self.resnet = resnet50(pretrained=True)
        freeze_parameters(self.resnet)
        self.resnet.fc = nn.Identity()
        self.fc1 = nn.Linear(2048, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 64)
        self.fc4 = nn.Linear(64, OUTPUT_SHAPE)

    def forward(self, x):
        x = self.resnet(x)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = custom_activation(self.fc4(x))
        return x


def freeze_parameters(model):
    for param in model.parameters():
        param.requires_grad = False


def custom_loss(output, target):
    first_output_slice = output[:, 0:SPLIT_POINT]
    second_output_slice = output[:, SPLIT_POINT:]
    first_target_slice = target[:, 0:SPLIT_POINT]
    second_target_slice = target[:, SPLIT_POINT:]
    first_criterion = nn.MSELoss()
    second_criterion = nn.BCELoss()
    first_slice_loss = first_criterion(first_output_slice, first_target_slice)
    second_slice_loss = second_criterion(second_output_slice, second_target_slice)
    loss = first_slice_loss + second_slice_loss
    return loss


def custom_activation(x):
    first_slice = x[:, 0:SPLIT_POINT]
    second_slice = x[:, SPLIT_POINT:]
    tuple_of_activated_parts = (
        F.softsign(first_slice),
        torch.sigmoid(second_slice)
    )
    x = torch.cat(tuple_of_activated_parts, dim=1)
    return x
