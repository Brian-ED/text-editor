from tkinter import * 
font = "BQN386 Unicode"
fontSize = 20
lastSize = [0,0]
lastPos = [0,0]

root = Tk()

text_box = Text(root, font=(font,20))
text_box.pack(expand = True, fill = BOTH)

def resize(event:Event):
    if (event.x, event.y)==(0, 0):
        return
    print(event)

root.bind("<Configure>", resize)
root.mainloop()
