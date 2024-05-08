import time
from tkinter import *
from tkinter import messagebox

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        master.geometry("500x400")
        master.title("Pomodoro Timer")
        master.configure(background='lightblue')

        self.pomodoro_str = StringVar()
        self.break_str = StringVar()
        self.cycles_str = StringVar()

        self.pomodoro_str.set("00")
        self.break_str.set("00")
        self.cycles_str.set("00")

        Label(master, text="Pomodoro (minutes): ").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.pomodoro_entry = Entry(master, width=5, font=("Calibri", 12, ""), textvariable=self.pomodoro_str)
        self.pomodoro_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(master, text="Break (minutes): ").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.break_entry = Entry(master, width=5, font=("Calibri", 12, ""), textvariable=self.break_str)
        self.break_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(master, text="Cycles: ").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.cycles_entry = Entry(master, width=5, font=("Calibri", 12, ""), textvariable=self.cycles_str)
        self.cycles_entry.grid(row=2, column=1, padx=5, pady=5)

        self.set_time_button = Button(master, text='Start Pomodoro', bd='5', command=self.run_timer)
        self.set_time_button.grid(row=3, columnspan=2, padx=5, pady=5)

    def validate_input(self):
        try:
            pomodoro_time = int(self.pomodoro_str.get())
            break_time = int(self.break_str.get())
            cycles = int(self.cycles_str.get())
            if pomodoro_time <= 0 or break_time <= 0 or cycles <= 0:
                messagebox.showerror("Error", "Please enter positive values.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")
            return False

    def reset_timer(self):
        self.pomodoro_str.set("00")
        self.break_str.set("00")

    def run_timer(self):
        if not self.validate_input():
            return

        cycles = int(self.cycles_str.get())

        for cycle in range(cycles):
            total_pomodoro_seconds = int(self.pomodoro_str.get()) * 60
            total_break_seconds = int(self.break_str.get()) * 60

            
            while total_pomodoro_seconds >= 0:
                minutes, seconds = divmod(total_pomodoro_seconds, 60)
                self.pomodoro_str.set("{:02d}:{:02d}".format(minutes, seconds)) 
                self.master.update()
                time.sleep(1)

                if total_pomodoro_seconds == 0:
                    break
                total_pomodoro_seconds -= 1

            
            while total_break_seconds >= 0:
                minutes, seconds = divmod(total_break_seconds, 60)
                self.break_str.set("{:02d}:{:02d}".format(minutes, seconds)) 
                self.master.update()
                time.sleep(1)

                if total_break_seconds == 0:
                    break
                total_break_seconds -= 1

            self.reset_timer()
    
if __name__ == "__main__":
    root = Tk()
    app = PomodoroTimer(root)
    root.mainloop()