import matplotlib.pyplot as plt
import torch


class Tester:
    def __init__(self, model, device, criterion, testloader):
        self.model = model
        self.device = device
        self.model.to(device)
        self.criterion = criterion
        self.testloader = testloader
        self.test_losses = []
        self.test_counter = []

    def test(self):
        self.model.eval()
        test_loss = 0
        with torch.no_grad:
            for batch_idx, (data, target) in self.testloader:
                output = self.model(data)
