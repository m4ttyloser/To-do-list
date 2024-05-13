from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import datetime
import pygame

class ProgressTracker:
    def __init__(self, master):
        self.master = master
        master.title("To-do list")
        master.geometry("400x650+400+100")
        master.resizable(False, False)

        # icon
        self.Image_icon = Image.open("task.png")
        self.Image_icon = ImageTk.PhotoImage(self.Image_icon)
        master.iconphoto(False, self.Image_icon)

        self.TopImage = Image.open("topbar.png")
        self.TopImage = ImageTk.PhotoImage(self.TopImage)
        Label(master, image=self.TopImage).pack()

        self.dockImage = Image.open("dock.png")
        self.dockImage = ImageTk.PhotoImage(self.dockImage)
        Label(master, image=self.dockImage, bg="#32405b").place(x=30, y=25)

        self.noteImage = Image.open("task.png")
        self.noteImage = ImageTk.PhotoImage(self.noteImage)
        Label(master, image=self.noteImage, bg="#32405b").place(x=30, y=25)

        heading = Label(master, text="PROGRESS", font="arial 20 bold", bg="#32405b")
        heading.place(x=125, y=20)

        # pomodoro button
        self.pomodoro_icon = Image.open("timer icon.png").resize((100, 100))
        self.pomodoro_icon = ImageTk.PhotoImage(self.pomodoro_icon)
        Button(master, image=self.pomodoro_icon, bd=0).place(x=30, y=90)

        # planner button
        self.planner_icon = Image.open("planner.png").resize((100, 100))
        self.planner_icon = ImageTk.PhotoImage(self.planner_icon)
        Button(master, image=self.planner_icon, bd=0).place(x=145, y=90)

        # Progress button
        self.progress_icon = Image.open("progress.png").resize((100, 100))
        self.progress_icon = ImageTk.PhotoImage(self.progress_icon)
        Button(master, image=self.progress_icon, bd=0).place(x=270, y=90)

        # Progress bar
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(master, orient=HORIZONTAL, length=300, mode="determinate", variable=self.progress_var)
        self.progress_bar.place(x=50, y=300)

        # Progress percentage label
        self.progress_label = Label(master, text="", font="arial 12")
        self.progress_label.place(x=200, y=350)

        self.update_progress(100)

    def update_progress(self, percentage):
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"{percentage}%")


def tracker_window():
    root = Tk()
    app = ProgressTracker(root)
    root.mainloop()


tracker_window