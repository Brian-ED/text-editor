import tkinter as tk
from tkinter.font import Font
from utilities import*

def addButton(widget, label, command):
    widget.add_command(label=label, command=command)

def getLang(lang:str):
    def f():

        selection = text_box.selection_get()
        correctedText = ac.Speller(lang=lang).autocorrect_sentence(selection)
        text_box.selection_clear()
        text_box.insert("insert", correctedText) # sel.first, sel.last

        with open(saveFileName,'w',encoding="utf-8")as f:
            f.write(text_box.get(1.0,'end-1c'))
    return f

# Buttons / widgets
def onResize(event:tk.Event):
    pos = event.x, event.y           # pos er x og y positionin av top vinstra punkt av window.
    if pos == (0, 0):                # onResize var tendra oftari en vanta, við x og y av 0, men tað er eitt glitch.
        return
    data['window']['size'] = event.width, event.height
    data['window']['pos'] = pos

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
    data['window']['width']
    f = lambda x:1550/max(1,x)
    fontSize = f(longestLine)
    print(fontSize)
    
    font.configure(size=max(minFontSize, min(maxFontSize, int(fontSize))))

def fullScreen():
    x= root.wm_attributes()
    print(x)
    isFullScreen = x[1+x.index("-fullscreen")]
    if isFullScreen:
        root.overrideredirect(data['window']['titleBar'])
    else: 
        root.overrideredirect(0)
    root.attributes("-fullscreen", not isFullScreen)
    data["window"]['fullScreen'] = not isFullScreen
    openMainMenu()

def darkModeToggle():
    if data['window', 'background'] == 'black':
        data['window']['background'] = 'white'
        data['window']['foreground'] = 'black'
    else:
        data['window']['background'] = 'black'
        data['window']['foreground'] = 'white'
    text_box.configure(background=data['window']['background'], foreground=data['window']['foreground'])
    openMainMenu()

def toggleTitleBar():
    data['window']['titleBar'] = not data['window']['titleBar']
    root.overrideredirect(data['window']['titleBar'])
    openMainMenu()

def openMainMenu(_=0):
    try:
        print("hi",menubar.index("current"))
    except:0
    if menubar.index(1):
        return menubar.delete(1,100)
    menubar.add_command(label="↩", command=lambda*x:menubar.delete(1,10))
    
    upperMenuBar=tk.Menu(menubar, tearoff=0)

    addButton(upperMenuBar,"Dark mode toggle",darkModeToggle)
    addButton(upperMenuBar,"Fullscreen",fullScreen)
    addButton(upperMenuBar,"toggle title bar",toggleTitleBar)
    languageBar = tk.Menu(upperMenuBar, tearoff=0)
    Map(addButton,languageBar,
        ["English","Polish","Turkish","Russian","Ukranian","Czech","Portuguese","Greek","Italian","Vietnamese","French","Spanish"],map(getLang,
        ["en",     "pl",    "tr",     "ru",     "uk",      "cs",   "pt",        "el",   "it",     "vi",        "fr",    "es"])
    )
    upperMenuBar.add_cascade(label="Auto Correct",menu=languageBar)
    upperMenuBar.add_separator()
    addButton(upperMenuBar,"Exit",root.quit)
    menubar.add_cascade(label="⛭", menu=upperMenuBar)

data=makeData(r"../data/data.yaml",(),[
    [['window'], {
        'size':(1284, 701),
        'pos':(0,0), 
        'foreground':'black', 
        'background':'white',
        'fullScreen':False,
        'titleBar' :True}],
    [['tabs'], {}]
])

minFontSize = 20
maxFontSize = 200
saveFileName = "../data/saveFile.txt"
root = tk.Tk()
root.geometry('+'.join(('x'.join(map(str,data['window']['size'])),*map(str,data['window']['pos']))))
root.attributes("-fullscreen", data['window']['fullScreen'])
root.overrideredirect(data['window']['titleBar'])
font = Font(family="BQN386 Unicode", size=maxFontSize)
text_box = tk.Text(root, font=font, background=data["window"]['background'], foreground=data["window"]['foreground'])
# text_box.tag_configure("default", background="black", foreground="white")
text_box.pack(side = "left", expand = True, fill = 'both')
menubar = tk.Menu(root)

with open(saveFileName, "r", encoding="utf-8")as f:
    text_box.insert(1.0, f.read())
onPress(0)

*map(root.bind, ('<KeyPress-Alt_L>', '<KeyPress>', '<KeyPress-Escape>', '<Configure>'),
                (  openMainMenu,       onPress,      openMainMenu,        onResize)),

# def onWindowClose():
#     # data['window'] = windowData
#     root.destroy()
# root.protocol("WM_DELETE_WINDOW", onWindowClose)

root.config(menu=menubar, )
root.mainloop()
