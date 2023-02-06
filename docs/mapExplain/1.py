def Map(func,*values):
    length = min(len(i) for i in values if hasattr(i,"__len__"))
    return *map(func, *[i if hasattr(i, "__iter__") else (i,)*length for i in values]),
# print(Map(lambda x,y:x+y, (1,2,3,4),1))
# (2, 3, 4, 5)

def addButton(widget, label, command):
    widget.add_command(label=label, command=command)

addButton(langaugeBar, "English"   ,getLang("en")),
addButton(languageBar, "Polish"    ,getLang("pl")),
addButton(languageBar, "Turkish"   ,getLang("tr")),
addButton(languageBar, "Russian"   ,getLang("ru")),
addButton(languageBar, "Ukranian"  ,getLang("uk")),
addButton(languageBar, "Czech"     ,getLang("cs")),
addButton(languageBar, "Portuguese",getLang("pt")),
addButton(languageBar, "Greek"     ,getLang("el")),
addButton(languageBar, "Italian"   ,getLang("it")),
addButton(languageBar, "Vietnamese",getLang("vi")),
addButton(languageBar, "French"    ,getLang("fr")),
addButton(languageBar, "Spanish"   ,getLang("es")),