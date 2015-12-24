__author__ = 'Sven'

import pygcurse

lista={}
lista['search']=True
lista['avoid']=False
lista['bomb']=True
lista['landing']=False

win = pygcurse.PygcurseWindow(40, 25)



while True:
    win.cursor = (5, 5)
    win.fgcolor='white'
    win.pygprint('Current Status \n')

    for idx, val in enumerate(lista):
        #print(str(idx)+str(val)+str(lista[val]))
        win.fgcolor='white'
        win.write(str(idx)+" "+str(val)+" is: ")
        if lista[val]:
            win.fgcolor = 'green'
            win.write("Enabled \n")
        else:
            win.fgcolor = 'red'
            win.write("Disabled \n")

    win.fgcolor='white'
    choice = win.input()
    change=False

    for idx, val in enumerate(lista):
        if str(choice)==str(idx):
            change=True
            toChange=val

    if change:
        if lista[toChange]:
            win.write("\n\n Disable of "+str(toChange)+" (yes/no):")
        else:
            win.write("\n\n Enable of "+str(toChange)+" (yes/no):")

        choice = win.input()

        if choice=="yes":
            lista[toChange]= not lista[toChange]

    win.cursor = (1, 1)
    win.erase()

pygcurse.waitforkeypress()







