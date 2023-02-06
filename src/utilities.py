import yaml
from functools import reduce
import autocorrect as ac

def rgb(rgb):
    return "#%02x%02x%02x" % rgb 

def nothing():0

def Map(func,*values):
    length = min(len(i) for i in values if hasattr(i,"__len__"))
    return *map(func, *[i if hasattr(i, "__iter__") else (i,)*length for i in values]),
# print(Map(lambda x,y:x+y, (1,2,3,4),1))
# (2, 3, 4, 5)

def unlink(x):
    if type(x)==makeData:
        return unlink(x.unlink())
    if type(x)==dict:
        return {i:unlink(x[i])for i in x}
    if type(x)==str:
        return x
    if hasattr(x, "__iter__"):
        return[*map(unlink, x)]
    return x

# used for the data class
def write(fAsStr):
    def f(s,*a,**kw):
        with open(s.filePath,"r", encoding="utf-8") as f:
            data=yaml.unsafe_load(f.read())
        tempData=data # Create tempData, which will be indexed by the path var which is tuple[indexes] where indexes is s.path
        for i in s.path: # Reach into path, by redefining tempData further and further inside the data dictionary
            if type(i)!=slice and type(tempData)==dict and i not in tempData: # Handling of if index wasn't found (Initiates checking default values)
                for path, defaultsDict in s.defaults:                         # Go through the defaults at the spesific paths set by __init__
                    if all(( # Check if s.path and path are compatible with eachother
                        hasattr(i, "__hash__") and i.__hash__!=None, 
                        i in defaultsDict,
                        len(s.path)==len(path)+1,
                        *map(lambda i,j:i in (None, j), path, s.path)
                    )):
                        tempData[i] = unlink((lambda i:i() if callable(i)else i)(defaultsDict[i])) # If path and s.path are compatible, execute this. This means a default value was found for indexing this data.
                        break       # Break out because the value at location was already found
                else: tempData[i]={}# If indexing an unexistant item, and no default was found, just use empty dictionary.
            tempData=tempData[i]    # Index into data one more time
        
        # Handling of the method which was activated for the data object, and activating that method instead on tempData.
        if fAsStr == "unlink":      # If the method used was .unlink was activated, then you wanna just return tempData which would make this unlinked from the data file
            return tempData
        reset  = lambda i:i.unlink()if type(i)==makeData else i # reset funciton to apply to args. turns dataclass into whatever is inside of it. if removed, causes errors like int has no __iadd__ method.
        args   = *map(reset, a),
        kwargs = {i:reset(kw[i]) for i in kw}
        if hasattr(tempData,fAsStr): # if tempData.fAsStr exists, activate the method on the args and kwargs
            x = getattr(tempData, fAsStr)(*args,**kwargs)
        elif hasattr(args[0], attr if (attr:={"__radd__":"__add__"}.get(fAsStr))!=None else ''): # This is to fix one error, where the method __radd__ causes issues. reason is because __radd__ is the reverse of __add__ and it gets called when the first object didn't know how to add, example being 1+data, but int doesn't have a __radd__ method so it errors for data(assuming it's an int). the plus first looks at the data's __radd__ and we don't want that so i reverse and force __add__ to be applied to 1, insetad of the other way round.
            if (len(args), kwargs)==(1, {}): # it applies only if one argument is found
                x = getattr(args[0], attr)(tempData) # Calculate the method, define it as x before writing it to file
            else: raise TypeError(f"found inverse for the available method {fAsStr}, but didn't run because too many arguments. {type(tempData)=}") # Erroring before writing to file is very important. updating data in a wrong way is bad, Backups still encouraged.
        else: raise TypeError(f"Method {fAsStr} doesn't exist in {type(tempData)}.\nData::\n{tempData}")
        with open(s.filePath, 'w', encoding='utf-8') as f: # Finally write result to file
            yaml.dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        return x # returned calculated result
    return f

# The "makeData" class is used for creating an object that, whenever you mutate it, 
# it writes it to file automatically. This makes it very easy to use and change data without having to 
# save it every time you change something. everything is done automaticallly :D
#
# The data is first assigned with `data = makeData(filePath, path, defaults)`. the data here is equal to whatever was in the
# yaml data file at the filePath given. 
# 
# This object just imitates the type that it gets from the file. so if the yaml holds a dictionary, then it will 
# act like one. example would be data['playerData'] which is the same behaivior as a normal dictionary, but if you
# check the type of it with `type(data)`, it will give "makeData" which is sometimes what you want, sometimes not.
# If data is a list of strings for example, "".join(data) won't work because "".join() checks if the type is actually
# a string or not, using type(), so it will error. this can be avioided by doing "".join(map(str,data)).
# 
# Indexing the data object never reads the file. it only just returns a new data object with the "path" argument changed.
# path argument is just a list of indexes, so data["hi"]["hello"] is the same as makeData(filePath, ("hi","hello"), defaults)
class makeData:
    def __init__(s, filePath:str, path=(), defaults:list[list[list,dict]]=[]):
        s.filePath = filePath
        s.path = tuple(path)
        s.defaults = defaults

    def __getitem__(s,x):
        return makeData(s.filePath, s.path+tuple(x if type(x) in (tuple, list) else (x,)), s.defaults)

    unlink = write("unlink")

def methodFilter(methods:dict):
    return (i for i in methods if callable(methods[i]))

lottaTypes  = int, float, list, str, set, dict
typeMethods = set().union(*map(methodFilter, map(vars,lottaTypes)))

for i in typeMethods.difference({"__getitem__","__new__","__getattribute__","__init__","__iadd__"}):
    setattr(makeData, i, write(i))


# used to reset the yaml file to a working state if it's empty or non-existant or just isn't working.
def resetYaml(yamlFilePath):
    with open(yamlFilePath, 'w', encoding='utf-8') as f:
        yaml.dump({}, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
# uncomment if you wanna reset data.yaml:
# resetYaml("../data/data.yaml")