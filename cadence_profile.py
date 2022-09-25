from cmath import exp
import numpy as np
import math
import matplotlib.pyplot as plt

class CadenceProfile:
    def __init__(self, sensitivity=1):
        '''
        INPUT
            sensitivity; threshold number of standard deviations away from expected cadence where invalid cadences are cut off
        '''
        self.trainData = np.array([]) #numpy array, where the ij element is the jth keystroke element of the ith password entry
        self.centroid = np.array([]) #numpy array, where the jth element is the average of the jth components of trainData
        self.distMean = np.array([])
        self.distStd = 0
        self.sensitivity = sensitivity
        
    def __str__(self):
        '''
        Printing this class gives the size of the training data and the number of keystrokes
        '''
        return str(np.shape(self.trainData))

    def getTrainData(self):
        return self.trainData
    
    def getCentroid(self):
        return self.centroid

    def getDistMean(self):
        return self.distMean

    def getDistStd(self):
        return self.distStd

    def timeToRatio(self, timeKeystroke):
        '''
        Converts a list of keystroke durations into a list of keystroke durations normalized to the sum fo their durations
        INPUT
            timeKeystroke; a list keystroke durations
        '''
        return np.array(timeKeystroke) / sum(timeKeystroke)

    def train(self, trainData):
        '''
        Trains the binary classifier to recognize valid cadence.
        INPUT
            trainData; numpy array, where the ij element is the jth keystroke element of the ith password entry
        OUTPUT
            centroid; the Euclidean centroid of the train_data
            mean; mean of the log of the Euclidean norms between training data and centroid
            std; standard deviation of the log of the Euclidean norms between training data and centroid
        '''
        centroid = np.average(trainData, axis=0)
        if(len(trainData.shape) == 1):
            dist = np.log(np.linalg.norm(trainData - centroid)) 
        else:
            dist = np.log(np.linalg.norm(trainData - centroid, axis=1))        
        return centroid, np.average(dist), np.std(dist)

    def verifyCadence(self, timeKeystroke, visualize=False):
        '''
        INPUT
            timeKeystroke; python list new keystroke entry (measures time elapsed between keystrokes, not necessarily with normalization)
            visualize; boolean whether to visualize the match graphically
        OUTPUT
            True/False to indicate validity of keystroke
        '''
        print("verifyCadence: ",timeKeystroke )
        keystroke = self.timeToRatio(timeKeystroke)
        
        # if the keystroke vector length is not consistent with the established length, reject
        if(keystroke.size  != self.trainData.shape[1]):
            return False

        # compute distance between each vector and the centroid
        error = math.log(np.linalg.norm(keystroke - self.centroid))
        threshold = self.distMean + self.sensitivity * self.distStd

        # check if vector is within threshold
        if (error < threshold):
            self.updateData(timeKeystroke)
            flag = True
        else:
            flag = False
        
        # visualize
        if (visualize):
            self.visualizeCadence(keystroke, flag)
        return (flag)

    def updateData(self, timeKeystroke):
        '''
        Updates the training data to include new valid detected keystroke entry. Then retrains model.
        INPUT
            timeKeystroke; python list new keystroke entry (measures time elapsed between keystrokes, not necessarily with normalization)
        '''
        keystroke = self.timeToRatio(timeKeystroke)
        if(self.trainData.size == 0):
            self.trainData = keystroke
        else:
            self.trainData = np.vstack([self.trainData, keystroke]) # add vector to training corpus
        self.centroid, self.distMean, self.distStd = self.train(self.trainData) # retrain

    def visualizeCadence(self, timeKeystroke=[], flag=False):
        '''
        Plots the target cadence range against an input cadence
        INPUT
            timeKeystroke; python list new keystroke entry (measures time elapsed between keystrokes, not necessarily with normalization)
            flag; boolean whether the input keystroke was admitted or not
        '''
        keystroke = self.timeToRatio(timeKeystroke) # normalize times of keystroke vector
        numTrain, numKey = self.trainData.shape
        keyInds = range(0, numKey)
        
        # compute target cadence bounds
        errRange = 1 / math.sqrt(numTrain) * math.exp(self.distMean + self.sensitivity * self.distStd)
        loBound = self.centroid - errRange
        hiBound = self.centroid + errRange

        # plot cadence bounds
        plt.fill_between(keyInds, loBound, hiBound,
                            interpolate=True, color="green", alpha=0.2,
                            label="Target cadence")
        
        # plot tested keystroke
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

# user = CadenceProfile()
# user.updateData([1, 2, 3, 4])
# print(user.getTrainData)

# dat = [[3, 2, 4.5, 6], [2.5, 1, 5.5, 7], [3.5, 3, 4, 5], [3, 2, 6, 6]]
# sensitivity = 1.5
# profile = CadenceProfile(dat, sensitivity)

# print(profile.verifyCadence(np.array([1, 2, 3, 4]), True))
# print(profile.verifyCadence(np.array([3, 2, 5.1, 6]), True))
# print(profile.verifyCadence(np.array([3, 2, 4, 4]), True))
# print(profile.verifyCadence(np.array([2, 3, 7, 7]), True))
# print(profile.verifyCadence(np.array([2, 3, 10, 8]), True))
# print(profile.verifyCadence(np.array([3, 2, 5, 0, 0]), True))

# print(profile.getTrainData())
# print(profile)
