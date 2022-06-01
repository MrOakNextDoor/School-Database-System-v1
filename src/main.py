
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

		if self.settings.restore_last:
			self.restore_last()
		else:
			self.reload_window()
			w = round((self.winfo_screenwidth()/5)*4)
			h = round((self.winfo_screenheight()/5)*4)
			x = round((self.winfo_screenwidth()/2)-(w/2))
			y = round((self.winfo_screenheight()/2)-(h/2))
			self.geometry(f'{w}x{h}+{x}+{y}')

		self.protocol('WM_DELETE_WINDOW', self.exit)
		self.mainloop()

	def restore_last(self) -> None:
		self.appstate.load()

	def reload_window(self) -> None:
		self.settings.load()

		self.title(self.settings.title)

	def exit(self) -> None:

		self.appstate.dump()

		self.destroy()

if __name__ == '__main__':
	a = App()
	sys.exit(0)
