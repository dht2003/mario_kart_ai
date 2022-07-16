from torchvision import transforms
from torch.optim.lr_scheduler import MultiStepLR
from Data import MKDataSet, show_batch, data_loader
import torch
import torch.nn as nn
import torch.optim as optim
from model import NvidiaModel, ResnetTransferModel, custom_loss
from train import Trainer
import matplotlib.pyplot as plt

lr = 1e-4
weight_decay = 1e-5
batch_size = 64
num_workers = 4
epochs = 100
milestones = [30, 65]
gamma = 0.1
save_dir = "./results"


def main():
    model = ResnetTransferModel()
    trainloader, validloader = data_loader("D:/dev/mario_kart_ai/samples", "D:/dev/mario_kart_ai/valid", batch_size,
                                           num_workers)
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = MultiStepLR(optimizer, milestones=milestones, gamma=gamma)
    criterion = custom_loss
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    trainer = Trainer(model, device, optimizer, scheduler, criterion, trainloader, validloader, save_dir)
    # trainer.load("results/mario-kart-model-2.pt")
    trainer.train(epochs)
    f = trainer.plot_train_loss()
    plt.show()


if __name__ == "__main__":
    main()
