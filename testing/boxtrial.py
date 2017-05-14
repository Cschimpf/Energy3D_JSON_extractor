from tkinter import *


class listoboxes:
	def __init__(self):
		self.boxes = []

	def addBox(self, master, check_text):
		self.boxes.append(self.sidebar_checkbox(master, check_text, self))

	def updateBox(self, newstate):
		pass


	class sidebar_checkbox:
		def __init__(self, master, check_text, main):
			self.state = StringVar()
			self.box = Checkbutton(master, text=check_text, variable=self.state, onvalue=check_text, offvalue="-" + check_text, state=ACTIVE)
			#command=self.printContents)
			self.box.bind("<Button-1>", self.printSender)
			self.state.set("-" + check_text)
			self.box.pack(anchor=W)
			self.main_window = main


		def printContents(self):
			for items in self.main_window.boxes:
				print(items.state.get())

			print('\n')
		
		def printSender(self, event):
			clicked = event.widget.cget("text")
			for checkbox in self.main_window.boxes:
				if clicked == checkbox.state.get() or "-" + clicked == checkbox.state.get():
					print(checkbox.state.get())
					print(checkbox.state.get("text"))

	


def main():
	checkboxlist = ['Add SolarPanel', 'Edit SolarPanel', 'Change SolarPanel', 'Paste SolarPanel', 'Show Heliodon', 'Add Wall', 'Add Window']
	root = Tk()
	listboxes = listoboxes()
	for item in checkboxlist:
		listboxes.addBox(root, item)



    	


	root.mainloop()

if __name__ == "__main__":
	main()  