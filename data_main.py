from Data import MKDataSet, show_batch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils


def main():
    data = MKDataSet("D:/dev/mario_kart_ai/samples",
                     transform=transforms.Compose([transforms.ToTensor()]))
    f , c = data[0]
    loader = DataLoader(data, batch_size=192, num_workers=4)


if __name__ == "__main__":
    main()
