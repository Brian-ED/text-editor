import tkinter as tk
font = "BQN386 Unicode"
minFontSize = 20
maxFontSize = 200
root = tk.Tk()
saveFileName = "saveFile.txt"

# justify="left"
text_box = tk.Text(root, font=(font, maxFontSize))

text_box.pack(expand = True, fill = 'both')

size = 1284, 701

def onResize(event:tk.Event):
    global size
    pos = event.x, event.y           # pos er x og y positionin av top vinstra punkt av window
    if pos == (0, 0):
        return
    size = event.width, event.height

def onPress(_):
    text = text_box.get(1.0,'end')
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

with open(saveFileName, "r", encoding="utf-8")as f:
    text_box.insert(1.0, f.read())
onPress('')

root.bind('<KeyPress>', onPress)
root.bind("<Configure>", onResize)

root.mainloop()