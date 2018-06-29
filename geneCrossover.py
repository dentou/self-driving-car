"""
Created on Fri Jun 29 10:02:51 2018

@author: npgh2
"""

"""
Implement different gene crossover method
https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_crossover.htm
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import math

class Crossover(object):
    
    def __init__(self, weightsA, weightsB, sizes):
        """
        Take input parents as python list
        """
        self.weightsA = weightsA
        self.weightsB = weightsB
        
        assert len(weightsA) == len(weightsB)
        self.wSize = len(weightsA)
        
        self.sizes = sizes
        
    def onePointCrossover(self, crossPoint):
        """
        Not recommended since the bias is put at the front
        Example: crossPoint = 3
        ParentA: 1 2 3 4 5 6 7 8 9
        ParentB: 9 8 7 6 5 4 3 2 1
        Result : 1 2 3 6 5 4 3 2 1
        
        """
        return self.weightsA[:crossPoint]+self.weightsB[crossPoint:]
    
    def middlePointCrossover(self):
        """
        Example: 
        ParentA: 1 2 3 4 5 6 7 8 9
        ParentB: 9 8 7 6 5 4 3 2 1
        Result : 1 2 3 4 5 4 3 2 1
        """
        n = int(self.wSize/2)
        return self.onePointCrossover(n)
    
    def multiPointCrossover(self, crossPoints):
        """
        Input crossPoints as alternating size of genes to take from each
        parents.
        Example: crossPoints = [2,3,2,2]
        ParentA: 1 2 3 4 5 6 7 8 9
        ParentB: 9 8 7 6 5 4 3 2 1
        Result : 1 2 7 6 5 6 7 2 1
        
        Error should be handled if sum of crossPoints equal to size of weightss
        """        
        b = []
        flag = True
        for i in crossPoints:
            if flag:
                b = b + [1]*i
            else:
                b = b + [0]*i
        
        assert len(b) == np.wSize
        
        w = [x*i+y*(1-i) for x, y, i in
                     zip(self.weightsA, self.weightsB, b)]
        return w
    
    def zigzagCrossover(self):
        """
        Example: 
        ParentA: 1 2 3 4 5 6 7 8 9
        ParentB: 9 8 7 6 5 4 3 2 1
        Result : 1 8 3 6 5 4 7 2 9
        """
        c = [1]*self.wSize
        return self.multiPointCrossover(c)
    
    def binomialCrossover(self, bias):
        """
        Generate a crossPoints list by flipping coin with bias
        then use multiPointCrossover to mix genes
        0 <= Bias <= 1
        Bias = 0.5 is unbiased coin
        Bias > 0.5 favors Parent B
        Bias < 0.5 favors Parent A
        """
        currentFlip = flipCoin(bias)
        cP = [1]
        
        for i in range(1, self.wSize):
            nextFlip = flipCoin(bias)
            if nextFlip == currentFlip:
                cP[-1] += 1
            else:
                cP.append(1)
            currentFlip = nextFlip
        
        return self.multiPointCrossover(cP)
    
    def linearArithmeticCombination(self, alpha):
        """
        Combine the two parents' genes by linear combination
        0 <= alpha <= 1
        weightChild = alpha*weightA + (1-alpha)*weightB
        """
        return [alpha*x + (1-alpha)*y for x, y in
                            zip(self.weightsA, self.weightsB)]

def flipCoin(bias):
    rdnum = random.random()
    if rdnum > bias:
        return 1
    else:
        return 0
