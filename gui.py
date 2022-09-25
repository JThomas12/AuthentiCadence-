import tkinter as tk
from tkinter import messagebox
import time

from user_profile import UserProfile

class TestAuthentiCadence:
    def __init__(self):
        self.window = tk.Tk()
        self.user = UserProfile()

        self.num_trials = 0

        self.cur_train_keystrokes = []
        self.prev_train_str = ""
        self.prev_train_change_time = None
        self.prev_test_change_time = None

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

        self.cur_test_keystrokes = []
        self.prev_test_str = ""

        test_pass_label = tk.Label(self.window, text = "Test your trained password below:")
        test_pass_label.pack(padx=50, pady=5)

        self.test_pass_entry = tk.StringVar()
        self.test_pass_entry.trace("w", lambda name, index, mode, sv = self.test_pass_entry: self.onTestPassChange(sv))
        
        self.test_pass_box = tk.Entry(self.window, textvariable = self.test_pass_entry, state='disabled')
        self.test_pass_box.pack(padx=50, pady=5)
        
        self.test_pass_button = tk.Button(self.window, text="Enter Password", command=self.testPass, state='disabled')
        self.test_pass_button.pack()

        self.window.mainloop()

    def onCreatePassChange(self, sv):
        cur_str = sv.get()
        cur_change_time = time.perf_counter()

        if len(self.prev_train_str) == 0 or len(cur_str) == 0:
            self.cur_train_keystrokes = []
        else:
            if len(cur_str) > len(self.prev_train_str):
                self.cur_train_keystrokes.append(cur_change_time - self.prev_train_change_time)
            else:
                self.cur_train_keystrokes.pop()

        print(self.cur_train_keystrokes)
        self.prev_train_str = cur_str
        self.prev_train_change_time = cur_change_time

    def trainPass(self):    
        print(self.cur_train_keystrokes)
        # If the user has a stored password
        if self.user.hasPassword():
            # Validate password is correct
            if hash(self.train_pass_entry.get()) == self.user.password:
                # Add current time data to user's time dataset
                self.user.cadence_profile.updateData(self.cur_train_keystrokes)
                print("Correct password added to user!")
            else:
                # If password incorrect, do nothing
                messagebox.showerror("Incorrect password!", "Please enter the correct password.")
        else:
            # Set password of user to current pass entry
            self.user.setPassword(self.train_pass_entry.get())
            # Add current time data to user's time datset
            self.user.cadence_profile.updateData(self.cur_train_keystrokes)
            print("New password added to user!")

        # Reset entry box
        self.train_pass_entry.set("")
        self.num_trials += 1
        self.num_trials_label.config(text = str(self.num_trials) + " Trials")
        
        # Enable testing functionality
        self.test_pass_box.config(state="normal")
        self.test_pass_button.config(state="normal")

        print(self.user.cadence_profile.getTrainData())

    def onTestPassChange(self, sv):
        cur_str = sv.get()
        cur_change_time = time.perf_counter()

        if len(self.prev_test_str) == 0 or len(cur_str) == 0:
            self.cur_test_keystrokes = []
        else:
            if len(cur_str) > len(self.prev_test_str):
                self.cur_test_keystrokes.append(cur_change_time - self.prev_test_change_time)
            else:
                self.cur_test_keystrokes.pop()

        print(self.cur_test_keystrokes)
        self.prev_test_str = cur_str
        self.prev_test_change_time = cur_change_time
            
    def testPass(self):
        if hash(self.train_pass_entry.get()) != self.user.password:
            # If password incorrect, do nothing
            messagebox.showerror("Incorrect password!", "Please enter the correct password.")
        else:
            isVerified = self.user.verifyPassword(self.test_pass_entry.get(), self.cur_test_keystrokes)
            if isVerified:
                print("User successfully logged in")
            else:
                print("User failed to authenticate")
            self.user.cadence_profile.visualizeCadence(self.cur_test_keystrokes, isVerified)
        self.test_pass_entry.set("")

TestAuthentiCadence()