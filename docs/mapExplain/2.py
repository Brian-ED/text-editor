def addButton(widget, label, command):
    widget.add_command(label=label, command=command)

Map(addButton,languageBar, ["English","Polish","Turkish","Russian","Ukranian","Czech","Portuguese","Greek","Italian","Vietnamese","French","Spanish"],
               map(getLang,["en",     "pl",    "tr",     "ru",     "uk",      "cs",   "pt",        "el",   "it",     "vi",        "fr",    "es"])
)