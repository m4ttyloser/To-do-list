import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time

class todolistFeat:
    def __init__(self):
        self.tasks = []
        self.total_points = 0

    def add_task(self, task, points=0, deadline = None):
        timestamp = datetime.now().strftime('HH:MM AM/PM')
        self.task.append({"task" : task, "points": points, "deadline": deadline, "timestamp": timestamp, "status": False})
    
    
    def remove_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
            self.refresh_task()
        else:
            messagebox.showerror("Error","Please pick  a task")
    

    def mark_as_done(self,task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]["done"] = True
            self.total_points += self.tasks[task_index]["points"]
        else:
            messagebox.showerror("Error", "Please pick a task")