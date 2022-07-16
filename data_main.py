import torch

from Data import MKDataSet, show_batch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from model import NvidiaModel, custom_loss


def main():
    data = MKDataSet("D:/dev/mario_kart_ai/samples",
                     transform=transforms.Compose([transforms.ToTensor()]))
    f, c = data[0]
    model = NvidiaModel()
    loader = DataLoader(data, batch_size=128, num_workers=4)
    for i, (data, target) in enumerate(loader):
        #print(custom_loss(model(data), target))
        print(model(data))


if __name__ == "__main__":
    main()
