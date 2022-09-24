import numpy as np

class CadenceProfile:
    def __init__(self, timeData):
        """
        INPUT
            trainData; numpy array, where the ij element is the jth keystroke element of the ith password entry
        """
        trainData = np.array([self.timeToRatio(keystroke) for keystroke in timeData])
        self.trainData = trainData
        self.centroid, self.distMean, self.distStd = self.train(trainData)
    
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


    def verifyCadence(self, timeKeystroke, sensitivity):
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
        threshold = self.distMean + sensitivity * self.distStd
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

dat = [[3, 2, 4.5, 6], [2.5, 1, 5.5, 7], [3.5, 3, 4, 5], [3, 2, 6, 6]]
profile = CadenceProfile(dat)
sensitivity = 1.5
print(profile.verifyCadence(np.array([1, 2, 3, 4]), sensitivity))
print(profile.verifyCadence(np.array([3, 2, 5.1, 6]), sensitivity))
print(profile.verifyCadence(np.array([3, 2, 4, 4]), sensitivity))
print(profile.verifyCadence(np.array([2, 3, 7, 7]), sensitivity))
print(profile.verifyCadence(np.array([2, 3, 10, 8]), sensitivity))
print(profile.verifyCadence(np.array([3, 2, 5, 0, 0]), sensitivity))

print(profile.getTrainData())
print(profile)
