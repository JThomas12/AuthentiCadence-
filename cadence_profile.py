from cmath import exp
import numpy as np
import math
import random
import matplotlib.pyplot as plt


class CadenceProfile:
    def __init__(self, timeData, sensitivity=1.5):
        """
        INPUT
            trainData; numpy array, where the ij element is the jth keystroke element of the ith password entry
        """
        trainData = np.array([self.timeToRatio(keystroke) for keystroke in timeData])
        self.trainData = trainData
        self.centroid, self.distMean, self.distStd = self.train(trainData)
        self.sensitivity = sensitivity

    def timeToRatio(self, keyStrokes):
        firstTime = keyStrokes[0]
        return (np.array(keyStrokes)[1:] / firstTime)
        
    def __str__(self):
        return str(np.shape(self.trainData))

    def getTrainData(self):
        return self.trainData
    
    def getCentroid(self):
        return self.centroid

    def getDistMean(self):
        return self.distMean

    def getDistStd(self):
        return self.distStd

    def train(self, trainData):
        """
        INPUT
            trainData; numpy array, where the ij element is the jth keystroke element of the ith password entry
        OUTPUT
            centroid; the Euclidean centroid of the train_data
            mean; mean of the log of the Euclidean norms between training data and centroid
            std; standard deviation of the log of the Euclidean norms between training data and centroid
        """
        centroid = np.average(trainData, axis=0)
        dist = np.log(np.linalg.norm(trainData - centroid, axis=1))        
        return centroid, np.average(dist), np.std(dist)


    def verifyCadence(self, timeKeystroke, visualize=False):
        """
        INPUT
            keystroke; numpy array of new keystroke entry
            sensitivity; number of standard deviations to account for in verification threshold
        OUTPUT
            True/False to indicate validity of keystroke
        """
        keystroke = self.timeToRatio(timeKeystroke)
        if(keystroke.size  != self.trainData.shape[1]):
            return False
        error = math.log(np.linalg.norm(keystroke - self.centroid))
        threshold = self.distMean + self.sensitivity * self.distStd
        if (error < threshold):
            self.updateData(keystroke)
            flag = True
        else:
            flag = False
        if (visualize):
            self.visualizeCadence(keystroke, flag)
        return (flag)

    def updateData(self, keystroke):
        """
        Updates the training data to include new valid detected keystroke entry. Then retrains model.
        INPUT
            keystroke; numpy array of new keystroke entry
        """
        self.trainData = np.vstack([self.trainData, keystroke])
        self.centroid, self.distMean, self.distStd = self.train(self.trainData)

    def visualizeCadence(self, keystroke=np.array([0]), flag=False):
        numTrain, numKey = self.trainData.shape
        keyInds = range(0, numKey)
        errRange = 1 / math.sqrt(numTrain) * math.exp(self.distMean + self.sensitivity * self.distStd)
        loBound = self.centroid - errRange
        hiBound = self.centroid + errRange
        plt.fill_between(keyInds, loBound, hiBound,
                            interpolate=True, color="green", alpha=0.2,
                            label="Target cadence")
        if (keystroke.any()):
            if (flag):
                plt.plot(keyInds, keystroke,
                            color = "blue",
                            label = "Observed cadence (ACCEPTED)")
            else:
                plt.plot(keyInds, keystroke,
                            color = "red",
                            label = "Observed cadence (REJECTED)")
        plt.xticks(range(numKey))
        plt.xlabel("Keystroke #")
        plt.ylabel("Cadence ratio")
        plt.title("Cadence authentication")
        plt.legend()
        plt.show()
        pass


dat = [[3, 2, 4.5, 6], [2.5, 1, 5.5, 7], [3.5, 3, 4, 5], [3, 2, 6, 6]]
sensitivity = 1.5
profile = CadenceProfile(dat, sensitivity)

print(profile.verifyCadence(np.array([1, 2, 3, 4]), True))
print(profile.verifyCadence(np.array([3, 2, 5.1, 6]), True))
print(profile.verifyCadence(np.array([3, 2, 4, 4]), True))
print(profile.verifyCadence(np.array([2, 3, 7, 7]), True))
print(profile.verifyCadence(np.array([2, 3, 10, 8]), True))
print(profile.verifyCadence(np.array([3, 2, 5, 0, 0]), True))

print(profile.getTrainData())
print(profile)
