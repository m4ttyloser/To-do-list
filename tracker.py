from tkinter import *
from tkinter import ttk

class ProgressTracker:
    def __init__(self, master):
        self.master = master
        master.title("To-do list")
        master.geometry("400x650+400+100")
        master.resizable(False, False)

        # icon
        self.Image_icon = PhotoImage(file="task.png")
        master.iconphoto(False, self.Image_icon)

        self.TopImage = PhotoImage(file="topbar.png")
        Label(master, image=self.TopImage).pack()

        self.dockImage = PhotoImage(file="dock.png")
        Label(master, image=self.dockImage, bg="#32405b").place(x=30, y=25)

        self.noteImage = PhotoImage(file="task.png")
        Label(master, image=self.noteImage, bg="#32405b").place(x=30, y=25)

        heading = Label(master, text="PROGRESS", font="arial 20 bold", bg="#32405b")
        heading.place(x=125, y=20)

        # pomodoro button
        self.pomodoro_icon = PhotoImage(file="timer icon.png")
        small_pomodoro_icon = self.pomodoro_icon.subsample(6, 6)
        Button(master, image=small_pomodoro_icon, bd=0).place(x=40, y=90)

        # planner button
        self.planner_icon = PhotoImage(file="planner.png")
        small_planner_icon = self.planner_icon.subsample(6, 6)
        Button(master, image=small_planner_icon, bd=0).place(x=150, y=90)

        # Progress button
        self.progress_icon = PhotoImage(file="progress.png")
        small_progress_icon = self.progress_icon.subsample(6, 6)
        Button(master, image=small_progress_icon, bd=0).place(x=280, y=90)

        # Progress bar
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(master, orient=HORIZONTAL, length=300, mode="determinate", variable=self.progress_var)
        self.progress_bar.place(x=50, y=300)

        # Progress percentage label
        self.progress_label = Label(master, text="", font="arial 12")
        self.progress_label.place(x=200, y=350)

        self.update_progress(50)

    
    def update_progress(self, percentage):
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"{percentage}%")



def tracker_window():
    root = Tk()
    app = ProgressTracker(root)
    root.mainloop()

tracker_window()
