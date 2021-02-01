import tkinter as tk
from tkinter import ttk


root = tk.Tk()

columnHeadings = ("Heading 1", "Heading 2")

def printMsg():
    print("Ok")

frame = ttk.Frame(root).grid(row=0, column=0)

label1 = tk.Label(frame, text="Label here").grid(row=0, column=0, columnspan=1)
button1 = tk.Button(frame, text="Yes", width=2, command=printMsg).grid(row=0, column=1)
button2 = tk.Button(frame, text="No", width=2, command=printMsg).grid(row=0, column=2)
#Label and buttons too far apart
#treeview1 = ttk.Treeview(frame, columns=columnHeadings, show='headings').grid(row=1,column=0, columnspan=3)

#Right distance but that's a huge columnspan
treeview1 = ttk.Treeview(frame, columns=columnHeadings, show='headings').grid(row=1,column=0, columnspan=100)

root.mainloop()

def gamer(string):
    print(string)