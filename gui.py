import tkinter as tk
from tkinter import messagebox
import time

from user_profile import *

class UserProfile:
    def __int__(self, username, password, timeData):
        """
        INPUT
            username; a string that is the user's username
            password; a string that is the user's password
            timeData; the time between each keyStroke when entering the password
        """
        #self.username = username
        self.password = password
        self.timeData = timeData

class TestAuthentiCadence:
    def __init__(self):
        self.window = tk.Tk()
        user = UserProfile()
        self.user = user

        # store all trials of entered password
        user.timeData = []
        user.password = None

        self.delta_ts = []
        self.prev_str = ""
        self.prev_change_time = time.perf_counter()

        # Create password and train model =================================================

        #show_hide_pass_box = tk.Checkbutton(text="", )

        train_pass_label = tk.Label(self.window, text = "Create a password below with your favorite rhythm!")
        train_pass_label.pack(padx=50, pady=5)

        self.num_trials_label = tk.Label(self.window, text = "0 Trials")
        self.num_trials_label.pack()

        self.train_pass_entry = tk.StringVar()
        self.train_pass_entry.trace("w", lambda name, index, mode, sv=self.train_pass_entry: self.onCreatePassChange(sv))

        train_pass_box = tk.Entry(self.window, textvariable=self.train_pass_entry)
        train_pass_box.pack(padx=50, pady=5)

        train_pass_button = tk.Button(self.window, text="Create/Train Password", command=self.trainPass)
        train_pass_button.pack()

        # Test Model ====================================================

        test_pass_label = tk.Label(self.window, text = "Test your trained password below:")
        test_pass_label.pack(padx=50, pady=5)

        self.test_pass_entry = tk.StringVar()
        self.test_pass_entry.trace("w", lambda name, index, mode, sv = self.test_pass_entry: self.onCreatePassChange(sv))
        
        self.test_pass_box = tk.Entry(self.window, textvariable = self.test_pass_entry, state='disabled')
        self.test_pass_box.pack(padx=50, pady=5)
        
        self.test_pass_button = tk.Button(self.window, text="Enter Password", command=self.testPass, state='disabled')
        self.test_pass_button.pack()

        self.window.mainloop()

    def onCreatePassChange(self, sv):
        cur_str = sv.get()
        cur_change_time = time.perf_counter()

        if len(cur_str) == 0:
            self.delta_ts = []
        else:
            if len(cur_str) > len(self.prev_str):
                self.delta_ts.append(cur_change_time - self.prev_change_time)
            else:
                self.delta_ts.pop()

        print(self.delta_ts)
        self.prev_str = cur_str
        self.prev_change_time = cur_change_time

    def trainPass(self):
        # If the user has a stored password
        if self.user.password:
            # Validate password is correct
            if self.train_pass_entry.get() == self.user.password:
                # Add current time data to user's time dataset
                self.user.timeData.append(self.delta_ts)
                print("Correct password "+ self.user.password + " added to user!")
            else:
                # If password incorrect, do nothing
                messagebox.showerror("Incorrect password!")
        else:
            # Set password of user to current pass entry
            self.user.password = self.train_pass_entry.get()
            # Add current time data to user's time datset
            self.user.timeData.append(self.delta_ts)
            print("New password "+ self.user.password + " added to user!")

        # Reset entry box
        self.train_pass_entry.set("")
        self.num_trials_label.config(text = str(len(self.user.timeData)) + " Trials")
        
        # Enable testing functionality
        self.test_pass_box.config(state="normal")
        self.test_pass_button.config(state="normal")

    def testPass(self):
        print("Test")
        # If the user has a stored password

TestAuthentiCadence()