import numpy as np
import math
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


    def verifyCadence(self, timeKeystroke):
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
        error = np.log(np.linalg.norm(keystroke - self.centroid))
        threshold = self.distMean + self.sensitivity * self.distStd
        if (error < threshold):
            self.updateData(keystroke)
            return True
        return False

    def updateData(self, keystroke):
        """
        Updates the training data to include new valid detected keystroke entry. Then retrains model.
        INPUT
            keystroke; numpy array of new keystroke entry
        """
        self.trainData = np.vstack([self.trainData, keystroke])
        self.centroid, self.distMean, self.distStd = self.train(self.trainData)

    def visualize(self, keystroke=None):
        numTrain, numKey = self.trainData.shape
        keyInds = range(0, numKey)
        errRange = self.sensitivity * self.distStd / math.sqrt(numTrain)
        loBound = self.centroid - errRange
        hiBound = self.centroid + errRange
        plt.fill_between(keyInds, loBound, hiBound,
                            interpolate=True, color="green", alpha=0.2,
                            label="Target cadence")
        plt.show()
        pass


dat = [[3, 2, 4.5, 6], [2.5, 1, 5.5, 7], [3.5, 3, 4, 5], [3, 2, 6, 6]]
sensitivity = 1.5
profile = CadenceProfile(dat, sensitivity)

print(profile.verifyCadence(np.array([1, 2, 3, 4])))
print(profile.verifyCadence(np.array([3, 2, 5.1, 6])))
print(profile.verifyCadence(np.array([3, 2, 4, 4])))
print(profile.verifyCadence(np.array([2, 3, 7, 7])))
print(profile.verifyCadence(np.array([2, 3, 10, 8])))
print(profile.verifyCadence(np.array([3, 2, 5, 0, 0])))

print(profile.getTrainData())
print(profile)
profile.visualize()