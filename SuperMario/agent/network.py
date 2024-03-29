import torch
import torch.nn as nn


class DeepConvQNetwork(nn.Module):
    """
    Deep Convolutional Q-Network for reinforcement learning.

    This neural network is designed for use in deep reinforcement learning scenarios,
    particularly with environments that have image-based state representations.

    Args:
        input_dim (tuple): Input dimensions representing the shape of the state space.
        output_dim (int): Number of output nodes representing the Q-values for different actions.

    Attributes:
        input_dim (tuple): Input dimensions of the state space.
        output_dim (int): Number of output nodes representing Q-values.
        fc_input_dim (int): Size of the feature vector produced by the convolutional layers.
        conv (nn.Sequential): Convolutional layers of the neural network.
        network (nn.Sequential): regular layers of the neural network.

    Methods:
        forward(state): Performs a forward pass through the neural network.
        feature_size(): Calculates the size of the feature vector produced by the convolutional layer.
    """
    def __init__(self, input_dim, output_dim):
        super(DeepConvQNetwork, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim

        self.conv = nn.Sequential(
            nn.Conv2d(input_dim[0], 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU()
        )

        self.fc_input_dim = self.feature_size()

        self.network = nn.Sequential(
            self.conv,
            nn.Flatten(),
            nn.Linear(self.fc_input_dim, 512),
            nn.ReLU(),
            nn.Linear(512, self.output_dim)
        )
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.to(self.device)

    def forward(self, state):
        """
        Forward pass through the neural network.

        Args:
            state (torch.Tensor): Input state, typically an image or a tensor representing the environment state.

        Returns:
            torch.Tensor: Output Q-values predicted by the neural network for different actions.
        """
        #features = self.conv(state)
        #features = features.view(features.size(0), -1)
        #qvals = self.network(features)
        state = state.to(self.device)
        qvals = self.network(state)
        
        return qvals
    
    def feature_size(self):
        """
        Calculate the size of the feature vector produced by the convolutional layer.

        This method initializes a tensor filled with zeros and passes it through the convolutional layer,
        then computes the size of the resulting feature vector. The size is crucial for determining
        the input dimension of subsequent layers in a neural network.

        Returns:
            int: Size of the feature vector produced by the convolutional layer.
        """
        return self.conv(torch.autograd.Variable(torch.zeros(1, *self.input_dim))).view(1, -1).size(1)
    

class DuelingDeepConvQNetwork(nn.Module):
    """
    Dueling Deep Convolutional Q-Network for reinforcement learning.

    This neural network is designed for use in deep reinforcement learning scenarios,
    particularly with environments that have image-based state representations.
    The dueling architecture decomposes Q-values into state values and advantages.

    Args:
        input_dim (tuple): Input dimensions representing the shape of the state space.
        output_dim (int): Number of output nodes representing the Q-values for different actions.

    Attributes:
        input_dim (tuple): Input dimensions of the state space.
        output_dim (int): Number of output nodes representing Q-values.
        fc_input_dim (int): Size of the feature vector produced by the convolutional layers.
        conv (nn.Sequential): Convolutional layers of the neural network.
        value_stream (nn.Sequential): Stream for estimating state values.
        advantage_stream (nn.Sequential): Stream for estimating advantages.

    Methods:
        forward(state): Performs a forward pass through the dueling deep Q-network.
        feature_size(): Calculates the size of the feature vector produced by the convolutional layer.
    """
    def __init__(self, input_dim, output_dim):
        super(DuelingDeepConvQNetwork, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim

        self.conv = nn.Sequential(
            nn.Conv2d(input_dim[0], 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU()
        )

        self.fc_input_dim = self.feature_size()

        # Value Stream.
        self.value_stream = nn.Sequential(
            nn.Linear(self.fc_input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )
        # Advantage Stream.
        self.advantage_stream = nn.Sequential(
            nn.Linear(self.fc_input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, self.output_dim)
        )

    def forward(self, state):
        """
        Perform a forward pass through the dueling deep Q-network.

        Args:
            state (torch.Tensor): Input state, typically an image or a tensor representing the environment state.

        Returns:
            torch.Tensor: Output Q-values computed using the dueling architecture.
                        The Q-values are decomposed into state values and advantages.
        """
        features = self.conv(state)
        features = features.view(features.size(0), -1)
        values = self.value_stream(features)
        advantages = self.advantage_stream(features)
        qvals = values + (advantages - advantages.mean())
        
        return qvals
    
    def feature_size(self):
        """
        Calculate the size of the feature vector produced by the convolutional layer.

        This method initializes a tensor filled with zeros and passes it through the convolutional layer,
        then computes the size of the resulting feature vector. The size is crucial for determining
        the input dimension of subsequent layers in a neural network.

        Returns:
            int: Size of the feature vector produced by the convolutional layer.
        """
        return self.conv(torch.autograd.Variable(torch.zeros(1, *self.input_dim))).view(1, -1).size(1)