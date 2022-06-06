
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

		self.appstate = data.AppState()
		self.settings = data.Settings()

		self.pagemanager = gui.PageManager()
		self.homepage = gui.HomePage(self)
		self.newpage = gui.NewPage(self)

		self.pagemanager.add_page('homepage', self.homepage)
		self.pagemanager.add_page('newpage', self.newpage)

		if self.settings.restore_last:
			self.restore_last()
		else:
			w = round((self.winfo_screenwidth()/5)*4)
			h = round((self.winfo_screenheight()/5)*4)
			x = round((self.winfo_screenwidth()/2)-(w/2))
			y = round((self.winfo_screenheight()/2)-(h/2))
			self.geometry(f'{w}x{h}+{x}+{y}')
			if self.settings.expand:
				self.state('zoomed')
			self.pagemanager.current_page = 'homepage'
			self.reload_window()

		self.protocol('WM_DELETE_WINDOW', self.exit)
		self.mainloop()

	def reload_window(self, event=None) -> None:
		self.settings.load()

		self.title(self.settings.title)

		self.pagemanager.pages[self.pagemanager.current_page].reload_page()

	def restore_last(self) -> None:

		self.appstate.load()

		self.pagemanager.current_page = self.appstate.current_page
		self.pagemanager.previous_page = self.appstate.previous_page

	def dump(self) -> None:
		
		self.appstate.current_page = self.pagemanager.current_page
		self.appstate.previous_page = self.pagemanager.previous_page

		self.appstate.dump()
		self.settings.dump()

	def exit(self) -> None:

		self.dump()

		self.destroy()

if __name__ == '__main__':
	a = App()
	sys.exit(0)
