from tkinter import *
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


root = Tk()
root.title("TO-do list")
root.resizable(False,False)

task_list = []

#icon
Image_icon = PhotoImage(file = "image/task.png") # image not popping out
root.iconphoto(False,Image_icon)

TopImage = PhotoImage(file = "image/tobar.png")
Label(root,image = TopImage).pack()

dockImage = PhotoImage(file ="image/dock.png")
Label(root,image = dockImage,bg="#32405b").place(x=30,y=25)

noteImage = PhotoImage(file = "image/task.png")
Label(root,image = noteImage,bg="#32405b").place(x=30,y=25)

heading = Label(root,text="ALL TASK",font = "arial 20 bold",fg="white",bg="#32405b")
heading.lace(x=130,y=20)

#main
frame = Frame(root,width=400, height = 50,bg = "white")
frame.place(x=0,y=180)

task = StringVar()
task_entry = Entry(frame,width = 18,font = "arial 20",bd=0)
task_entry.place(x = 10, y = 7)


button = Button(frame,text = "ADD",font = "arial 20 bold", width = 6, bg = "5a95ff",fg = "#fff", bd =0)
button.place(x=300, y= 0)

#listbox
frame1 = Frame(root,bd=3,width=700,height=280,bg="32405b")
frame1.pack(pady=(160,0))

listbox = Listbox(frame1, font=("arial",12),width=40,height=16,bg="#32405b",fg="white",cursor="hand2",selectbackground="#5a95ff")
listbox.pack(side = LEFT, fill=BOTH,padx=2)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT,fill =BOTH)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

#delete
delete_icon = PhotoImage(file = "image/delete.png")
Button(root,image=delete_icon,bd=0).pack(side=BOTTOM,pady=13)



root.mainloop()