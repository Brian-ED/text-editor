import tkinter as tk
from tkinter.font import Font

root = tk.Tk()
txt="hellooo world"
t_Font = Font(family='Georgia', size=17)

lines = 20
# +4 to include the width of the border (default 1) and padding (default 1)
border = 1
padding = 1
widthpadding = border*2+padding*2
frame = tk.Frame(root, width=t_Font.measure(txt)+widthpadding, height=200)
frame.pack()

# put text box inside the frame
t = tk.Text(frame, font=t_Font)
t.insert(1.0, txt)
t.place(relwidth=1, relheight=1) # fill the available space of the frame


root.mainloop()