"""
Created on Fri Jun 29 09:09:26 2018

@author: npgh2

Some code taken from Michael Nielsen
"""

"""
Three layer feed-forward neural nets for self-driving car program
"""

import numpy as np
import matplotlib.pyplot as plt
import random

class NeuralNetwork(object):
    
    def __init__(self, sizes, genes = None):
        """
        The list 'sizes' contain sizes for each layer in neural net (including input and output layers)
        The list 'genes' contain weights&biases for all layers in NN, flattened
        If 'weights' is None, randomize the weights and biases
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = []
        self.weights = []

        num_genes = sum(sizes[1:]) + sum([x*y for x, y in zip(sizes[:-1], sizes[1:])])
        assert len(genes) = num_genes

        if weights == None:
            self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
            self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

        else:
            for i in sizes[1:]:
                self.biases.append(np.array(genes[:i]).reshape(i, 1))
                genes = genes[i:] #truncate the appended genes
        
            for i in range(self.num_layers-1):
                nw = sizes[i+1]*sizes[i]
                self.weights.append(np.array(genes[:nw]).reshape((sizes[i+1],sizes[i])))
                genes = genes[nw:] #truncate the appended genes

    def feedForward(self, a):
        """
        Output of neural network if input is a
        """
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def flattenWeights(self):
        genes = []
        for b in self.biases:
            genes += b.flatten().tolist()

        for w in self.weights:
            genes += w.flatten().tolist()

        return genes
    
def sigmoid(z):
    """
    The sigmoid function.
    """
    return 1.0/(1.0+np.exp(-z))
