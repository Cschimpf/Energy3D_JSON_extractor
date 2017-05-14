from tkinter import filedialog
import csv
from tkinter import tix

from tkinter import *
 


root = tix.Tk()
#need to control for condition where person cancels file upload
def openreadCSV():
	openedfile =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
	
	with open(openedfile, newline = '\n') as csvfile:
		readobj = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for line in readobj:
			print(line)
 
def openDir():
	dirc = filedialog.askdirectory(initialdir = "/", title = "Select Directory")
	print(dirc)
	dt = tix.DirList(root, value = dirc)
	dt.pack()
	
	#print(directory)

def saveFILE():
	print("Not implemented")

menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)

menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open File", command=openreadCSV)
subMenu.add_command(label="Open Directory", command=openDir)
subMenu.add_command(label="Save",command=saveFILE)

display = Text(root, height = 10, width = 30)
display.pack()
display.insert(END, "First line" + "\n")
display.insert(END, "Second line")


root.mainloop()

#print (type(root.filename))