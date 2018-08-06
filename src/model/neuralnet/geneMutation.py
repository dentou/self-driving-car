"""
Created on Fri Jun 29 11:41:49 2018

@author: npgh2
"""

"""
Implement methods for mutation of children to occur
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

class Mutation(object):
    
    def __init__(self, genes, sizes):
        self.genes = genes
        self.gSize = len(genes)
        self.sizes = sizes
        
    def gaussian(self, mu = 0, sigma = 0.1, mask = None):
        """
        Random mutation according to normal distribution on selected genes
        mask is 0/1 list of length self.wSize indicating which gene to be
        mutated
        """
        if mask == None:
            return [w + random.gauss(mu, sigma) for w in self.genes]
        else:
            assert len(mask) == self.gSize
            return [w + i*random.gauss(mu, sigma) for w, i in zip(self.weights, genes)]
