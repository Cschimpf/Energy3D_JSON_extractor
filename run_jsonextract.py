from jsonHNDLR import jsonHNDLR
from jsonNAV import jsonNAV, NoJSONFile
from ActORCHARD import actORCHARD, actTREE
from StudentFiles import studentFILES
from TreeProc import treePROC, dataVER, filter, activityFilter
from actNAV import * 
import time 

def Main():
	timestart = time.time()
	jhndlr, sfiles = jsonHNDLR(), studentFILES() 
	a_orch, b_orch = actORCHARD(), actORCHARD()
	jhndlr.extractJSONFile()
	
	for key, val in jhndlr.jsondict.items():
		sfiles.addStudent(val)
		jnav, jnav.jsonfile = jsonNAV(), jhndlr.openJSON(key, val) #for now I am not looping through anything, just checking integration of all the modules  
		if jnav.jsonfile:
			b_orch = jnav.jsonSC4NNR(True)
		else:
			b_orch = None #I believe this is here because sometimes the json file is empty or can't be processed, still need to work w/ Charles on this 
			continue 
		if b_orch:
			sfiles.addRecord(val, key, b_orch) #student_id, fname, actORCHARD object
		#for items in b_orch.actTREES:
			#a_orch.planTREE(items)
			#a_orch.planTYPE(x, key, val)
		#print(val, key, "done!")


	#for k, v in a_orch.actTYPES.items():
		#print(k, '\n', v)
	print(type(b_orch), b_orch)
	print("Done Extracting!", time.time() -timestart)
	# tproc = treePROC()
	# actfil = activityFilter('activities', sfiles)
	# actfil.applyFilter(3, True)
	# tproc.printRECS(actfil.liveVER.mod_records.recordlist)
	print("Done Writing!", time.time() -timestart)
	#return sfiles
	#return a_orch




if __name__ == "__main__":
    Main()