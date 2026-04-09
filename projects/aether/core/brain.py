import torch
import torch.nn as nn
import torch.nn.functional as F

class RobotBrain(nn.Module):
    """
    A neural network brain for a humanoid robot.
    Uses PReLU activation as requested.
    """
    def __init__(self, input_size=8, hidden_size=24, output_size=6):
        super(RobotBrain, self).__init__()
        # Input: [survival, profit, task, health, role_scaled, balance_scaled, 0, 0] (3D)
        # Input: [survival, profit, task, health, role_scaled, balance_scaled] (2D)
        # Output: [charging, selling, tasking, scavenging, idle, maintenance]
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.prelu1 = nn.PReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.prelu2 = nn.PReLU()
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.prelu1(x)
        x = self.fc2(x)
        x = self.prelu2(x)
        x = self.fc3(x)
        return x

    def decide(self, state_tensor):
        """Returns the index of the highest value output."""
        with torch.no_grad():
            output = self.forward(state_tensor)
            return output
