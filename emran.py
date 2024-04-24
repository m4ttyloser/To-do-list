import time

def pomodoro_timer(pomodoro_minutes, break_minutes, cycles):
    for cycle in range(cycles):
        # Pomodoro Session
        print("Pomodoro session starts now!")
        countdown(pomodoro_minutes)
        print("Pomodoro session ended. Take a break!")
        # Short Break
        countdown(break_minutes)
        print("Short break ended.")

    print("Pomodoro Timer completed!")

def countdown(minutes):
    seconds = minutes * 60
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r') 
        time.sleep(1)
        seconds -= 1

if __name__ == "__main__":
   
    print("Welcome to the Pomodoro Timer Helper!")
    pomodoro_minutes = int(input("Enter the duration of each Pomodoro session (in minutes): "))
    break_minutes = int(input("Enter the duration of the short break (in minutes): "))
    cycles = int(input("Enter the number of Pomodoro cycles: "))

    pomodoro_timer(pomodoro_minutes, break_minutes, cycles)
    
else :
    print("Pomodoro Error")