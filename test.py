from tkinter import *

#create the window
root = Tk()
print(max((1,2,3,4)))
#modify the root window
root.title("My Tkinter Window")
root.geometry("400x400")

#create a text entry box
entry = Entry(root, width = 25)
entry.pack()

#create a function to be called every few seconds
def get_input():
    
    var = entry.get()
    #define the variable based on the contents of the entry box
    global my_var 
    my_var = var
    print(my_var)

root.after(4, get_input)

#start the main loop
root.mainloop()