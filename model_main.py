from torchvision import transforms

from Data import MKDataSet, show_batch, data_loader
import torch
import torch.nn as nn
import torch.optim as optim
from model import Model
from train import Trainer
import matplotlib.pyplot as plt

lr = 1e-4
weight_decay = 1e-5
batch_size = 64
num_workers = 4
save_dir = "./results"


def main():
    model = Model()
    trainloader, validloader = data_loader("D:/dev/mario_kart_ai/samples", "D:/dev/mario_kart_ai/valid", batch_size,
                                           num_workers)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    trainer = Trainer(model, device, optimizer, criterion, trainloader, validloader, save_dir)
    trainer.load("results/mario-kart-model-0.pt")
    trainer.train(1)
    f = trainer.plot_train_loss()
    plt.show()


if __name__ == "__main__":
    main()
