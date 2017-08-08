from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as msgbox
from jsonHNDLR import jsonHNDLR
from jsonNAV import jsonNAV, NoJSONFile
from actNAV import * 
from ActORCHARD import actORCHARD, actTREE
from Extract_Transform_Model import extract_transform_model





class Window(Frame):

   
    def __init__(self, master=None):
        
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master 
        self.scanned = False 
        self.file_checkboxes = {}
        self.parent_file_clicked = []
        self.type_checkboxes = []
        self.UndoStream = [] #placeholder until I get here

        self.model = extract_transform_model()
        
       
        self.init_window()

    def init_window(self):
        '''Creates the initial program view'''
        self.master.title("Energy3D JSON Extractor")
        self.create_topmenu()
        self.create_file_sidebar()
        self.create_center_window()
        self.create_bottom_window()
        self.create_type_sidebar()
        

     

    def create_topmenu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)
        file.add_command(label="File Open", command=self.openFile) #right now this doesn't do anything basically, it just opens something but isn't connected to anything else 
        file.add_command(label="Open Dir...", accelerator = 'Ctrl + D', command=self.openDir)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        # create the edit menu
        edit = Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)

        # create the transform menu
        importjson = Menu(menu)
        importjson.add_command(label="Scan...", command=self.run_scan_for_types)
        importjson.add_command(label="Extract", command=self.run_extract_types)
        menu.add_cascade(label="Import JSON", menu=importjson)  

        exportdata = Menu(menu)
        exportoptions = Menu(menu)
        exportoptions.add_command(label="Action Count", command=self.run_export_data)
        exportoptions.add_command(label='Action Density', command=self.run_export_action_desnity)
        menu.add_cascade(label="Export Data", menu=exportdata)
        exportdata.add_cascade(label="Export", menu=exportoptions)

        
        #exportoptions.add_command()

        filtermenu = Menu(menu)
        filtermenu.add_command(label="Reset Filters", command=self.run_reset_filters) #need to fill this out
        menu.add_cascade(label="Filter Options", menu=filtermenu)

        helpmenu = Menu(menu)
        helpmenu.add_command(label="Help")

    def create_file_sidebar(self):
        self.file_sidebar_canvas = Canvas(self.master, height=600, width = 150, bg ='slate gray', highlightthickness = 0)
        self.file_sidebar_canvas.grid(row = 0, column = 0, rowspan = 2, sticky = N+S+W+E)
        self.file_sidebar = Frame(self.file_sidebar_canvas, height=600, width = 130, highlightthickness = 0)
        self.file_sidebar_canvas.create_window((0,0), window=self.file_sidebar, anchor="nw", tags="self.file_sidebar")
        #self.file_sidebar.pack(side=LEFT)
        

    def create_center_window(self):
        self.mWin = Canvas(self.master, bg = "white" , borderwidth = 3, relief = RIDGE)
        self.mWin.create_line(5,20,50,20, width = 3)
        self.mWin.create_line(50,20,50,70, width = 3)
        self.mWin.create_line(5,20,5,70, width = 3)
        self.mWin.create_line(5,70,50,70, width = 3)
        self.mWin.grid(row = 0, column = 1, sticky = N+S+W+E, padx =50)

    def create_bottom_window(self):
        self.infoBox = statusCanvas(self.master, bg= "white", borderwidth = 2, relief = SUNKEN)
        self.infoBox.grid(row=1, column = 1, sticky = N+S+W+E)
        self.infoBoxHeader = Label(self.infoBox, text="No Operations Summary to Display", anchor = W, bg="gray90", borderwidth = 1, relief = RIDGE)
        self.infoBoxHeader.pack(side=TOP, fill=X)
        #self.infoBox.columnconfigure(0, weight = 1, minsize = 50)

    def create_type_sidebar(self):
        self.type_sidebar_canvas = Canvas(self.master, height=600, width = 150, bg ='slate gray', highlightthickness = 0)
        self.type_sidebar_canvas.grid(row = 0, column = 2, rowspan = 2, sticky = N+S+W+E)
        self.type_sidebar = Frame(self.type_sidebar_canvas, height=600, width = 130, highlightthickness = 0)
        self.type_sidebar_canvas.create_window((0,0), window=self.type_sidebar, anchor="nw", tags="self.type_sidebar")


    
    def openFile(self):
        openedfile =  filedialog.askopenfilename(initialdir = "/",title = "Select JSON File",filetypes = (("json files","*.json"),("all files","*.*")))

    def openDir(self):
        '''NEED To error handle if user cancels Open Dir...'''
        self.model.json_handler = jsonHNDLR(filedialog.askdirectory(initialdir = "/", title = "Select Directory"))
        self.model.json_handler.extractJSONFile()
        self.model.user_filelist = self.model.json_handler.jsonlist
        self.drawLsidebar(self.model.user_filelist)
        #print("height:", self.Lside_canvas.winfo_reqheight())
        #print("width:", self.Lside_canvas.winfo_reqwidth())
      

    def run_scan_for_types(self):
        try:
            self.model.scan_for_types()
            self.drawRsidebar(self.model.types_available)   
            self.infoBox.insertStatus("{} types of actions in the logs".format(len(self.model.types_available)))
        except:
            msgbox.showwarning("No JSON loaded", "WARNING! No JSON files loaded!")

    def run_extract_types(self):
        try:
            self.model.extract_types()

        except:
            msgbox.showwarning("Not Scanned for Types", "WARNING! JSON files have not been scanned for types!")
        

    def run_export_data(self):
        '''
        ###NEEDS EXCEPTION HANDLING###
        '''

        self.model.export_data(filedialog.asksaveasfilename(initialdir = "/",title = "Select file", filetypes = (("csv files","*.csv"),("all files","*.*"))))

    def run_export_action_desnity(self):
        '''
        temporary method to get this up and running
        Should be some way to handle all these calls
        without separate methods
        '''
        self.model.export_action_density(filedialog.asksaveasfilename(initialdir = "/",title = "Select file", filetypes = (("csv files","*.csv"),("all files","*.*"))))

    def generate_info_box(self, header="", body=""):
        msgbox.showinfo(header, body)

    def drawLsidebar(self, print_list = []):
        '''
        should there be an error handler in case this gets called before the creation of Lsidebar?
        '''
     
        self.file_sidebar_canvas.delete("all")
        self.create_file_sidebar()
        self.vbar_left=Scrollbar(self.master, orient=VERTICAL)
        self.vbar_left.config(command = self.file_sidebar_canvas.yview)
        self.vbar_left.grid(row = 0, column = 0, rowspan = 2, sticky = N+S+E)

        folderlist = []
        current_key = ''
        for entry in print_list:
            if type(entry[0]) != str or type(entry[1]) != str:
                entry[0], entry[1] = str(entry[0]), str(entry[1])

            if entry[1] != 'Empty' and entry[1] not in folderlist:
                current_key = sidebar_checkbox(self.file_sidebar, entry[1]) 
                current_key.box.bind("<Button-1>", self.change_filechild_state)
                self.file_checkboxes[current_key] = []
                folderlist.append(entry[1])
                print(current_key.state.get())

                
            if entry[0].find('.json'):
                self.file_checkboxes[current_key].append(sidebar_checkbox(self.file_sidebar, entry[0], 10))
        # for key, val in self.file_checkboxes.items():
        #     print(key, val, '\n')

        Button(self.file_sidebar, text="Update", command = self.run_file_student_filter).pack(side=LEFT, padx = 30)

        self.file_sidebar_canvas.config(yscrollcommand = self.vbar_left.set)
        self.file_sidebar.bind("<Configure>", self.onFrameConfigure_file_sidebar)

        self.infoBox.insertStatus("{} students and {} JSON files".format(len(folderlist), len(print_list)))

            #, scrollregion=(0,0,0,15 *len(print_list)))
        #self.file_sidebar.grid(row = 0, column = 0, rowspan = 2, sticky = N+S+W+E)
        #self.file_sidebar.pack(side=LEFT) #not necessary???

    def drawRsidebar(self, print_list=[]):
        self.type_sidebar_canvas.delete("all")
        self.create_type_sidebar()
        self.vbar_right=Scrollbar(self.master, orient=VERTICAL)
        self.vbar_right.config(command = self.type_sidebar_canvas.yview)
        self.vbar_right.grid(row = 0, column = 2, rowspan = 2, sticky = N+S+E)

        for entry in print_list:
            self.type_checkboxes.append(sidebar_checkbox(self.type_sidebar, entry))
        Button(self.type_sidebar, text="Update", command = self.run_type_filter).pack(side=LEFT, padx = 30) #this should have a command that calls some method that deals with the 
        self.type_sidebar_canvas.config(yscrollcommand = self.vbar_right.set)
        self.type_sidebar.bind("<Configure>", self.onFrameConfigure_type_sidebar)

        

    def onFrameConfigure_file_sidebar(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        #print("I am here!")
        self.file_sidebar_canvas.configure(scrollregion=self.file_sidebar_canvas.bbox("self.file_sidebar"))

    def onFrameConfigure_type_sidebar(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        #print("I am here!")
        self.type_sidebar_canvas.configure(scrollregion=self.type_sidebar_canvas.bbox("self.type_sidebar"))

    def change_filechild_state(self, event):
        '''
        Clicked gets the text of parent checkbox clicked. Then it loops 
        through all the file checkboxes. If there is a match between the 
        text retrieved its added to track_parent_file because the on/off
        status of the parent checkbox seems to be thrown off by this method
        then it goes through the list of child check boxes under the
        clicked parents and flips them all to on or off depending on the
        change to the parent
        '''

        clicked = event.widget.cget("text")
    
        for key, val in self.file_checkboxes.items():
            if key.state.get() == clicked or key.state.get() == "-" + clicked:
                self.track_parent_file_clicked(key)
                for box in val:
                    if key.state.get()[0] == "-":
                        if box.state.get()[0] == "-":
                            box.state.set(box.state.get()[1:]) 
                    else:
                        if box.state.get()[0] != "-":
                            box.state.set("-" + box.state.get())
             
        #print(self.parent_file_clicked)
                
    def track_parent_file_clicked(self, checkbox):
        if checkbox.state.get() not in self.parent_file_clicked and checkbox.state.get()[0] != "-":
            self.parent_file_clicked.append(checkbox.state.get())
    # def file_state_swap(self, filebox):
    #     if filebox.state.get()[0]== "-":
    #         filebox.state.set(filebox.state.get()[1:])
    #     else:
    #         filebox.state.set("-" + filebox.state.get())
    #         #print(filebox.state.get())

    def run_file_student_filter(self):
        self.model.filter_ref._student_file_filter = self.process_file_checkbox_state()
        self.model.filtered_model.instance_scheduler()
        #this assumes data has been extracted#####################TEST CODE FOR FILE FILTER####
        # self.model.filtered_model._student_records = self.model.filter_ref.filter_student_files()
        
        
        
     
      

    def run_type_filter(self):
        self.model.filter_ref._type_filter = self.process_list_checkbox_state(self.type_checkboxes) 

        #self.model.filtered_model._student_records = self.model.filter_ref.filter_student_file_types()
        self.model.filtered_model.instance_scheduler()
        
    def run_reset_filters(self):
        '''
        will need to set something here so it checks
        through the R, L filter and resets them iff
        needed
        '''
        self.model.filter_ref.filters_reset()
        self.generate_info_box("Status Update", "Filters have been reset!")
    



    def client_exit(self):
        exit()

    def create_extract_dialogue(self):
        self.extract_dialogue = Toplevel(self.master)
        self.extract_dialogue.title("Extraction Options")
        #Label(extract_dialogue, text="Extraction Options").pack()
        Label(self.extract_dialogue, text="Enter Record Types").pack(anchor=W, padx=10)
        self.user_extract_selections = Text(self.extract_dialogue, height=5, width=15)
        self.user_extract_selections.pack(anchor=W, fill=X, padx=10)
        checkvar = IntVar().set(1)
        Checkbutton(self.extract_dialogue, text='Display Extracted Types', variable=checkvar).pack(anchor=W)
        Button(self.extract_dialogue, text="OK", width = 5, command=self.ok).pack(side=LEFT, pady=5, padx=5)
        Button(self.extract_dialogue, text="Cancel", command=self.cancel).pack(side=LEFT, pady=5, padx=5)
        self.extract_dialogue.transient(self.master)
        print(self.extract_dialogue.winfo_reqwidth())

    def process_file_checkbox_state(self):
        #this will need to process a dictionary and return something that can be stored in the filter
        #self.parent_file_clicked 
        tofilter = {}
        for key, val in self.file_checkboxes.items():
            unchecked_files = self.process_list_checkbox_state(val)
            if unchecked_files:
                if key.state.get()[0] == "-":
                    tofilter[key.state.get()[1:]] = unchecked_files
                else:
                    tofilter[key.state.get()] = unchecked_files

        return tofilter
    


    def process_list_checkbox_state(self, checkboxlist):
        '''
        Note that this does filter away the "-" and lack thereof used
        on the checkboxes themselves, simplify things for the filter
        this distinction is not necessary
        '''
        tofilter = []
        for box in checkboxlist:
            if box.state.get()[0] == "-":
                tofilter.append(box.state.get()[1:])
        return tofilter



    def ok(self):
        print(self.user_extract_selections.get(1.0, END))
        self.extract_dialogue.destroy()
    def cancel(self):
        print("I am dead")
        self.extract_dialogue.destroy()


class sidebar_checkbox:
    def __init__(self, master, check_text, indent = 0):
        self.state = StringVar()
        self.box = Checkbutton(master, text=check_text, variable=self.state, onvalue=check_text, offvalue="-" + check_text, state=ACTIVE)
        self.state.set(check_text)
        self.box.pack(anchor=W, padx = indent)
        self.main_window = main    

class statusCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.defaultx = 5 
        self.defaulty = 25 

    def updateCoordinates(self, x = 0, y = 0):
        self.defaultx = self.defaultx + x
        self.defaulty = self.defaulty + y

    def insertStatus(self, statusmsg):
        if statusmsg == '':
            return
        else:
            print("I am trying to do something")
            self.create_text(self.defaultx, self.defaulty, text=statusmsg, fill = "blue", anchor=NW)
            self.updateCoordinates(0, 15)







class ResizingCanvas(Canvas):
    def __init__(self,parent, **kwargs):
        #print(kwargs)
        Canvas.__init__(self,parent, **kwargs)
        
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        print("height:", self.winfo_reqheight())
        print("width:", self.winfo_reqwidth())


    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        # curframe = inspect.currentframe()
        # calframe = inspect.getouterframes(curframe, 2)
        # print('caller name:', calframe[1][3])
        # argv = inspect.getargvalues(curframe)
        # print(argv)
        print(event.height - self.height)
        print(event.width - self.width)
     
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        #self.Lside_canvas.scale("all",0,0,wscale,hscale)

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
def main():
    root = Tk()

    root.resizable(0,0)

    root.columnconfigure(0, weight=1, minsize = 150)
    root.columnconfigure(1, weight=7, minsize = 500)
    root.columnconfigure(2, weight=1, minsize =150)
    root.rowconfigure(0, weight=1, minsize = 400)
    root.rowconfigure(1, weight=1, minsize = 200)
    #creation of an instance
    #pdb.set_trace()
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

# def Lsidebar_textshift(self, value, incr = 15):
#     value = value + incr
#     return value  

#def add_sidebar_box(self, check_text, storage, home, indent = 0):
    #     storage.append(sidebar_checkbox(home, check_text, indent))
#def process_checkbox_parents(self):
    #     parent_file_clicked_temp = self.parent_file_clicked
    #     for key, val in parent_file_clicked_temp.items():
    #         pass
    # def mirror_parent_file_clicked(self):
    #     parent_

    #need to write out the method called below
        #self.model.filter_ref.file_filter = file_student_list
        #for entry in self.model.filter_ref.file_filter:
            #print(entry)