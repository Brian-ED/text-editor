import tkinter as tk
import asyncio
font = "BQN386 Unicode"
minFontSize = 20
maxFontSize = 200
root = tk.Tk()
saveFileName = "saveFile.txt"

# justify="left"
text_box = tk.Text(root, font=(font, maxFontSize))

text_box.pack(expand = True, fill = 'both')


def onResize(event:tk.Event):
    pos = event.x, event.y           # pos er x og y positionin av top vinstra punkt av window
    size = event.width, event.height
    if pos == (0, 0):
        return
    print(pos)

def onPress(_):
    text = text_box.get(1.0,'end')
    with open(saveFileName,'w',encoding="utf-8")as f:
        f.write(text)
    
    longestLine = max(map(len, text.split('\n')))

    # f(charLength) = fontSizeNeeded
    # f(8) = 200
    # f(14) = 110
    # f(54) = 30
    # f(31) = 50
    f = lambda x:1550/max(1,x)
    fontSize = f(longestLine)
    print(fontSize)

    text_box.configure(font=(font,max(minFontSize, min(maxFontSize, int(fontSize)))))

with open(saveFileName, "r", encoding="utf-8")as f:
    text_box.insert(1.0, f.read())
onPress('')

root.bind('<KeyPress>', onPress)
root.bind("<Configure>", onResize)

root.mainloop()