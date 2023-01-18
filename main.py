from tkinter import * 
FONT = "BQN386 Unicode",
root = Tk()

text_box = Text(root, font=FONT+(20,))
text_box.pack(expand = True, fill = BOTH)

fontSize = 20

lastWidth=None

def resize(event:Event):
    global lastWidth
    if lastWidth!=None and lastWidth != event.x:
        print(event)
        text_box.configure(font=FONT+(100,))
    lastWidth=event.x

root.bind("<Configure>", resize)


root.mainloop()