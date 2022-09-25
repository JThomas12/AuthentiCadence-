from sre_parse import State
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD
import customtkinter
import time

from user_profile import UserProfile

class TestAuthentiCadence:
    def __init__(self):
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        self.window = customtkinter.CTk()
        self.window.title("AuthentiCadence")
        self.window.geometry("800x500")

        self.user = UserProfile()

        customtkinter.CTkLabel(text="AuthentiCadence", text_font=("Calibri",25)).pack(pady=10)
        
        customtkinter.CTkLabel(text="Options:", text_font=("Calibri Bold", 16)).pack(pady=10)
        customtkinter.CTkButton(self.window, text="Refresh Window", command=self.refresh).pack()

        self.show_viz_check = tk.IntVar(value=1)
        customtkinter.CTkCheckBox(self.window, text="Show Authentication Visualization", variable=self.show_viz_check, onvalue=1, offvalue=0).pack()
        
        self.hide_password_check = tk.IntVar()
        customtkinter.CTkCheckBox(self.window, text="Hide Password Entry", variable=self.hide_password_check, onvalue=1, offvalue=0, command=self.updateShowPass).pack()

        self.num_trials = 0

        self.cur_train_keystrokes = []
        self.prev_train_str = ""
        self.prev_train_change_time = None
        self.prev_test_change_time = None

        # Create password and train model =================================================
        customtkinter.CTkLabel(text="Password Training:", text_font=("Calibri Bold", 16)).pack(pady=(10, 0))

        train_pass_label = customtkinter.CTkLabel(self.window, text = "Create a password below with your favorite rhythm!")
        train_pass_label.pack()

        self.num_trials_label = customtkinter.CTkLabel(self.window, text = "0 Trials")
        self.num_trials_label.pack()

        self.train_pass_entry = tk.StringVar()
        self.train_pass_entry.trace("w", lambda name, index, mode, sv=self.train_pass_entry: self.onCreatePassChange(sv))

        self.train_pass_box = customtkinter.CTkEntry(self.window, textvariable=self.train_pass_entry)
        self.train_pass_box.pack()

        train_pass_button = customtkinter.CTkButton(self.window, text="Create/Train Password", command=self.trainPass)
        train_pass_button.pack(pady=(5, 0))

        # Test Model ====================================================
        customtkinter.CTkLabel(text="Password Testing:", text_font=("Calibri Bold", 16)).pack(pady=(10, 0))

        self.cur_test_keystrokes = []
        self.prev_test_str = ""

        test_pass_label = customtkinter.CTkLabel(self.window, text = "Test your trained password below:")
        test_pass_label.pack()

        self.test_pass_entry = tk.StringVar()
        self.test_pass_entry.trace("w", lambda name, index, mode, sv = self.test_pass_entry: self.onTestPassChange(sv))
        
        self.test_pass_box = customtkinter.CTkEntry(self.window, textvariable = self.test_pass_entry, state=tk.DISABLED)
        self.test_pass_box.pack()
        
        self.test_pass_button = customtkinter.CTkButton(self.window, text="Enter Password", command=self.testPass, state=tk.DISABLED)
        self.test_pass_button.pack(pady=(5, 0))

        self.window.mainloop()
        self.window.update()

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
                self.num_trials += 1
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
            self.num_trials += 1

        # Reset entry box
        self.train_pass_entry.set("")
        self.num_trials_label.configure(text = str(self.num_trials) + " Trials")
        
        # Enable testing functionality if at least two trials
        if self.num_trials >= 2:
            self.test_pass_box.configure(state="normal")
            self.test_pass_button.configure(state="normal")

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
        if hash(self.test_pass_entry.get()) != self.user.password:
            # If password incorrect, do nothing
            messagebox.showerror("Incorrect password (value)!", "Please enter the password value.")
        else:
            isVerified = self.user.verifyPassword(self.test_pass_entry.get(), self.cur_test_keystrokes)
            showViz = self.show_viz_check.get()
            
            if showViz:
                self.user.cadence_profile.visualizeCadence(self.cur_test_keystrokes, isVerified)
            else:
                if isVerified:
                    messagebox.showinfo("Correct password!", "User sucessfuly authenticated.")
                else:
                    messagebox.showerror("Incorrect password (rhythm)!", "Please enter the correct password rhythm.")

        self.test_pass_entry.set("")

    def updateShowPass(self):
        if self.hide_password_check.get():
            self.test_pass_box.configure(show="*")
            self.train_pass_box.configure(show="*")
        else:
            self.test_pass_box.configure(show="")
            self.train_pass_box.configure(show="")
    
    def refresh(self):
        self.window.destroy()
        TestAuthentiCadence()

TestAuthentiCadence()