from cadence_profile import CadenceProfile 

class UserProfile:
    def __int__(self, username, password, timeData):
        """
        INPUT
            username; a string that is the user's username
            password; a string that is the user's password
            timeData; a list of the times between each key stroke for the 5 trainig enteries
        """
        self.username = username
        self.password = password.hash()
        self.cadence_profile = CadenceProfile(timeData)

    def getUsername(self):
        return self.username

    def verifyPassword(self, password,keyStrokeTime):
        """
        INPUT
            password; the password the user entered
            keyStrokeTime; the time between each keyStroke when entering the password
        OUTPUT
            true if the password and cadence match, false otherwise
        """
        if(self.password != password.hash()):
            return False
        return self.cadence_profile.verifyCadence(keyStrokeTime)

    def resetPassword(self, password, timeData):
        """
        INPUT
            password; the new password the user entered
            timeData; a list of the times between each key stroke for the 5 trainig enteries
        """
        self.password = password.hash()
        self.cadence_profile = CadenceProfile(timeData)
