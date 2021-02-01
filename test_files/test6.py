from tkinter import *
from functools import partial



class test(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.frame = Frame(self)
        self.frame.pack()
        self.button_identities = []

        self.run()
        print(self.button_identities)

    def change(self, n):
        # function to get the index and the identity (bname)
        print(n)
        bname = (self.button_identities[n])
        bname.configure(text = "clicked")

    def run(self):
        for i in range(5):
            # creating the buttons, assigning a unique argument (i) to run the function (change)
            button = Button(self.frame, width=10, text=str(i), command=partial(self.change, i))
            button.pack()
            # add the button's identity to a list:
            self.button_identities.append(button)


# just to show what happens:
win = test()
win.mainloop()

