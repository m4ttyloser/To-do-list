import pygame
import tkinter as tk
from tkinter import *
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        master.title("Music Setting")
        master.configure(bg="white")

        self.builtin_songs = [
            "jar of hearts.mp3",
            "where is my mind.mp3",
            "love of my life.mp3",
            "total eclipse of the heart.mp3",
            "goodnight dad.mp3",
            "everytime.mp3",
            "slipping through my fingers.mp3",
            "nothings gonna change my love for you.mp3",
            "unchained melody.mp3",
            "cant help falling in love.mp3",
            "tears in heaven.mp3",
            "my heart will go on.mp3",
            "a thousand years.mp3",
            "someone like you.mp3",
            "when we were young.mp3"
        ]

        self.playlist = []
        self.current_track = 0

        pygame.init()

        self.create_widgets()
    
    def play_song(self):
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play()
        self.update_track_label()

    def update_track_label(self):
        if self.playlist:
            self.track_label.config(text="Now Playing: " + self.playlist[self.current_track])
        else:
            self.track_label.config(text="No Track Playing")

    def add_to_playlist(self):
        selected_indices = self.song_menu.curselection()
        for index in selected_indices:
            song = self.builtin_songs[index]
            if song not in self.playlist:
                self.playlist.append(song)

    def create_widgets(self):
        # Buttons/Labels
        self.track_label = Label(self.master, text="No Track Playing",  width=40, bg="black", font=("Arial", 10), fg="white")
        self.track_label.grid(row=0, column=0, columnspan=3)

        self.song_menu = Listbox(self.master, selectmode=MULTIPLE, bg="white")
        for song in self.builtin_songs:
            self.song_menu.insert(END, song)
        self.song_menu.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.add_button = Button(self.master, text="Add to Playlist", command=self.add_to_playlist, bg="black", fg="white", font=("Arial", 12))
        self.add_button.grid(row=2, column=2, sticky="ne")

        self.play_button = Button(self.master, text="Play", command=self.play_playlist, bg="black", fg="white", font=("Arial", 12))
        self.play_button.grid(row=2, column=0)

        # Disable resizing
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.resizable(False, False)

    def play_playlist(self):
        selected_indices = self.song_menu.curselection()
        if selected_indices:
            self.playlist = [self.builtin_songs[index] for index in selected_indices]
            self.current_track = 0
            self.play_song()
        else:
            self.track_label.config(text="Please select songs.")


root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
