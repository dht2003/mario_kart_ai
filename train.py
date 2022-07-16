import os.path

import matplotlib.pyplot as plt
import torch


class Trainer:
    def __init__(self, model, device, optimizer, scheduler, criterion, trainloader, validationloader, save_dir="./"):
        self.model = model
        self.device = device
        self.model.to(device)
        self.start_epoch = 0
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = criterion
        self.trainloader = trainloader
        self.validationloader = validationloader
        self.log_interval = 10
        self.batch_size = trainloader.batch_size
        self.history = []
        self.epoch_counter = []
        self.save_dir = save_dir

    def train(self, epochs):
        for epoch in range(self.start_epoch, epochs + self.start_epoch):
            self.model.train()
            epoch_train_loss = 0.0
            train_running_loss = 0.0
            epoch_valid_loss = 0.0
            for batch_idx, (data, target) in enumerate(self.trainloader):
                data, target = data.to(self.device), target.to(self.device)
                self.optimizer.zero_grad()
                output = self.model(data)
                loss = self.criterion(output, target)
                loss.backward()
                self.optimizer.step()
                epoch_train_loss += loss.item() * output.size(0)
                train_running_loss += loss.item()
                if batch_idx % self.log_interval == 0:
                    loss_val = train_running_loss / self.log_interval
                    print(f"[Training Epoch: {epoch},Batch: {batch_idx}] | Loss: {loss_val}")
                    train_running_loss = 0.0
            with torch.no_grad():
                self.model.eval()
                for batch_idx, (data, target) in enumerate(self.validationloader):
                    data, target = data.to(self.device), target.to(self.device)
                    output = self.model(data)
                    loss = self.criterion(output, target)
                    epoch_valid_loss += loss.item() * output.size(0)
            epoch_train_loss_val = epoch_train_loss / len(self.trainloader.dataset)
            epoch_valid_loss_val = epoch_valid_loss / len(self.validationloader.dataset)
            self.scheduler.step()
            print(f"Epoch {epoch}: \tTraining Loss: {epoch_train_loss_val} |\tValidation Loss: {epoch_valid_loss_val}")
            self.history.append([epoch_train_loss_val, epoch_valid_loss_val])
            self.epoch_counter.append(epoch)
            self.save(epoch)

    def plot_train_loss(self):
        fig = plt.figure()
        train_losses = [i[0] for i in self.history]
        valid_losses = [i[1] for i in self.history]
        plt.plot(self.epoch_counter, train_losses, label="Train Loss")
        plt.plot(self.epoch_counter, valid_losses, label="Validation Loss")
        plt.legend()
        plt.xlabel('Epochs')
        plt.ylabel('Mse + Bce Loss')
        return fig

    def save(self, epoch):
        state = {"epoch": epoch + 1,
                 "model_state_dict": self.model.state_dict(),
                 "optimizer_state_dict": self.optimizer.state_dict(),
                 "history": self.history,
                 "epoch_counter": self.epoch_counter,
                 'scheduler': self.scheduler.state_dict()}
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
        self.history = checkpoint["history"]
        self.epoch_counter = checkpoint["epoch_counter"]
        self.scheduler.load_state_dict(checkpoint["scheduler"])
