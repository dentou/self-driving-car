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

        self.num_genes = sum(sizes[1:]) + sum([x*y for x, y in zip(sizes[:-1], sizes[1:])])

        if genes == None: # if no inputed genes, then randomized
            self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
            self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

        else:
            assert len(genes) == self.num_genes
            for i in sizes[1:]:
                self.biases.append(np.array(genes[:i]).reshape(i, 1))
                genes = genes[i:] #truncate the appended genes
        
            for i in range(self.num_layers-1):
                nw = sizes[i+1]*sizes[i]
                self.weights.append(np.array(genes[:nw]).reshape((sizes[i+1],sizes[i])))
                genes = genes[nw:] #truncate the appended genes

    def editGenes(self, genes):
        assert len(genes) == self.num_genes
        self.biases = []
        self.weights = []

        for i in self.sizes[1:]:
            self.biases.append(np.array(genes[:i]).reshape(i, 1))
            genes = genes[i:] #truncate the appended genes
    
        for i in range(self.num_layers-1):
            nw = self.sizes[i+1]*self.sizes[i]
            self.weights.append(np.array(genes[:nw]).reshape((self.sizes[i+1], self.sizes[i])))
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

def main():
    """
    Test program
    """
    nn = NeuralNetwork(sizes = [3, 4, 3])
    print("Initialize nn")
    print("Biases")
    print(nn.biases)
    print("Weights")
    print(nn.weights)

    a = nn.feedForward(np.array([100, 100, 100]))
    print("Output from all 100 vectors")
    print(a)

    b = nn.flattenWeights()
    print("Flattened weights (genes)")
    print(b)

    rdgenes = np.random.randn(4+3+3*4+4*3).tolist()
    nn.editGenes(rdgenes)
    print("Rerandom genes")
    a = nn.feedForward(np.array([100, 100, 100]))
    print("New output from all 100 vectors")
    print(a)


if __name__ == "__main__":
    main()