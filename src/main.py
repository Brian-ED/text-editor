import tkinter as tk
from tkinter.font import Font
from utilities import *
import autocorrect as ac

def addButton(widget:tk.Menu, label, command):
    widget.add_command(label = label, command = command)

def getLang(lang:str):
    def f():
        selection = text_box.selection_get()
        correctedText = ac.Speller(lang = lang).autocorrect_sentence(selection)
        text_box.selection_clear()
        text_box.insert("insert", correctedText) # sel.first, sel.last

        with open(SAVE_FILE, "w", encoding = "utf-8")as f:
            f.write(text_box.get(1.0, "end-1c"))
    return f

def toggleWrap():
    data["window"]["wrap"]

# Buttons / widgets
def onResize(event:tk.Event):
    pos = event.x, event.y           # pos er x og y positionin av top vinstra punkt av window.
    if pos == (0, 0):                # onResize var tendra oftari en vanta, við x og y av 0, men tað er eitt glitch.
        return
    data["window"]["size"] = event.width, event.height
    data["window"]["pos"] = pos

def onPress(_ = 0):
    print("hi")
    text = text_box.get(1.0, "end-1c")
    longestLine = max(1, *map(measureFont.measure, text.split("\n")))
    
    border = 1
    padding = 1
    widthpadding = border*2+padding*2
    space = data["window"]["size"][0]-widthpadding

    fontSize = space/1276/longestLine*30000
    
    font.configure(size = max(MIN_FONT_SIZE, min(MAX_FONT_SIZE, int(fontSize))))
    with open(SAVE_FILE, "w", encoding = "utf-8")as f:
        f.write(text)

def fullScreen():
    x = window.wm_attributes()
    isFullScreen = x[1+x.index("-fullscreen")]
    if isFullScreen:
        window.overrideredirect(data["window"]["titleBar"])
    else:
        window.overrideredirect(0)
    window.attributes("-fullscreen", not isFullScreen)
    data["window"]["fullScreen"] = not isFullScreen
    openMainMenu()

def darkModeToggle():
    if data["window", "background"] == "black":
        data["window"]["background"] = "white"
        data["window"]["foreground"] = "black"
    else:
        data["window"]["background"] = "black"
        data["window"]["foreground"] = "white"
    text_box.configure(background = data["window"]["background"], foreground = data["window"]["foreground"])
    openMainMenu()

def toggleTitleBar():
    data["window"]["titleBar"] = not data["window"]["titleBar"]
    window.overrideredirect(data["window"]["titleBar"])
    openMainMenu()

def openMainMenu(_ = 0):
    if menubar.index(1):
        return menubar.delete(1, 100)
    menubar.add_command(label = "↩", command = lambda*x:menubar.delete(1, 10))
    
    topMenuBar  = tk.Menu(menubar,    tearoff = 0)
    languageBar = tk.Menu(topMenuBar, tearoff = 0)

    Map(addButton)(topMenuBar,
        ("Dark mode toggle", "Fullscreen", "toggle title bar"),
        ( darkModeToggle,    fullScreen,  toggleTitleBar)
    )
    Map(addButton)(languageBar, *languages)
    topMenuBar.add_cascade(label = "Auto Correct", menu = languageBar)
    topMenuBar.add_separator()
    addButton(topMenuBar, "Exit", window.quit)
    menubar.add_cascade(label = "⛭", menu = topMenuBar)

def moveCurserUp(_):
    #  window.event_generate("<Motion>", warp = True, x = 50, y = 50)
    text_box.mark_set("insert", (lambda x, y:f"{x-(y == 0)}.{(y == 0)*10000000+y-1}")(*map(int, text_box.index("insert").split("."))))

def showRightClickMenu(e:tk.Event):
    rightClickMenu.entryconfigure("Cut",   command = lambda: e.widget.event_generate("<<Cut>>"))
    rightClickMenu.entryconfigure("Copy",  command = lambda: e.widget.event_generate("<<Copy>>"))
    rightClickMenu.entryconfigure("Paste", command = lambda: e.widget.event_generate("<<Paste>>"))
    rightClickMenu.tk.call("tk_popup", rightClickMenu, e.x_root, e.y_root)

# general saved data 
data = makeData(r"../data/data.yaml", (), [
    [["window"], {
        "size"      :(1284, 701),
        "pos"       :(-10, 0),  # No idea why, but to make the window appear centered it has to be shifted by -10
        "foreground":"black",
        "background":"white",
        "fullScreen":False,
        "titleBar"  :False,
        "wrap"      :False}],
    [["tabs"], {}]
])

languages =  (["English", "Polish", "Turkish", "Russian", "Ukranian", "Czech", "Portuguese", "Greek", "Italian", "Vietnamese", "French", "Spanish"],
 map(getLang, ["en",      "pl",     "tr",      "ru",      "uk",       "cs",    "pt",         "el",    "it",      "vi",         "fr",     "es"])
)

SAVE_FILE = "../data/saveFile.txt"
MIN_FONT_SIZE, MAX_FONT_SIZE = 20, 200
FONT = "BQN386 Unicode"
window = tk.Tk()
window.geometry("+".join(("x".join(map(str, data["window"]["size"])), *map(str, data["window"]["pos"]))))
window.attributes("-fullscreen", data["window"]["fullScreen"])
window.overrideredirect(data["window"]["titleBar"])
font = Font(family = FONT, size = MAX_FONT_SIZE)
measureFont = Font(family = FONT, size = 25)

# Right click menu
rightClickMenu = tk.Menu(window, tearoff = 0)
Map(addButton)(rightClickMenu, ["Cut", "Copy", "Paste"], lambda:0)

text_box = tk.Text(window, undo = True, wrap = "none", font = font, background = data["window"]["background"], foreground = data["window"]["foreground"])
text_box.pack(side = "left", expand = True, fill = "both")
text_box.bind_class("Entry", "<Button-3><ButtonRelease-3>", showRightClickMenu)

menubar = tk.Menu(window)

# Create save file if it doesn't exist:
if not os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "w") as f:0
with open(SAVE_FILE, "r", encoding = "utf-8")as f:
    text_box.insert(1.0, f.read())
onPress()

*map(window.bind, ("<KeyPress-Alt_L>", "<KeyPress>", "<KeyPress-Escape>", "<Configure>", "<Control-g>"),
                  (  openMainMenu,       onPress,      openMainMenu,        onResize,     moveCurserUp)),

a = tk.Listbox(window, selectmode = "multiple")
window.config(menu = menubar)
window.mainloop()
