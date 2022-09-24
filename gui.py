# Python tkinter hello world program
  
import tkinter as tk
import time

class TestEntry:

    def __init__(self):
        self.window = tk.Tk()

        self.delta_ts = []
        self.prev_str = ""
        self.prev_change_time = time.perf_counter()

        self.create_widgets()

    def create_widgets(self):
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))

        b = tk.Label(self.window, text ="Hello World")
        a = tk.Entry(self.window, textvariable=sv)

        a.pack()
        b.pack()

        self.window.mainloop()

    def callback(self, sv):
        cur_str = sv.get()
        cur_change_time = time.perf_counter()

        if len(cur_str) > len(self.prev_str):
            self.delta_ts.append(cur_change_time - self.prev_change_time)
        else:
            self.delta_ts.pop()

        print(self.delta_ts)
        self.prev_str = cur_str
        self.prev_change_time = cur_change_time

TestEntry()