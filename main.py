from tkinter import *
from tkinter import messagebox

def add_task():
    task_text = task_entry.get()
    if task_text:
        listbox.insert(END, task_text)
        task_entry.delete(0, END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")


def remove_task():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        listbox.delete(selected_task_index)
    else:
        messagebox.showwarning("PLease select a task to remove")

def mark_as_done():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        selected_task = listbox.get(selected_task_index)
        if not selected_task.endswith("\u2713"):
            completed_task = selected_task + " \u2713"  
            listbox.itemconfig(selected_task_index, {'bg':'light grey', 'fg':'grey'})
            listbox.delete(selected_task_index)
            listbox.insert(selected_task_index, completed_task)
            update_score(1)  
            button_mark_as_done.config(state=DISABLED)
        else:
            button_mark_as_done.config(state=NORMAL)


def update_score(points):
    global score
    score += points
    score_label.config(text=str(score))


root = Tk()
root.title("To-do list")
root.geometry("400x650+400+100")
root.resizable(False,False)


#icon
Image_icon = PhotoImage(file = "task.png") # image not popping out
root.iconphoto(False,Image_icon)

TopImage = PhotoImage(file = "topbar.png")
Label(root,image = TopImage).pack()

dockImage = PhotoImage(file ="dock.png")
Label(root,image = dockImage,bg="#32405b").place(x=30,y=25)

noteImage = PhotoImage(file = "task.png")
Label(root,image = noteImage,bg="#32405b").place(x=30,y=25)

heading = Label(root,text="PLANNER",font = "arial 20 bold",fg="white",bg="light blue")
heading.place(x=130,y=20)

#main
frame = Frame(root,width=400, height = 50,bg = "white")
frame.place(x=0,y=180)

task_entry = Entry(frame,width = 18,font = "arial 20",bd=0)
task_entry.place(x = 10, y = 7)

#add task button
button = Button(frame,text = "+",font = "arial 20 bold", width = 6, bg = "light blue",fg = "black", bd =0, command = add_task)
button.place(x=300, y= 0)

#listbox
frame1 = Frame(root,bd=3,width=700,height=280,bg="blue")
frame1.pack(pady=(160,0))

#task list
listbox = Listbox(frame1, font=("arial",12),width=40,height=16,bg="pink",fg="black",cursor="hand2",selectbackground="black")
listbox.pack(side = LEFT, fill=BOTH,padx=2)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT,fill =BOTH)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

#delete button
delete_icon = PhotoImage(file="delete.png")
Button(root, image=delete_icon, bd=0, command=remove_task).pack(side=LEFT,padx = 50)


#mark as done button
mark_as_done_button = PhotoImage(file="tick.png")
small_mark_as_done = mark_as_done_button.subsample(3, 3)  
button_mark_as_done = Button(root, image=small_mark_as_done, bd=0, command = mark_as_done )
button_mark_as_done.pack(side=RIGHT, pady=10, padx = 50)

#pomodoro button
pomodoro_icon = PhotoImage(file="timer icon.png")
small_pomodoro_icon = pomodoro_icon.subsample(6, 6)
Button(root, image=small_pomodoro_icon, bd=0,).place(x=60, y= 90)

#Progress button
progress_icon = PhotoImage(file="progress.png")
small_progress_icon = progress_icon.subsample(6, 6)
Button(root, image=small_progress_icon, bd=0,).place(x=240, y= 90)

#score label
score = 0
score_label = Label(root, text=str(score), font="arial 14 bold", fg="black", bg="light blue")
score_label.place(x=360, y=585)




root.mainloop()