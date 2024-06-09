import pygame
import tkinter as tk
from tkinter import *
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        master.title("Music Player")

        self.builtin_songs = [
            "sleepwalk.mp3",
            "where is my mind.mp3",
            "love of my life.mp3",
            "total eclipse of the heart.mp3",
            "goodnight dad.mp3"
            # Add more songs as needed
        ]

        self.playlist = []
        self.current_track = 0
        self.paused = False
        self.paused_time = 0

        pygame.init()

        self.create_widgets()
    
    def play_builtin_song(self, song_index):
        pygame.mixer.music.load(self.builtin_songs[song_index])
        pygame.mixer.music.play()
        self.track_label.config(text="Now Playing: " + self.builtin_songs[song_index])
        self.play_pause_button.config(text="Pause")
        self.paused = False


    def create_widgets(self):
        # Background Image
        bg_image = tk.PhotoImage(file="bglofi3.png")
        bg_label = tk.Label(self.master, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Buttons/Labels
        self.track_label = Label(self.master, text="No Track Playing",  width=40, bg="black", font=("Arial", 10), fg="pink")
        self.track_label.grid(row=0, column=0, columnspan=3)

        self.play_pause_button = Button(self.master, text="Play", command=self.play_pause, bg="black", fg="pink", font=("Arial", 12))
        self.play_pause_button.place(x=135, y=180)

        self.next_button = Button(self.master, text="Next", command=self.next_track, bg="black", fg="pink", font=("Arial", 12))
        self.next_button.place(x=40, y=180)

        self.prev_button = Button(self.master, text="Previous", command=self.prev_track, bg="black", fg="pink", font=("Arial", 12))
        self.prev_button.place(x=220, y=180)

        self.bg_image = bg_image

    def play_pause(self):
     if self.playlist:
        if not pygame.mixer.music.get_busy() or self.paused:
            if self.paused:
                pygame.mixer.music.unpause()  # Resume from paused position
            else:
                pygame.mixer.music.load(self.playlist[self.current_track])
                pygame.mixer.music.play()
            self.track_label.config(text="Now Playing: " + self.playlist[self.current_track])
            self.play_pause_button.config(text="Pause")
            self.paused = False
        else:
            pygame.mixer.music.pause()  # Pause the music
            self.paused_time = pygame.mixer.music.get_pos() / 1000  # Store the paused time
            self.paused = True
            self.track_label.config(text="Music Paused")
            self.play_pause_button.config(text="Play")
     else:  # If there are no tracks in the playlist, play a built-in song
        if not pygame.mixer.music.get_busy() or self.paused:
            self.play_builtin_song(0)  # Change the index as needed for different built-in songs
            self.play_pause_button.config(text="Pause")
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused_time = pygame.mixer.music.get_pos() / 1000  # Store the paused time
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
        else:
            self.current_track = (self.current_track + 1) % len(self.builtin_songs)
            self.play_builtin_song(self.current_track)

    def prev_track(self):
        if self.playlist:
            self.current_track = (self.current_track - 1) % len(self.playlist)
            self.paused_time = 0
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.track_label.config(text="Now Playing: " + self.playlist[self.current_track])
            self.play_pause_button.config(text="Pause")
            self.paused = False
        else:
            self.current_track = (self.current_track - 1) % len(self.builtin_songs)
            self.play_builtin_song(self.current_track)

def main() :
    root = tk.Tk()
    root.resizable(False,False)
    app = MusicPlayer(root)
    root.geometry("300x215")
    root.mainloop()

main()
