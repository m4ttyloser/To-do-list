import time
from tkinter import *
from tkinter import messagebox

# Create the interface object
clock_window = Tk()
clock_window.geometry("300x200")
clock_window.title("Pomodoro Timer")
clock_window.configure(background='lightblue')

# Declare variables for Pomodoro, Break, and Cycles
pomodoro_str = StringVar()
break_str = StringVar()
cycles_str = StringVar()

# Set default values
pomodoro_str.set("00")
break_str.set("00")
cycles_str.set("00")

# Function to validate user input
def validate_input():
    try:
        pomodoro_time = int(pomodoro_str.get())
        break_time = int(break_str.get())
        cycles = int(cycles_str.get())
        if pomodoro_time <= 0 or break_time <= 0 or cycles <= 0:
            messagebox.showerror("Error", "Please enter positive values.")
            return False
        return True
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers.")
        return False

# Function to run the countdown timer
def run_timer():
    if not validate_input():
        return

    total_pomodoro_seconds = int(pomodoro_str.get()) * 60
    total_break_seconds = int(break_str.get()) * 60
    cycles = int(cycles_str.get())

    for cycle in range(cycles):
        # Pomodoro Timer
        while total_pomodoro_seconds >= 0:
            minutes, seconds = divmod(total_pomodoro_seconds, 60)

            pomodoro_str.set("{:02d}".format(minutes))

            clock_window.update()
            time.sleep(1)

            if total_pomodoro_seconds == 0:
                break

            total_pomodoro_seconds -= 1

        # Break Timer
        while total_break_seconds >= 0:
            minutes, seconds = divmod(total_break_seconds, 60)

            break_str.set("{:02d}".format(minutes))

            clock_window.update()
            time.sleep(1)

            if total_break_seconds == 0:
                break

            total_break_seconds -= 1

# Entry for Pomodoro time
Label(clock_window, text="Pomodoro (minutes): ").grid(row=0, column=0, padx=5, pady=5, sticky="e")
pomodoro_entry = Entry(clock_window, width=5, font=("Calibri", 12, ""), textvariable=pomodoro_str)
pomodoro_entry.grid(row=0, column=1, padx=5, pady=5)

# Entry for Break time
Label(clock_window, text="Break (minutes): ").grid(row=1, column=0, padx=5, pady=5, sticky="e")
break_entry = Entry(clock_window, width=5, font=("Calibri", 12, ""), textvariable=break_str)
break_entry.grid(row=1, column=1, padx=5, pady=5)

# Entry for Cycles
Label(clock_window, text="Cycles: ").grid(row=2, column=0, padx=5, pady=5, sticky="e")
cycles_entry = Entry(clock_window, width=5, font=("Calibri", 12, ""), textvariable=cycles_str)
cycles_entry.grid(row=2, column=1, padx=5, pady=5)

# Set Time button
set_time_button = Button(clock_window, text='Start Pomodoro', bd='5', command=run_timer)
set_time_button.grid(row=3, columnspan=2, padx=5, pady=5)

clock_window.mainloop()
