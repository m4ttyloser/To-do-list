import tkinter as tk
from tkinter import *

class ProgressTracker:
    def _init_(self, master):
        self.master = master
        master.title("Productivity tracker")
        master.geometry("500x500")
        master.configure(background = "lightblue")

        self.label = Label(master, text="Productivity:")
        self.label.pack(pady=10)

        self.progress_var = DoubleVar()
        self.progress_bar = tk.Progressbar(master, orient="horizontal", length=300, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack(pady=10)

        self.progress_label = Label(master, text="0%")
        self.progress_label.pack(pady=5)

        self.progress_button = Button(master, text="Show rate")
        self.progress_button.pack(pady=10)

        self.wisdom_label = Label(master, text="Words of wisdom")
        self.wisdom_label.place(x=200,y=270)

        self.canvas = Canvas(master, width=400, height=200, bg="lightblue", highlightthickness=0)
        self.canvas.place(x= 50,y=290)

        self.canvas.create_text(200, 100, text="Motivational", font=("Arial", 16), fill="white")

        self.create_rounded_rectangle(20, 20, 380, 180, 20, outline="#333333", fill="black")

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def open_progress_tracker():
        root = Tk()
        pprogress_tracker_window = ProgressTracker(root)
        root.mainloop()