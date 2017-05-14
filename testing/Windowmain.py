from tkinter import *
from tkinter import filedialog
from jsonHNDLR import jsonHNDLR
import inspect, pdb 


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
        
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master
        self.dirc = None 
        self.UndoStream = []
        self.gui_store = GUIStorage()
       
        self.init_window()

    #Creation of init_window
    def init_window(self):
   
        self.master.title("Energy3D JSON Extractor")

        # allowing the widget to take the full space of the root window, not sure what this refers to? was part of copied code
        #self.pack()

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        file.add_command(label="File Open", command=self.openFile)
        file.add_command(label="Open Directory", command=self.openDir)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu)

        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)

        #resizing of canvas not working, need to look it up cuz right now you specify a size and that seems to conflict with resizing events 
        self.Lsidebar = Frame(self.master, bg="white", borderwidth = 3, relief = GROOVE)
        self.Lsidebar.grid(row = 0, column = 0, rowspan = 2, sticky = N+S+W+E)
        self.Lside_canvas = Canvas(self.Lsidebar, width = 120, height = 600)
        self.Lcanvas_height = self.Lside_canvas.winfo_reqheight()
        self.Lcanvas_width = self.Lside_canvas.winfo_reqwidth()
        self.Lside_canvas.grid(row = 0, column = 0, rowspan = 2)
        self.Lside_canvas.bind("<Configure>", self.on_resize)
      
        #self.Lsidebar.columnconfigure(0, weight = 1, minsize =105)
        #self.Lsidebar.columnconfigure(1, weight = 1, minsize =15)
       


        #self.sideScroll = Scrollbar(self.Lsidebar)
        #self.sideScroll.grid(row = 0, column = 0, sticky = N+S)
        #self.Lsidebar.rowconfigure(0, weight = 1, minsize = 600)
        

        self.mWin = Frame(self.master, bg = "white" , borderwidth = 3, relief = RIDGE)
        self.mWin.grid(row = 0, column = 1, sticky = N+S+W+E, padx =50)

        self.infoBox = Frame(self.master, bg= "white", borderwidth = 3, relief = GROOVE)
        self.infoBox.grid(row=1, column = 1, sticky = N+S+W+E, pady = 10)
        self.infoBoxHeader = Label(self.infoBox, text="No Operations Summary to Display", anchor = W, bg="gray90", borderwidth = 2, relief = RIDGE)
        self.infoBoxHeader.grid(row =0, column = 0, sticky = N+S+W+E)
        self.infoBox.columnconfigure(0, weight = 1, minsize = 50)

       
      
    
    def openFile(self):
        openedfile =  filedialog.askopenfilename(initialdir = "/",title = "Select JSON File",filetypes = (("json files","*.json"),("all files","*.*")))
    def openDir(self):
        self.dirc = filedialog.askdirectory(initialdir = "/", title = "Select Directory")
        jHNDLR = jsonHNDLR(self.dirc)
        jHNDLR.extractJSONFile()
        self.drawLsidebar(jHNDLR.jsonlist)
        self.gui_store.path_and_locs = jHNDLR.jsonlist
        for items in jHNDLR.jsonlist:
            print(items)
        print(len(jHNDLR.jsonlist))
    def client_exit(self):
        exit()

    def drawLsidebar(self, print_list = []):
        '''
        should there be an error handler in case this gets called before the creation of Lsidebar?
        '''
        self.Lside_canvas.delete("all")
        self.vbar=Scrollbar(self.master, orient=VERTICAL)
        self.vbar.config(command = self.Lside_canvas.yview)
        self.vbar.grid(row = 0, column = 0, rowspan = 2, sticky = N+S+E)
        self.Lside_canvas.config(yscrollcommand = self.vbar.set, scrollregion=(0,0,0,2500))
        #self.Lside_canvas.grid(row = 0, column = 0)

        defaultx, defaulty = 5, 10
        folderlist = []
        for entry in print_list:
            if type(entry[0]) != str or type(entry[1]) != str:
                entry[0], entry[1] = str(entry[0]), str(entry[1])

            if entry[1] != 'Empty' and entry[1] not in folderlist:
                self.Lside_canvas.create_text(defaultx, defaulty, text=entry[1], anchor = NW)
                defaulty = self.Lsidebar_textshift(defaulty) 
                #defaulty = defaulty + 15
                folderlist.append(entry[1])
            if entry[0].find('.json'):
                self.Lside_canvas.create_text(defaultx + 10, defaulty, text=entry[0], anchor = NW, fill = "lime green")
            defaulty = self.Lsidebar_textshift(defaulty)  
            #defaulty = defaulty + 15
    def Lsidebar_textshift(self, value, incr = 15):
        value = value + incr
        return value  

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print('caller name:', calframe[1][3])
        argv = inspect.getargvalues(curframe)
        print(argv)

        wscale = float(event.width)/self.Lcanvas_width
        hscale = float(event.height)/self.Lcanvas_height
        self.Lcanvas_width = event.width
        self.Lcanvas_height = event.height
        # resize the canvas 
        self.Lside_canvas.config(width=self.Lcanvas_width, height=self.Lcanvas_height)
        # rescale all the objects tagged with the "all" tag
        #self.Lside_canvas.scale("all",0,0,wscale,hscale)
   


class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
def main():
    root = Tk()

#   root.resizable(0,0)

    root.columnconfigure(0, weight=1, minsize = 120)
    root.columnconfigure(1, weight=7, minsize = 500)
    root.rowconfigure(0, weight=1, minsize = 400)
    root.rowconfigure(1, weight=1, minsize = 200)
    #creation of an instance
    app = Window(root)
    pdb.set_trace()

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