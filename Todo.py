from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
import pygame
from emran import *


def update_button_state():
    has_undone_tasks = any(not task.endswith("\u2713") for task in listbox.get(0, END))
    button_mark_as_done.config(state=NORMAL if has_undone_tasks else DISABLED)


def early_score(early_points):
    global early_scores
    early_scores += early_points


def calculate_productivity(progress_tracker=None):
    global early_scores
    global score
    if early_scores > 0:
        percentage = (score / early_scores) * 100
        percentage_label.config(text=f"Productivity: {percentage:.2f}%")
        if progress_tracker:
            progress_tracker.update_progress(percentage)
    else:
        percentage_label.config(text="Productivity: N/A")
        if progress_tracker:
            progress_tracker.update_progress(0)


def open_pomodoro_timer():
    pomodoro_window = Toplevel(root)
    pomodoro_window.title("Pomodoro timer")
    pomodoro_window.geometry("500x400")
    PomodoroTimer(pomodoro_window)


def open_progress_tracker():
    progress_tracker_window = Toplevel(root)
    progress_tracker = ProgressTracker(progress_tracker_window)
    calculate_productivity(progress_tracker)
    progress_tracker_window.mainloop()


def add_task():
    task_text = task_entry.get()
    if task_text:
        start_time = f"{hour_spinbox_due.get().zfill(2)}:{minute_spinbox_due.get().zfill(2)}"
        if start_time:
            task_text += f" (At: {start_time})"
            listbox.insert(END, task_text)
            task_entry.delete(0, END)
            update_button_state()
            early_score(1)
            if percentage_label.cget("text") == "Productivity: 100.00%":
                pass
            else:
                calculate_productivity()
            current_time = datetime.datetime.now().strftime('%H:%M')
            if current_time == start_time:
                play_alarm()
    else:
        messagebox.showwarning("Warning", "Please enter a task.")


def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("BLIND.wav")
    pygame.mixer.music.play()


def remove_task():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        listbox.delete(selected_task_index)
        update_button_state()
        early_score(-1)
    else:
        messagebox.showwarning("Please select a task to remove")


def mark_as_done():
    selected_task_indices = listbox.curselection()
    if selected_task_indices:
        for index in selected_task_indices:
            selected_task = listbox.get(index)
            if isinstance(selected_task, str):
                if not selected_task.endswith("\u2713"):
                    completed_task = selected_task + " \u2713"  # Unicode for checkmark symbol
                    listbox.itemconfig(index, {'bg': 'light grey', 'fg': 'grey'})
                    listbox.delete(index)
                    listbox.insert(index, completed_task)
                    update_score(1)
                    update_button_state()
                    calculate_productivity()
                    break
                else:
                    button_mark_as_done.config(state=NORMAL)


# Function to update the score
def update_score(points):
    global score
    score += points
    score_label.config(text=str(score))


class ProgressTracker:
    def __init__(self, master):
        self.master = master
        master.title("Productivity tracker")
        master.geometry("500x500")
        master.configure(background="lightblue")

        self.label = Label(master, text="Productivity:")
        self.label.pack(pady=10)

        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack(pady=10)

        self.progress_label = Label(master, text="0%")
        self.progress_label.pack(pady=5)

        self.wisdom_label = Label(master, text="Words of wisdom")
        self.wisdom_label.place(x=200, y=270)

        self.canvas = Canvas(master, width=400, height=200, bg="lightblue", highlightthickness=0)
        self.canvas.place(x=50, y=290)

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

    def update_progress(self, percentage):
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"{percentage:.2f}%")


root = Tk()
root.title("To-do list")
root.geometry("400x650+400+100")
root.resizable(False, False)

# icon
Image_icon = PhotoImage(file="task.png")  # image not popping out
root.iconphoto(False, Image_icon)

TopImage = PhotoImage(file="topbar.png")
Label(root, image=TopImage).pack()

dockImage = PhotoImage(file="dock.png")
Label(root, image=dockImage, bg="#32405b").place(x=30, y=25)

noteImage = PhotoImage(file="task.png")
Label(root, image=noteImage, bg="#32405b").place(x=30, y=25)

heading = Label(root, text="PLANNER", font="arial 20 bold", bg="#32405b")
heading.place(x=135, y=20)

# main
frame = Frame(root, width=400, height=50, bg="white")
frame.place(x=0, y=180)

# Task entry field
Label(frame, text="Task:", font="arial 10", bg="white").place(x=10, y=7)
task_entry = Entry(frame, width=12, font="arial 10", bd=0)
task_entry.place(x=60, y=10)

# Due date entry button
Label(frame, text="Starting:", font="arial 10", bg="white").place(x=230, y=7)
hour_spinbox_due = Spinbox(frame, from_=0, to=23, width=2)
hour_spinbox_due.place(x=300, y=10)
Label(frame, text=":", font="arial 10", bg="white").place(x=290, y=7)
minute_spinbox_due = Spinbox(frame, from_=0, to=59, width=2)
minute_spinbox_due.place(x=330, y=10)

# Line separating task entry and due date entry
canvas = Canvas(frame, width=400, height=1, bg="black")
canvas.place(x=0, y=35)
canvas.create_line(0, 0, 400, 0, fill="black")

# Add task button
button = Button(frame, text="+", font="arial 20 bold", width=2, bg="light blue", fg="black", bd=0, command=add_task)
button.place(x=360, y=0)

# listbox
frame1 = Frame(root, bd=3, width=700, height=280, bg="blue")
frame1.pack(pady=(160, 0))

# task list
listbox = Listbox(frame1, font=("arial", 12), width=40, height=16, bg="pink", fg="black", cursor="hand2", selectbackground="black")
listbox.pack(side=LEFT, fill=BOTH, padx=2)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# delete button
delete_icon = PhotoImage(file="delete.png")
Button(root, image=delete_icon, bd=0, command=remove_task).pack(side=LEFT, padx=50)

# mark as done button
mark_as_done_button = PhotoImage(file="tick.png")
small_mark_as_done = mark_as_done_button.subsample(3, 3)
button_mark_as_done = Button(root, image=small_mark_as_done, bd=0, command=mark_as_done)
button_mark_as_done.pack(side=RIGHT, pady=10, padx=50)

# score label
score = 0
score_label = Label(root, text=str(score), font="arial 14 bold", fg="black", bg="light blue")
score_label.place(x=360, y=585)

early_scores = 0
percentage_label = Label(root, text="Productivity: N/A", font="arial 14 bold", fg="black", bg="light blue")
percentage_label.place(x=120, y=585)

# pomodoro button
pomodoro_icon = PhotoImage(file="timer icon.png")
small_pomodoro_icon = pomodoro_icon.subsample(6, 6)
Button(root, image=small_pomodoro_icon, bd=0, command=open_pomodoro_timer).place(x=40, y=90)

# planner button
planner_icon = PhotoImage(file="planner.png")
small_planner_icon = planner_icon.subsample(6, 6)
Label(root, image=small_planner_icon, bd=0).place(x=150, y=90)

# Progress button
early_scores = 0
progress_icon = PhotoImage(file="progress.png")
small_progress_icon = progress_icon.subsample(6, 6)
Button(root, image=small_progress_icon, bd=0, command=open_progress_tracker).place(x=280, y=90)

root.mainloop()
