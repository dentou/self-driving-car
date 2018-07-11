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
import pandas as pd
import random

class Network(object):
    
    def __init__(self, weights, sizes):
        """
        The list sizes contain sizes for each layer in neural net
        The list weights contain weights for all layers in NN, flattened
                with biases in front
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = []
        for i in sizes[1:]:
            self.biases.append(np.array(weights[:i]).reshape(i, 1))
            weights = weights[i:]
        
        self.weights = []
        for i in (self.num_layers-1):
            nw = sizes[i+1]*sizes[i]
            self.weights.append(np.array(weights[:nw])
                                .reshape((sizes[i+1],sizes[i])))
            weights = weights[nw:]

    def feedForward(self, a):
        """
        Output of neural network if input is a
        """
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a
    
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))
