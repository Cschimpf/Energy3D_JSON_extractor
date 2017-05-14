'''
Created on Dec 29, 2015

@author: Corey Schimpf
'''
import os, json

class jsonHNDLR(object):
    '''
    This class takes a base directory as input and performs operations related to it or 
    on documents extracted from that directory
    '''
    def __init__(self, basedir, sub = False):
        self.basedir = basedir
        self.basedex = 0
        self.jsondict = {} #should this have a setter and getter? ****DEFUNCT*****
        self.jsonlist = []
        self.subdir = [] #this will hold the contents of a subdirectory to be processed
        self.subdirname = ''

    #@property
    #def basedir(self):
        #return self._basedir 
    #@basedir.setter 
    #def basedir(self, dirname):
        '''
        originally I was going to put a check on the dirname here
        but I think it makes more sense to put this somewhere else,
        like a function call that repeats input back in the __init__
        for jsonHNDLR instead of waiting down here until its about to be set
        '''
        #self._basedir = self.procDir(dirname)

    def procDir(self, dirname):
        return dirname.replace("\\", "/")

    def incrBasedex(self):
        self.basedex +=1
        
    def openJSON(self, fname, dirname =''):
        '''
        Creates a dictionary from json file
        For more public release may want have
        some check over whether fname is str or not
        '''
        fname = self.checkSLASH(fname)
        if dirname:
            dirname = self.checkSLASH(dirname)
        try:
            jsonfile = json.load(open(self.basedir + dirname + fname))
            return jsonfile
        except ValueError as e:
            print(e) 
            return None #it would do this anyways but just to be explicit 
        
         

    def removeSUB(self, dirlist):
        dirlist2 = []
        for items in dirlist:
            if items[0] != '.':
                dirlist2.append(items)  
        return dirlist2

    def openDir(self, dirname = '', keepsub = 0):
        '''
        Creates a list of the files in a directory. If dirname is empty will return list of files in basedirectory.
        Otherwise dirname will be appended to the basedirectory
        '''
        if dirname != '':
            dirname = self.checkSLASH(dirname)
            
            
        dirlist = os.listdir(self.basedir + dirname) #removed basedir for GUI interface
        
        if keepsub == 0: #if 0 will disinclude any folder with a '.' if 1 will include
            dirlist = self.removeSUB(dirlist)
        return dirlist 

    def extractJSONFile(self, dirname = ''):
        filelist = self.openDir(dirname)

        for item in filelist:
            
            if self.checkDir(item) and not self.subdirname:
                self.setsubDir(self.checkDir(item), item)
                self.extractJSONFile(item)  
            else:
                if self.checkJSON(item):
                    self.addtoList(item)
                else:
                    continue 
        self.setsubDir()


    def assignName(self):
        if self.subdirname:
            return self.subdirname
        else:
            return 'Empty'
            #self.incrBasedex()
            #return 'Unknown'+ str(self.basedex)
    def addtoList(self, key):
        self.jsonlist.append([key, self.assignName()])
        #self.jsondict[key] = self.assignName()  

    def setsubDir(self, filelist = [], subname = ''):
        self.subdir = filelist
        self.subdirname = subname 


    def checkSLASH(self, name):
        if name[0] !='/':
            return '/' + name
        else:
            return name 
    def checkJSON(self, name):
        
        if name.find(".json") != -1:
            return name  
        else:
            return False 
    def checkDir(self, name = ''):
        try:
            return self.openDir(name)
        except:
            return False 

    #what if in openDir it basically scans the directory given. and makes dictionary entries for any valid JSON file. if the JSON is in the
    #base directory the key can be some identical value, maybe an integer like 1, which can be later strified and also will distinguish it from
    #entries that have a str key, which will refer to the folder name. But what should be the default value for JSON files in the base then?
    '''

    def checkVALUE(self, data, check):
        if data != check:
            return True
        return False 
    '''