import os.path

import matplotlib.pyplot as plt
import torch


class Trainer:
    def __init__(self, model, device, optimizer, criterion, trainloader, validationloader, save_dir="./"):
        self.model = model
        self.device = device
        self.model.to(device)
        self.start_epoch = 0
        self.optimizer = optimizer
        self.criterion = criterion
        self.trainloader = trainloader
        self.validationloader = validationloader
        self.log_interval = 10
        self.batch_size = trainloader.batch_size
        self.train_losses = []
        self.train_counter = []
        self.save_dir = save_dir

    def train(self, epochs):
        for epoch in range(self.start_epoch, epochs + self.start_epoch):
            print(f"Started epoch {epoch}")
            print("Training Start")
            self.model.train()
            train_loss = 0.0
            valid_loss = 0.0
            for batch_idx, (data, target) in enumerate(self.trainloader):
                data, target = data.to(self.device), target.to(self.device)
                self.optimizer.zero_grad()
                output = self.model(data)
                loss = self.criterion(output, target)
                loss.backward()
                self.optimizer.step()
                train_loss += loss.item()

                if batch_idx % self.log_interval == 0:
                    loss_val = train_loss / (batch_idx + 1)
                    print(f"Training Epoch: {epoch} | Loss: {loss_val}")
                    self.train_losses.append(loss_val)
                    self.train_counter.append(
                        (batch_idx * self.batch_size) + (epoch * len(self.trainloader.dataset)))
            print("Train End")
            self.save(epoch)
            print("Valid Start")
            with torch.no_grad():
                self.model.eval()
                for batch_idx, (data, target) in enumerate(self.validationloader):
                    data, target = data.to(self.device), target.to(self.device)
                    output = self.model(data)
                    loss = self.criterion(output, target)
                    valid_loss += loss.item()
                    if batch_idx % self.log_interval == 0:
                        loss_val = valid_loss / (batch_idx + 1)
                        print(f"Training Epoch: {epoch} | Loss: {loss}")
            print("Valid End\n")

    def plot_train_loss(self):
        fig = plt.figure()
        plt.plot(self.train_counter, self.train_losses, color='blue')
        plt.legend(['Train Loss', 'Test Loss'], loc='upper right')
        plt.xlabel('number of training examples seen')
        plt.ylabel('mean squared error loss')
        return fig

    def save(self, epoch):
        state = {"epoch": epoch + 1,
                 "model_state_dict": self.model.state_dict(),
                 "optimizer_state_dict": self.optimizer.state_dict(),
                 "train_losses": self.train_losses,
                 "train_counter": self.train_counter}
        print("Saving Checkpoint")
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        checkpoint_filename = f"mario-kart-model-{epoch}.pt"
        checkpoint_path = os.path.join(self.save_dir, checkpoint_filename)
        torch.save(state, checkpoint_path)

    def load(self, checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        self.start_epoch = checkpoint["epoch"]
        self.train_losses = checkpoint["train_losses"]
        self.train_counter = checkpoint["train_counter"]
