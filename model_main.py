from model import Model
from Data import MKDataSet, show_batch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from model import Model
from train import Trainer
import matplotlib.pyplot as plt


lr = 1e-4
weight_decay = 1e-5
batch_size = 512
num_workers = 4


def main():
    model = Model()
    data = MKDataSet("D:/dev/mario_kart_ai/samples",
                     transform=transforms.Compose([
                         transforms.ToTensor()]))
    trainloader = DataLoader(data, batch_size=128, num_workers=4)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    trainer = Trainer(model, device, 1, optimizer, criterion, trainloader, None)
    trainer.train()
    f = trainer.plot_train_loss()
    plt.show()


if __name__ == "__main__":
    main()
