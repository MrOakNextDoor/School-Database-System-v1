
#   Libraries
import sys
import tkinter as tk

import constants
import data
import gui
import misc

#   Code 
class App(tk.Tk):
	def __init__(self) -> None:

		super().__init__()

		self.sectionloader = data.SectionLoader(constants.PATHS.SECTIONS.value)
		self.studentloader = data.StudentLoader(constants.PATHS.STUDENTS.value)
		self.teacherloader = data.TeacherLoader(constants.PATHS.TEACHERS.value)

		self.pagemng = gui.PageManager()
		self.homepage = gui.HomePage(self)
		self.newpage = gui.NewPage(self)
		self.openpage = gui.OpenPage(self)

		self.pagemng.add_page('homepage', self.homepage)
		self.pagemng.add_page('newpage', self.newpage)
		self.pagemng.add_page('openpage', self.openpage)

		w = round((self.winfo_screenwidth()/5)*4)
		h = round((self.winfo_screenheight()/5)*4)
		x = round((self.winfo_screenwidth()/2)-(w/2))
		y = round((self.winfo_screenheight()/2)-(h/2))
		self.geometry(f'{w}x{h}+{x}+{y}')
		self.pagemng.current_page = 'homepage'
		self.reload_window()

		self.protocol('WM_DELETE_WINDOW', self.exit)
		self.mainloop()

	def reload_window(self, event=None) -> None:

		self.sectionloader.load()
		self.studentloader.load()
		self.teacherloader.load()

		self.title(constants.TITLE)

		self.pagemng.pages[self.pagemng.current_page].reload_page()

	def exit(self) -> None:

		self.destroy()

if __name__ == '__main__':
	a = App()
	sys.exit(0)
