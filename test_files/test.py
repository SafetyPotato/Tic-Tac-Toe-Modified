import tkinter as tk
from tkinter import ttk




scores = [54,67,48,99,27]

for i, score in enumerate(scores):
   print(i)


'''
root = tk.Tk()

root.geometry("500x500")

button1 = tk.Button(root, text = "button1")
button1.grid(row = 0, column = 0, sticky = "W")

button2 = tk.Button(root, text = "button2")
button2.grid(row = 0, column = 1, sticky = "E")

root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 2)

root.mainloop()
'''

#button2.grid_rowconfigure(0, weight = 20)


root = tk.Tk()

columnHeadings = ("Heading 1", "Heading 2")

def printMsg():
    print("Ok")

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

label1 = tk.Label(frame, text="Label here")
button1 = tk.Button(frame, text="Yes", width=2, command=printMsg)
button2 = tk.Button(frame, text="No", width=2, command=printMsg)
treeview1 = ttk.Treeview(frame, columns=columnHeadings, show='headings')

label1.grid(row=0, column=0, columnspan=1)
button1.grid(row=0, column=1)
button2.grid(row=0, column=2)
treeview1.grid(row=1,column=0, columnspan=4, sticky="nsew")

frame.grid_columnconfigure(3, weight=1)
frame.grid_rowconfigure(1, weight=1)

root.mainloop()






