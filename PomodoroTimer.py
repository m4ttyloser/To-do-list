#Run from todo.py
import tkinter as tk
from tkinter import messagebox, StringVar, Label, Entry, Button, Toplevel
import pygame
from PIL import Image, ImageTk, ImageSequence
from music import MusicPlayer


class PomodoroApp:
    def __init__(self, parent):
        self.root = Toplevel(parent)
        self.root.geometry("300x200")
        self.root.title("Pomodoro Timer Setup")

        self.pomodoro_str = StringVar()
        self.break_str = StringVar()
        self.cycles_str = StringVar()

        self.pomodoro_str.set("00:00")
        self.break_str.set("00:00")
        self.cycles_str.set("00")

        Label(self.root, text="Pomodoro : ", font=("Calibri", 12)).place(relx=0.3, rely=0.3, anchor=tk.CENTER)
        self.pomodoro_entry = Entry(self.root, width=5, font=("Calibri", 12), textvariable=self.pomodoro_str)
        self.pomodoro_entry.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

        Label(self.root, text="Break : ", font=("Calibri", 12)).place(relx=0.3, rely=0.4, anchor=tk.CENTER)
        self.break_entry = Entry(self.root, width=5, font=("Calibri", 12), textvariable=self.break_str)
        self.break_entry.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

        Label(self.root, text="Cycles: ", font=("Calibri", 12)).place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        self.cycles_entry = Entry(self.root, width=5, font=("Calibri", 12), textvariable=self.cycles_str)
        self.cycles_entry.place(relx=0.7, rely=0.5, anchor=tk.CENTER)

        self.set_time_button = Button(self.root, text='Start Pomodoro', bd='2', font=("Calibri", 12), command=self.open_timer_window)
        self.set_time_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.music_playlist_button = Button(self.root, text='Music Setup', bd='2', font=("Calibri", 12), command=self.open_playlist_window)
        self.music_playlist_button.place(relx=0.8, rely=0.1, anchor=tk.CENTER)

        self.is_running = False
        self.is_work_time = True
        self.pomodoros_completed = 0
        self.current_cycle = 0

        self.root.mainloop()

    def open_timer_window(self):
        if not self.validate_input():
            return
        self.timer_window = Toplevel(self.root)
        self.timer_window.geometry("500x300")
        self.timer_window.title("Pomodoro Timer")

        self.gif_image = Image.open("3413980959-preview.gif")
        self.frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(self.gif_image)]
        self.gif_label = Label(self.timer_window)
        self.gif_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.animate(0)

        self.timer_label = Label(self.timer_window, text="Timer", font=("Calibri", 40))
        self.timer_label.place(x=10, y=10, anchor=tk.NW)

        self.cycle_label = Label(self.timer_window, text="Cycle: {}".format(self.cycles_str.get()), font=("Calibri", 12))
        self.cycle_label.place(x=10, y=70, anchor=tk.NW)

        self.start_button = tk.Button(self.timer_window, text="Start", command=self.start_timer)
        self.start_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        pygame.mixer.init()
        self.alarm_sound = pygame.mixer.Sound("Alarm-clock-bell-ringing-sound-effect.wav")

    def open_playlist_window(self):
        self.player_window = Toplevel(self.root)
        self.music_player = MusicPlayer(self.player_window)

    def animate(self, counter):
        frame = self.frames[counter]
        counter += 1
        if counter == len(self.frames):
            counter = 0
        self.gif_label.configure(image=frame)
        self.timer_window.after(100, self.animate, counter)

    def start_timer(self):
        if not self.is_running:
            self.work_time = self.parse_time(self.pomodoro_str.get()) if self.is_work_time else self.work_time
            self.break_time = self.parse_time(self.break_str.get()) if not self.is_work_time else self.break_time
            self.cycles = int(self.cycles_str.get())

        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.update_timer()
        self.play_music_from_playlist()

    def play_music_from_playlist(self):
        self.music_player.play_playlist()

    def stop_timer(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)

    def validate_input(self):
        try:
            self.work_time = self.parse_time(self.pomodoro_str.get())
            self.break_time = self.parse_time(self.break_str.get())
            self.cycles = int(self.cycles_str.get())
            if self.work_time <= 0 or self.break_time <= 0 or self.cycles <= 0:
                messagebox.showerror("Error", "Please enter positive values.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Error", "Please enter valid time in MM:SS format and integer for cycles.")
            return False

    def parse_time(self, time_str):
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds

    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                    self.is_work_time = False
                    self.break_time = self.parse_time(self.break_str.get())
                    self.alarm_sound.play()
                    self.music_player.stop_song()
                    messagebox.showinfo("Break Time", "Take a break!")
            else:
                self.break_time -= 1
                if self.break_time == 0:
                    self.current_cycle += 1
                    self.cycles_str.set(str(int(self.cycles_str.get()) - 1))
                    if self.current_cycle >= self.cycles:
                        self.stop_timer()
                        self.alarm_sound.play()
                        messagebox.showinfo("Pomodoro Completed", "Congratulations! You've completed all cycles.")
                        return
                    self.is_work_time = True
                    self.work_time = self.parse_time(self.pomodoro_str.get())
                    self.music_player.play_playlist()
                    self.alarm_sound.play()  # Added alarm sound for break end
                    messagebox.showinfo("Work Time", "Get back to work!")

            minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.cycle_label.config(text="Cycle: {}".format(self.cycles_str.get()))
            self.timer_window.after(1000, self.update_timer)
