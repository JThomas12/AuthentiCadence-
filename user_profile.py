from cadence_profile import CadenceProfile 

class UserProfile:
    def __init__(self):
        """
        INPUT
            username; a string that is the user's username
            password; a string that is the user's password
            timeData; a list of the times between each key stroke for the 5 trainig enteries
        """
        self.password = ""
        self.cadence_profile = CadenceProfile()

    def setPassword(self, password):
        self.password = hash(password)

    def hasPassword(self):
        return self.password != ""
    

    def verifyPassword(self, password, keyStrokeTime):
        """
        INPUT
            password; the password the user entered
            keyStrokeTime; the time between each keyStroke when entering the password
        OUTPUT
            true if the password and cadence match, false otherwise
        """
        print("verifyPassword: ", keyStrokeTime)
        if(self.password != hash(password)):
            return False
        return self.cadence_profile.verifyCadence(keyStrokeTime)

    def resetPassword(self, password, timeData):
        """
        INPUT
            password; the new password the user entered
            timeData; a list of the times between each key stroke for the 5 trainig enteries
        """
        self.password = hash(password)
        self.cadence_profile = CadenceProfile(timeData)
    
    def getNumTrials(self):
        return self.cadence_profile.trainData.shape[0]
