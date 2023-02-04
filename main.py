

import tkinter as tk
from functools import reduce
import autocorrect as ac

# Funcs

def rgb(rgb):
    return "#%02x%02x%02x" % rgb 

def d():0

def makeMenu(buttons):
    def f(x,y):
        if y: x.add_command(label=y[0], command=y[1])
        else: x.add_separator()
        return x
    return reduce(f, buttons, tk.Menu(menubar, tearoff=0))


def onResize(event:tk.Event):
    global size
    pos = event.x, event.y           # pos er x og y positionin av top vinstra punkt av window
    if pos == (0, 0):
        return
    size = event.width, event.height

def onPress(_):     
    print(_)   
    text = text_box.get(1.0,'end-1c')
    with open(saveFileName,'w',encoding="utf-8")as f:
        f.write(text)
    
    longestLine = max(map(len, text.split('\n')))

    # f(charLength, screenWidth) = fontSizeNeeded
    # f(8, 1284) = 200
    # f(14,1284) = 110
    # f(54,1284) = 30
    # f(31,1284) = 50
    # f(28,665 ) = 30
    # f(8, 664 ) = 100
    # f(15,847 ) = 70
    f = lambda x:1550/max(1,x)    
    
    print(f'{size=}')
    fontSize = f(longestLine)
    print(fontSize)
    text_box.configure(font=(font,max(minFontSize, min(maxFontSize, int(fontSize)))))

def fullScreen():
    global isFullScreen
    isFullScreen=not isFullScreen
    root.attributes("-fullscreen", isFullScreen)

def autoCorrectCmd():
    correctedText = ac.Speller(lang=lang).autocorrect_sentence(text_box.get(1.0,'end-1c'))
    with open(saveFileName,'w',encoding="utf-8")as f:
        f.write(correctedText)
    text_box.replace(1.0,1000.0, correctedText)

def openMainMenu(_, menuState=None):
    if menubar.index(1):
        return menubar.delete(1,10)
    menubar.add_command(label="return", command=lambda*x:menubar.delete(1,10))
    menubar.add_cascade(label="Settings", menu=makeMenu([
        ["Language",d],
        ["Fullscreen",fullScreen],
        ["Auto Correct", autoCorrectCmd],
        [],
        ["Exit", root.quit]
    ]))

def altPressed(x):
    openMainMenu(x, menuState=0)


# vars
font = "BQN386 Unicode"
size = 1284, 701
minFontSize = 20
maxFontSize = 200
saveFileName = "saveFile.txt"
lang="en"
isFullScreen=0

root = tk.Tk()

text_box = tk.Text(root, font=(font, maxFontSize))
text_box.pack(expand = True, fill = 'both')

menubar = tk.Menu(root)

with open(saveFileName, "r", encoding="utf-8")as f:
    text_box.insert(1.0, f.read())
onPress(0)

*map(root.bind, ('<KeyPress-Alt_L>', '<KeyPress>', '<KeyPress-Escape>', '<Configure>'),
                (altPressed,         onPress,      openMainMenu,        onResize)),

root.config(menu=menubar, background=rgb((12,31,200)))
root.mainloop()

# Get selected text
# text_box.selection_get()
