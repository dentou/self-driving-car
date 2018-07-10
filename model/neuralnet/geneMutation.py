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
    
    def __init__(self, weights, sizes):
        self.weights = weights
        self.wSize = len(weights)
        self.sizes = sizes
        
    def normalDistMutation(self, genes, mu, sigma):
        """
        Random mutation according to normal distribution on selected genes
        genes is boolean list of length self.wSize indicating which gene to be
        mutated
        """
        return [w+i*random.gauss(mu, sigma) for w, i in
                                zip(self.weights, genes)]
