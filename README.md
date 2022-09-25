# AuthentiCadence: On-Beat Security
###  Created by Daniel Wang, Jonathan Thomas, George Lyu, and Caleb McKinney

## Presentation
youtube link

## Overview
We address human error in cybersecurity by introducing AuthentiCadence, a biometric dimension to multi-factor authentication. AuthentiCadence learns the timing and rhythm of the keystrokes in the user’s password entry, defined as the user’s cadence. A binary classifier then identifies valid password entries based on this cadence. Importantly, even if a hacker knows the password, the device remains secured by cadence authentication.

## How it Works
We start with an initial set of valid cadences as training data. The cadences are encoded as vectors, where vector components represent normalized time elapsed between keystrokes. The distribution of cadence vectors is used to determine the maximum tolerable deviation from an expected cadence. This distribution is used to train a binary classifier to categorize valid cadences. When somebody attempts to login, their password cadence is input into the classifier. If the new password is found to match the original user’s cadence, it is admitted. Future valid password entries are added to the training data to retrain the classifier to account for drift in cadence patterns over time.

## Impact
Our product protects your account against hackers who have gained access to your password. In many cases, the hacker will struggle to gain access even if they know your cadence. In our trials, the rhythm was incredibly difficult to mimic. Secondly, cadence measuring is a process that is independent of many dual-factor authentication products like Duo, so our product is compatible with existing security frameworks. Lastly, our product measures biometrics without any peripheral technologies or hardware, so it can be widely applicable to phone locks, email logins, and database security.

## Instructions

First, clone the repository.
```bash
$ git clone git@github.com/JThomas12/AuthentiCadence-
$ cd AuthentiCadence-
```
Then install the required libraries.
```bash
$ pip install matplotlib customtkinter
```
Finally, run the Tkinter Python GUI
```bash
$ python gui.py
```

From there: 
- think of a password and cadence
- enter it into the training box at least twice
- enter your password into the testing box
- press submit and find out whether you were successfully able to authenticate 🔓

We hope that you enjoy playing with our project as much as we enjoyed making it!