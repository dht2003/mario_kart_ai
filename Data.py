import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision.utils import make_grid
import torch
import torchvision
import math

CONTROLLER_STATE_END_COL = 13


class MKDataSet(Dataset):
    def __init__(self, root_dir, transform=None):
        if not os.path.exists(root_dir):
            raise IOError("[MKDataSet] Cannot find root dir")
        self.transform = transform
        self.root_dir = root_dir
        train_dirs_names = os.listdir(root_dir)
        train_dirs = []
        for name in train_dirs_names:
            train_dirs.append(os.path.join(root_dir, name))
        self.datafiles = []
        for train_dir in train_dirs:
            if os.path.exists(os.path.join(train_dir, "data.csv")):
                self.datafiles.append(os.path.join(train_dir, "data.csv"))
        self.x = None
        self.y = None

        for datafile in self.datafiles:
            x = np.genfromtxt(datafile, delimiter=',', encoding='utf8', usecols=0, dtype=str)
            y = np.genfromtxt(datafile, delimiter=',', encoding='utf8',
                              usecols=range(1, CONTROLLER_STATE_END_COL),
                              dtype=np.float32)  # TODO: Improve this line
            if self.x is None:
                self.x = x
            else:
                self.x = np.append(self.x, x, axis=0)
            if self.y is None:
                self.y = y
            else:
                self.y = np.append(self.y, y, axis=0)
            self.n_samples = self.y.shape[0]

    def load_image(self, index):
        img_path = self.x[index]
        if not os.path.exists(img_path):
            raise IOError("[MKDataSet] Cannot find path to image")
        img = Image.open(img_path)
        if self.transform:
            img = self.transform(img)
        return img

    def __getitem__(self, index):
        img = self.load_image(index)
        controller_state = torch.from_numpy(self.y[index])
        return img, controller_state

    def __len__(self):
        return self.n_samples


def show_batch(dl):
    for images, labels in dl:
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(make_grid(images, nrow=16).permute(1, 2, 0))
        plt.show()
        break


