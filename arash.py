import pygame
import tkinter as tk
from tkinter import *
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        master.title("Music Player")

        self.playlist = []
        self.current_track = 0
        self.paused = False
        self.paused_time = 0

        pygame.init()

        self.create_widgets()

    def create_widgets(self):
        # Background Image
        bg_image = tk.PhotoImage(file="bglofi3.png")
        bg_label = tk.Label(self.master, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Buttons/Labels
        self.track_label = Label(self.master, text="No Track Playing",  width=40, bg="black", font=("Arial", 10), fg="pink")
        self.track_label.grid(row=0, column=0, columnspan=3)

        self.add_button = Button(self.master, text="Add", command=self.add_track, bg="black", fg="pink", font=("Arial", 12))
        self.add_button.place(x=257, y=22)

        self.play_pause_button = Button(self.master, text="Play", command=self.play_pause, bg="black", fg="pink", font=("Arial", 12))
        self.play_pause_button.place(x=135, y=180)

        self.next_button = Button(self.master, text="Next", command=self.next_track, bg="black", fg="pink", font=("Arial", 12))
        self.next_button.place(x=40, y=180)

        self.prev_button = Button(self.master, text="Previous", command=self.prev_track, bg="black", fg="pink", font=("Arial", 12))
        self.prev_button.place(x=220, y=180)

        self.bg_image = bg_image

    def add_track(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3")])
        if file_path:
            self.playlist.append(file_path)

    def play_pause(self):
        if self.playlist:
            if not pygame.mixer.music.get_busy() or self.paused:
                pygame.mixer.music.load(self.playlist[self.current_track])
                pygame.mixer.music.play(start=self.paused_time)
                self.track_label.config(text="Now Playing: " + self.playlist[self.current_track])
                self.play_pause_button.config(text="Pause")
                self.paused = False
            else:
                self.paused_time = pygame.mixer.music.get_pos() / 1000  # Get the elapsed time in seconds
                pygame.mixer.music.pause()
                self.paused = True
                self.track_label.config(text="Music Paused")
                self.play_pause_button.config(text="Play")

    def next_track(self):
        if self.playlist:
            self.current_track = (self.current_track + 1) % len(self.playlist)
            self.paused_time = 0
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.track_label.config(text="Now Playing: " + self.playlist[self.current_track])
            self.play_pause_button.config(text="Pause")
            self.paused = False

    def prev_track(self):
        if self.playlist:
            self.current_track = (self.current_track - 1) % len(self.playlist)
            self.paused_time = 0
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.track_label.config(text="Now Playing: " + self.playlist[self.current_track])
            self.play_pause_button.config(text="Pause")
            self.paused = False

def main() :
    root = tk.Tk()
    root.resizable(False,False)
    app = MusicPlayer(root)
    root.geometry("300x215")
    root.mainloop()

main()
