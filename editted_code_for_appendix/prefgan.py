#Converted from IPython Notebook to .py file for inclusion in thesis

import numpy as np

import torch
from torch import nn, optim
from torch.autograd.variable import Variable
from torchvision import transforms, datasets

import graph_visualize as gv

import tqdm
from tqdm import tqdm_notebook

# A note on loggingutils
# I did not write loggingutils, it was written by Diego Gomex Mosquera
# His blog post titled 'GANs from Scratch 1: A deep introduction. 
# With code in PyTorch and TensorFlow' was instrumental in getting this all up 
# and running.
# It can be found at 
# https://medium.com/ai-society/gans-from-scratch-1-a-deep-introduction-with-code-
# in-pytorch-and-tensorflow-cb03cdcdba0f
from loggingutils import Logger

# Define dataloader
import importlib
import preference_loader as pl
data = pl.Dataset('../data_in/Practice/ED-01-03.soi')
data_loader = torch.utils.data.DataLoader(data, batch_size=20, shuffle=False)
num_batches = len(data_loader)
num_votes = len(data)
num_features = len(data.pairs[-1])

# Discriminator Network
N = num_features
class DiscriminatorNet(torch.nn.Module):
    """
    A three hidden-layer discriminative neural network
    """
    def __init__(self):
        super(DiscriminatorNet, self).__init__()
        n_features = N
        n_out = 1
        
        self.hidden0 = nn.Sequential( 
            nn.Linear(N, N),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3)
        )
        self.hidden1 = nn.Sequential(
            nn.Linear(N, N),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3)
        )
        self.out = nn.Sequential(
            torch.nn.Linear(N, n_out),
            torch.nn.Sigmoid()
        )

    def forward(self, x):
        x = self.hidden0(x)
        x = self.hidden1(x)
        x = self.hidden1(x)
        x = self.hidden1(x)
        x = self.out(x)
        return x

# Generator Network
class GeneratorNet(torch.nn.Module):
    """
    A three hidden-layer generative neural network
    """
    def __init__(self):
        super(GeneratorNet, self).__init__()
        n_features = 100
        # hidden layer size
        h = 100
        n_out = N
        
        self.first = nn.Sequential(
            nn.Linear(n_features, h),
            nn.LeakyReLU(0.2)
        )
        self.hidden0 = nn.Sequential(
            nn.Linear(h,2*h),
            nn.LeakyReLU(0.2)
        )
        self.hidden1 = nn.Sequential(            
            nn.Linear(2*h, 4*h),
            nn.LeakyReLU(0.2)
        )
        self.hidden2 = nn.Sequential(            
            nn.Linear(4*h, 8*h),
            nn.LeakyReLU(0.2)
        )
        self.hidden3 = nn.Sequential(            
            nn.Linear(8*h, 8*h),
            nn.LeakyReLU(0.2)
        )
        self.hidden4 = nn.Sequential(            
            nn.Linear(8*h, 4*h),
            nn.LeakyReLU(0.2)
        )
        self.hidden5 = nn.Sequential(            
            nn.Linear(4*h, 2*h),
            nn.LeakyReLU(0.2)
        )
        self.out = nn.Sequential(
            nn.Linear(2*h, N),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.first(x)
        x = self.hidden0(x)
        x = self.hidden1(x)
        x = self.hidden2(x)
        x = self.hidden3(x)
        x = self.hidden4(x)
        x = self.hidden5(x)
        x = self.out(x)
        return x

# Noise Vectors
def noise(size):
    n = Variable(torch.randn(size, 100))
    if torch.cuda.is_available(): return n.cuda() 
    return n

num_test_samples = 5
test_noise = [noise(num_test_samples) for i in range(num_test_samples)]

# Send Networks to the GPU
discriminator = DiscriminatorNet()
generator = GeneratorNet()
if torch.cuda.is_available():
    print('GPU available')
    discriminator.cuda()
    generator.cuda()

# Define Optimizers
# This is where the adhoc parameter optimization happened
# for soi_07_01 these values work best around .0002 and .0001
# for soi_01_03 these values work best around .00004 and .00002
d_optimizer = optim.Adam(discriminator.parameters(), lr=0.0002)
g_optimizer = optim.Adam(generator.parameters(), lr=0.0001)

# Loss function
loss = nn.BCELoss()

# Number of steps to apply to the discriminator
d_steps = 1  # In Goodfellow et. al 2014 this variable is assigned to 1

'''
The author of this blog post
https://medium.com/@utk.is.here/keep-calm-and-train-a-gan-pitfalls-and-tips-on-training-generative-adversarial-networks-edd529764aa9
suggest using real=0 and fake=1 for improvbed 'gradient flow in the early generations'
'''

def real_data_target(size):
    '''
    Tensor containing ones, with shape = size
    '''
    data = Variable(torch.zeros(size, 1))
    if torch.cuda.is_available(): return data.cuda()
    return data

def fake_data_target(size):
    '''
    Tensor containing zeros, with shape = size
    '''
    data = Variable(torch.ones(size, 1))
    if torch.cuda.is_available(): return data.cuda()
    return data

def train_discriminator(optimizer, real_data, fake_data):
    optimizer.zero_grad()
    prediction_real = discriminator(real_data)
    error_real = loss(prediction_real, real_data_target(real_data.size(0)))
    error_real.backward()
    prediction_fake = discriminator(fake_data)
    error_fake = loss(prediction_fake, fake_data_target(real_data.size(0)))
    error_fake.backward()
    optimizer.step()
    return error_real + error_fake, prediction_real, prediction_fake

def train_generator(optimizer, fake_data):
    optimizer.zero_grad()
    prediction = discriminator(fake_data)
    error = loss(prediction, real_data_target(prediction.size(0)))
    error.backward()
    optimizer.step()
    return error

# Training Loop

num_epochs = 1 # set at 1 for debugging, this number depends on the dataset size

logger = Logger(model_name='PrefGAN', data_name='soi_01_03')
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
print('Logging in graph_logs//{}'.format(timestr))
g_display = None

test_vote_logs = [[] for i in test_noise]
for epoch in range(num_epochs):
    for n_batch, real_batch in enumerate(data_loader):
        real_data = Variable(real_batch)
        if torch.cuda.is_available(): real_data = real_data.cuda()
        fake_data = generator(noise(real_data.size(0))).detach()
        d_error, d_pred_real, d_pred_fake = train_discriminator(d_optimizer,real_data, fake_data)

        fake_data = generator(noise(real_batch.size(0)))
        g_error = train_generator(g_optimizer, fake_data)
        logger.log(d_error, g_error, epoch, n_batch, num_batches)
        if (n_batch) % 10 == 0 or num_batches - n_batch <= 10:
            display.clear_output(True)
            # Display Graph
            for i, noise_vector in enumerate(test_noise):
                test_vote = generator(noise_vector).data.cpu()[0]
                test_vote_logs[i].append(test_vote)
                # Uncomment these to display and save graph visualizations while running
                # significantly slows performance
                # g_display = gv.vec_to_graph(test_vote)
                # g_display.save('epoch{}batch{}graph{}'.format(epoch,n_batch,i),'../graph_logs/{}'.format(timestr))
            
            logger.display_status(
                epoch, num_epochs, n_batch, num_batches,
                d_error, g_error, d_pred_real, d_pred_fake
            )
            