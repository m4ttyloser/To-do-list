from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import pygame
import sqlite3
import random
from emran import *

def create_database():
    conn = sqlite3.connect("productivity.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS productivity(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            task TEXT,
            score INTEGER,
            early_score INTEGER,
            percentage REAL
        )
    """)
    conn.commit()
    conn.close()

create_database()

create_database()

def update_button_state():
    has_undone_tasks = any(not task.endswith("\u2713") for task in listbox.get(0, END))
    button_mark_as_done.config(state=NORMAL if has_undone_tasks else DISABLED)

def early_score(early_points):
    global early_scores
    early_scores += early_points

def calculate_productivity():
    global early_scores
    global score
    if early_scores > 0:
        percentage = (score / early_scores) * 100
        percentage_label.config(text=f"Productivity: {percentage:.2f}%")
    else:
        percentage = 0
        percentage_label.config(text="Productivity: N/A")
    save_productivity(percentage, score, early_scores)

def save_productivity(percentage, score, early_score):
    today = datetime.date.today()
    conn = sqlite3.connect("productivity.db")
    c = conn.cursor()
    
    # Delete existing tasks for today to avoid duplication
    c.execute("DELETE FROM productivity WHERE date = ?", (str(today),))

    # Insert tasks individually
    tasks = listbox.get(0, END)
    for task in tasks:
        c.execute("INSERT INTO productivity (date, task, score, early_score, percentage) VALUES (?, ?, ?, ?, ?)",
                  (str(today), task, score, early_score, percentage))
    
    conn.commit()
    conn.close()

def open_pomodoro_timer():
    pomodoro_window = Toplevel(root)
    pomodoro_window.title("Pomodoro timer")
    pomodoro_window.geometry("500x400")
    PomodoroTimer(pomodoro_window)

def open_progress_tracker():
    progress_tracker_window = Toplevel(root)
    progress_tracker = ProgressTracker(progress_tracker_window)
    progress_tracker.show_productivity()

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
            save_productivity((score / early_scores) * 100 if early_scores > 0 else 0, score, early_scores)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("BLIND.mp3")
    pygame.mixer.music.play()

def remove_task():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        listbox.delete(selected_task_index)
        update_button_state()
        early_score(-1)
        calculate_productivity()
        save_productivity((score / early_scores) * 100 if early_scores > 0 else 0, score, early_scores)
    else:
        messagebox.showwarning("Warning", "Please select a task to remove.")

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
                    save_productivity((score / early_scores) * 100 if early_scores > 0 else 0, score, early_scores)
                    break
                else:
                    button_mark_as_done.config(state=NORMAL)

def update_score(points):
    global score
    score += points
    score_label.config(text=str(score))
    calculate_productivity()

class ProgressTracker:
    def __init__(self, master):
        self.master = master
        master.title("Productivity tracker")
        master.geometry("500x500")


        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack(pady=10)

        self.today_label = Label(master, text="Today", font=("Arial", 10))
        self.today_label.place(x=50, y=9)

        self.progress_label = Label(master, text="0%", bg="lightblue")
        self.progress_label.pack(pady=5)

        self.additional_progress_var = DoubleVar()
        self.additional_progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate", variable=self.additional_progress_var)
        self.additional_progress_bar.pack(pady=10)

        
        self.yesterday_label = Label(master, text="Yesterday", font=("Arial", 10))
        self.yesterday_label.place(x=30, y=81)

        self.additional_progress_label = Label(master, text="0%")
        self.additional_progress_label.pack(pady=5)

        self.daily_label = Label(master, text="Daily", font=("Arial", 10))
        self.daily_label.place(x=120, y=150)

        self.daily_progress_var = DoubleVar()
        self.daily_progress_bar = ttk.Progressbar(master, orient="vertical", length=80, mode="determinate", variable=self.daily_progress_var)
        self.daily_progress_bar.place(x=126, y=170)

        
        self.weekly_label = Label(master, text="Weekly", font=("Arial", 10))
        self.weekly_label.place(x=230, y=150)

        self.weekly_progress_var = DoubleVar()
        self.weekly_progress_bar = ttk.Progressbar(master, orient="vertical", length=80, mode="determinate", variable=self.weekly_progress_var)
        self.weekly_progress_bar.place(x=245, y=170)

        
        self.monthly_label = Label(master, text="Monthly", font=("Arial", 10))
        self.monthly_label.place(x=340, y=150)

        self.monthly_progress_var = DoubleVar()
        self.monthly_progress_bar = ttk.Progressbar(master, orient="vertical", length=80, mode="determinate", variable=self.monthly_progress_var)
        self.monthly_progress_bar.place(x=355, y=170)

        self.wisdom_label = Label(master, text="Words of wisdom")
        self.wisdom_label.place(x=200, y=270)

        self.canvas = Canvas(master, width=400, height=200, highlightthickness=0)
        self.canvas.place(x=50, y=290)
        self.create_rounded_rectangle(20, 20, 380, 180, 20, outline="#333333", fill="black")
        
        self.quote_text = self.canvas.create_text(200, 100, text="", font=("Arial", 16), fill="white", width=360)

        self.quotes = [
            "Quality is not an act, it’s a habit - Aristotle",
            "When you have a dream, you’ve got to grab it and never let go - Carol Burnett",
            "You were born to win. But to be a winner, you must plan to win, prepare to win, and expect to win. - Zig Ziglar",
            "If your dreams don’t scare you, they are too small. - Richard Branson",
            "Success is the sum of all efforts repeated day-in and day-out - Robert Collier",
            "Motivation is what gets you started. Habit is what keeps you going - Jim Ryun",
            "It does not matter how slow you go as long as you do not stop - Confucius",
            "There are no secrets to success. It is the result of preparation, hard work, and learning from failure. - Colin Powell",
            "Procrastination makes easy things hard and hard things harder - Mason Cooley",
            "Making miracles is hard work. Most people give up before they happen - Sheryl Crow"
        ]

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1,
                  x2, y1 + radius, x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2,
                  x2 - radius, y2, x2 - radius, y2, x1 + radius, y2, x1 + radius, y2, x1, y2,
                  x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    

    def previous_day_average(self):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        previous = today - datetime.timedelta(days=2) 
        conn = sqlite3.connect("productivity.db")
        c = conn.cursor()

        c.execute("SELECT percentage FROM productivity WHERE date =?", (str(yesterday),))
        yesterday_percentage = c.fetchone()
        if yesterday_percentage is None:
            yesterday_percentage = 0.0
        else:
            yesterday_percentage = yesterday_percentage[0]

        c.execute("SELECT percentage FROM productivity WHERE date =?", (str(previous),))
        previous_percentage = c.fetchone()
        if previous_percentage is None:
            previous_percentage = 0.0
        else:
            previous_percentage = previous_percentage[0]

        previous_average = (yesterday_percentage + previous_percentage) / 2
        conn.close()
        return previous_average
    

    def calculate_weekly_average(self):
        today = datetime.date.today()
        last_week = [today - datetime.timedelta(days=i) for i in range(7)]
        conn = sqlite3.connect("productivity.db")
        c = conn.cursor()

        total_percentage = 0
        count = 0
        for day in last_week:
            c.execute("SELECT percentage FROM productivity WHERE date = ?", (str(day),))
            result = c.fetchone()
            if result:
                total_percentage += result[0]
                count += 1

        conn.close()
        if count > 0:
            weekly_average = total_percentage / count
        else:
            weekly_average = 0.0

        return weekly_average


    def show_productivity(self):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        previous_average = self.previous_day_average()
        weekly_average = self.calculate_weekly_average()
        conn = sqlite3.connect("productivity.db")
        c = conn.cursor()
        c.execute("SELECT percentage FROM productivity WHERE date = ?", (str(today),))
        today_percentage = c.fetchone()
        c.execute("SELECT percentage FROM productivity WHERE date = ?", (str(yesterday),))
        yesterday_percentage = c.fetchone()
        conn.close()
        
        if today_percentage:
            self.progress_var.set(today_percentage[0])
            self.progress_label.config(text=f"{today_percentage[0]:.2f}%")
        if yesterday_percentage:
            self.additional_progress_var.set(yesterday_percentage[0])
            self.additional_progress_label.config(text=f"{yesterday_percentage[0]:.2f}%")
        if previous_average:
            self.daily_progress_var.set(previous_average)
        if weekly_average:
            self.weekly_progress_var.set(weekly_average)
        
        if previous_average < 60 or weekly_average < 60:
            self.canvas.itemconfig(self.quote_text, text=random.choice(self.quotes))
        else:
            self.canvas.itemconfig(self.quote_text, text="Good job! You are productive")

        


def load_productivity():
    today = datetime.date.today()
    conn = sqlite3.connect("productivity.db")
    c = conn.cursor()
    c.execute("SELECT task, score, early_score, percentage FROM productivity WHERE date = ?", (str(today),))
    rows = c.fetchall()
    conn.close()

    global score
    global early_scores

    if rows:
        score = rows[0][1]
        early_scores = rows[0][2]
        percentage = rows[0][3]
        for row in rows:
            task = row[0]
            listbox.insert(END, task)
        score_label.config(text=str(score))
        percentage_label.config(text=f"Productivity: {percentage:.2f}%")
    else:
        score_label.config(text="0")
        percentage_label.config(text="Productivity: N/A")

root = Tk()
root.title("To-do list")
root.geometry("400x650+400+100")
root.resizable(False, False)
Image_icon = PhotoImage(file="task.png")
root.iconphoto(False, Image_icon)

TopImage = PhotoImage(file="topbar.png")
Label(root, image=TopImage).pack()

dockImage = PhotoImage(file="dock.png")
Label(root, image=dockImage, bg="#32405b").place(x=30, y=25)
noteImage = PhotoImage(file="task.png")
Label(root, image=noteImage, bg="#32405b").place(x=30, y=25)
heading = Label(root, text="PLANNER", font="arial 20 bold", bg="#32405b")
heading.place(x=135, y=20)

frame = Frame(root, width=400, height=50, bg="white")
frame.place(x=0, y=180)
Label(frame, text="Task:", font="arial 10", bg="white").place(x=10, y=7)
task_entry = Entry(frame, width=12, font="arial 10", bd=0)
task_entry.place(x=60, y=10)

Label(frame, text="Starting:", font="arial 10", bg="white").place(x=230, y=7)
hour_spinbox_due = Spinbox(frame, from_=0, to=23, width=2)
hour_spinbox_due.place(x=300, y=10)
Label(frame, text=":", font="arial 10", bg="white").place(x=290, y=7)
minute_spinbox_due = Spinbox(frame, from_=0, to=59, width=2)
minute_spinbox_due.place(x=330, y=10)
canvas = Canvas(frame, width=400, height=1, bg="black")
canvas.place(x=0, y=35)
canvas.create_line(0, 0, 400, 0, fill="black")

button = Button(frame, text="+", font="arial 20 bold", width=2, bg="light blue", fg="black", bd=0, command=add_task)
button.place(x=360, y=0)

frame1 = Frame(root, bd=3, width=700, height=280, bg="blue")
frame1.pack(pady=(160, 0))

listbox = Listbox(frame1, font=("arial", 12), width=40, height=16, bg="pink", fg="black", cursor="hand2", selectbackground="black")
listbox.pack(side=LEFT, fill=BOTH, padx=2)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

delete_icon = PhotoImage(file="delete.png")
Button(root, image=delete_icon, bd=0, command=remove_task).pack(side=LEFT, padx=50)

mark_as_done_button = PhotoImage(file="tick.png")
small_mark_as_done = mark_as_done_button.subsample(3, 3)
button_mark_as_done = Button(root, image=small_mark_as_done, bd=0, command=mark_as_done)
button_mark_as_done.pack(side=RIGHT, pady=10, padx=50)

score = 0
score_label = Label(root, text=str(score), font="arial 14 bold", fg="black", bg="light blue")
score_label.place(x=360, y=585)

early_scores = 0
percentage_label = Label(root, text="Productivity: N/A", font="arial 14 bold", fg="black", bg="light blue")
percentage_label.place(x=120, y=585)

pomodoro_icon = PhotoImage(file="timer icon.png")
small_pomodoro_icon = pomodoro_icon.subsample(6, 6)
Button(root, image=small_pomodoro_icon, bd=0, command=open_pomodoro_timer).place(x=40, y=90)

planner_icon = PhotoImage(file="planner.png")
small_planner_icon = planner_icon.subsample(6, 6)
Label(root, image=small_planner_icon, bd=0).place(x=150, y=90)

early_scores = 0
progress_icon = PhotoImage(file="progress.png")
small_progress_icon = progress_icon.subsample(6, 6)
Button(root, image=small_progress_icon, bd=0, command=open_progress_tracker).place(x=280, y=90)

load_productivity()
root.mainloop()
