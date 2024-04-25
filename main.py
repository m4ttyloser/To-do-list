import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time

class todolistFeat:
    def __init__(self):
        self.task = []
        self.total_points = 0

    def add_task(self, task, points=0, deadline = None):
        timestamp = datetime.now().strftime('HH:MM AM/PM')
        self.task.append({"task" : task, "points": points, "deadline": deadline, "timestamp": timestamp, "status": False})
        

    def remove_task(todo_list, task):
        if remove in todo_list:
            todo_list.remove(remove)
            print('task removed')
        else:
            print('Task not found!')


    def show_task(todo_list):
        print('Your task:')
        z = 1
        for x in todo_list:
            print(f'{z}.{x}')
            z += 1

