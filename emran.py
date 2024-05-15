import time 
import pygame
import tkinter as tk
from tkinter import *
from tkinter import messagebox

class PomodoroTimer:
    def _init_(self, master):
        self.master = master
        master.geometry("500x310")
        master.title("Pomodoro Timer")
        
       
        self.bg_image = PhotoImage(file="class.png")

        self.bg_label = Label(master, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
      
        self.pomodoro_str = StringVar()
        self.break_str = StringVar()
        self.cycles_str = StringVar()

        self.pomodoro_str.set("00:00")
        self.break_str.set("00:00")
        self.cycles_str.set("00")

        Label(master, text="Pomodoro (min): ", font=("Calibri", 12)).place(relx=0.4, rely=0.3, anchor=CENTER)
        self.pomodoro_entry = Entry(master, width=5, font=("Calibri", 12), textvariable=self.pomodoro_str)
        self.pomodoro_entry.place(relx=0.6, rely=0.3, anchor=CENTER)

        Label(master, text="Break (min): ", font=("Calibri", 12)).place(relx=0.4, rely=0.4, anchor=CENTER)
        self.break_entry = Entry(master, width=5, font=("Calibri", 12), textvariable=self.break_str)
        self.break_entry.place(relx=0.6, rely=0.4, anchor=CENTER)

        Label(master, text="Cycles: ", font=("Calibri", 12)).place(relx=0.4, rely=0.5, anchor=CENTER)
        self.cycles_entry = Entry(master, width=5, font=("Calibri", 12), textvariable=self.cycles_str)
        self.cycles_entry.place(relx=0.6, rely=0.5, anchor=CENTER)

        self.set_time_button = Button(master, text='Start Pomodoro', bd='2', font=("Calibri", 12), command=self.start_timer)
        self.set_time_button.place(relx=0.5, rely=0.6, anchor=CENTER)

    def validate_input(self):
        try:
            pomodoro_time = int(self.pomodoro_str.get().split(":")[0])
            break_time = int(self.break_str.get().split(":")[0])
            cycles = int(self.cycles_str.get())
            if pomodoro_time <= 0 or break_time <= 0 or cycles <= 0:
                messagebox.showerror("Error", "Please enter positive values.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")
            return False

    def reset_timer(self):
        self.pomodoro_str.set("00:00")
        self.break_str.set("00:00")

    def start_timer(self):
        if not self.validate_input():
            return

        cycles = int(self.cycles_str.get())
        pomodoro_time = int(self.pomodoro_str.get().split(":")[0]) * 60
        break_time = int(self.break_str.get().split(":")[0]) * 60
        

        for cycle in range(cycles):
            self.run_timer(pomodoro_time, "Pomodoro")
            self.run_timer(break_time, "Break")

        
            cycles_left = int(self.cycles_str.get()) - (cycle + 1)
            self.cycles_str.set("{:02d}".format(cycles_left))
            self.master.update()

            if cycles_left == 0:
                break

    def run_timer(self, total_seconds, timer_type):
        while total_seconds > 0:
            minutes, seconds = divmod(total_seconds, 60)
            if timer_type == "Pomodoro":
                self.pomodoro_str.set("{:02d}:{:02d}".format(minutes, seconds))
            else:
                self.break_str.set("{:02d}:{:02d}".format(minutes, seconds))
            self.master.update()
            time.sleep(1)
            total_seconds -= 1