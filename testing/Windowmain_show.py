from tkinter import *
from tkinter import filedialog
from jsonHNDLR import jsonHNDLR
import inspect, pdb 
#what if we create a root and then create either one giant frame or a frame for each of the canvases and set their size in the canvas initialization and then within their frames, pack
#them and have them expand/fill as a system within the frames even though the frames are placed on a grid?

class GUIStorage(object):
    def __init__(self):
        '''should the attributes on this class all be decorators since they will be set, reset
        and changed as irregular times?
        '''
    @property
    def path_and_locs(self):
        return self._path_and_locs 
    @path_and_locs.setter 
    def path_and_locs(self, plocs_list):
        '''
        should you add any checks or error states here?
        '''
        self._path_and_locs = plocs_list


class Window(Frame):

    def __init__(self, master=None):
        
        #Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    def init_window(self):
   
        self.Lsidebar = Frame(self.master, bg="white", borderwidth = 3, relief = GROOVE)
        self.Lsidebar.grid(row = 0, column = 0, rowspan = 2)
        self.Lside_canvas = ResizingCanvas(self.Lsidebar, width = 120, height = 600, bg="red", highlightthickness = 0)
        self.Lside_canvas.grid(row = 0, column = 0, sticky=N+S+W+E)

class ResizingCanvas(Canvas):
    def __init__(self,parent, **kwargs):
        print(kwargs)
        Canvas.__init__(self,parent, **kwargs)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.bind("<Configure>", self.on_resize)
        print("new width", self.width, "new height:", self.height)

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)
        print(self.width, self.height)

def main():
    root = Tk()

    root.columnconfigure(0, weight=1, minsize = 120)
    root.columnconfigure(1, weight=7, minsize = 500)
    root.rowconfigure(0, weight=1, minsize = 400)
    root.rowconfigure(1, weight=1, minsize = 200)
    app = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()  

#*****************************DISCARDED CODE******************************************

#UNNECESSARY/REDUNDANT??
    #location for subwindows?
    #self.uploadedWin = None #this might be a candidate for a decorator as it will be updated regularly, but for now just a placeholder
    #self.mainWin = None 

#height = 400, width = 500, <-for main
#height = 600, width = 100, <-for sidebar

#self.uploadedWin.columnconfigure(0, weight=1)
#self.uploadedWin.rowconfigure(0, weight=1)

#self.mWin.columnconfigure(1, weight=1)
        #self.mWin.rowconfigure(0, weight=1)