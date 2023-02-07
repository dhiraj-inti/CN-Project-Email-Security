#Import the required Libraries
from tkinter import *
from tkinter import ttk

#Create an instance of Tkinter frame
win= Tk()

#Set the geometry of Tkinter frame
win.geometry("750x250")

def display_text():
   global entry,win
   string= entry.get("1.0","end-1c")
   with open('mail_to_be_sent.txt','w') as f:
    f.write(string)
   win.destroy()

inp_lab = Label(win, text="Input mail:")
inp_lab.place(x=70,y=90)
label=Label(win, text="Developed by Inti Dhiraj", font=("Courier 12 bold"))
label.pack()

#Create an Entry widget to accept User Input
entry= Text(win,height=10, width= 40)
entry.focus_set()
entry.pack()

#Create a Button to validate Entry Widget
ttk.Button(win, text= "Send",width= 20, command= display_text).pack(pady=20)

win.mainloop()