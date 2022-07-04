import matplotlib.pyplot as plt


class Trainer:
    # TODO : Add checkpoint saver
    def __init__(self, model, device, epochs, optimizer, criterion, trainloader, validationloader):
        self.model = model
        self.device = device
        self.model.to(device)
        self.epochs = epochs
        self.optimizer = optimizer
        self.criterion = criterion
        self.trainloader = trainloader
        self.validationloader = validationloader
        self.log_interval = 10
        self.batch_size = trainloader.batch_size
        self.train_losses = []
        self.train_counter = []

    def train(self):
        for epoch in range(self.epochs):
            print(f"Started epoch {epoch}")
            print("Training Start")
            self.model.train()
            train_loss = 0.0
            for batch_idx, (data, target) in enumerate(self.trainloader):
                data, target = data.to(self.device), target.to(self.device)
                self.optimizer.zero_grad()
                output = self.model(data)
                loss = self.criterion(output, target)
                loss.backward()
                self.optimizer.step()
                train_loss += loss.item()

                if batch_idx % self.log_interval == 0:
                    print("Training Epoch: {} | Loss: {}".format(epoch, train_loss / (batch_idx + 1)))
                    self.train_losses.append(loss.item())
                    self.train_counter.append(
                        (batch_idx * self.batch_size) + ((epoch + 1) * len(self.trainloader.dataset)))
        print("Train End")

    def plot_train_loss(self):
        fig = plt.figure()
        plt.plot(self.train_counter, self.train_losses, color='blue')
        plt.legend(['Train Loss', 'Test Loss'], loc='upper right')
        plt.xlabel('number of training examples seen')
        plt.ylabel('negative log likelihood loss')
        return fig
