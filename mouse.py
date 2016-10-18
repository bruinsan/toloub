import Tkinter
import time

root = Tkinter.Tk()

while True:
    x = root.winfo_pointerx()
    y = root.winfo_pointery()

    print "x = {}   y = {}".format(x, y)
   
    time.sleep(0.5)
