
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

        self.pagemanager = gui.PageManager()

        self.settings = data.Settings()
        self.appstate = data.AppState()
        self.reload_loaders()
        self.reload_window()

        if self.settings.restore_last:
            pass
        else:
            self.title(constants.DEFAULT_SETTINGS.TITLE.value)
            w = round((self.winfo_screenwidth()/5)*3)
            h = round((self.winfo_screenheight()/5)*3)
            x = round((self.winfo_screenwidth()/2) - (w/2))
            y = round((self.winfo_screenheight()/2) - (h/2))
            self.geometry(f'{w}x{h}+{x}+{y}')

        self.protocol('WM_DELETE_WINDOW', self.exit)
        self.mainloop()

    def reload_loaders(self, event=None) -> None:
        self.settings.load()
        self.appstate.load()

    def reload_window(self, event=None) -> None:
        self.title(self.settings.title)

    def dump(self, event=None) -> None:

        self.settings.dump()
        self.appstate.dump()

    def exit(self) -> None:
        
        self.dump()

        self.destroy()

if __name__ == '__main__':
    a = App()
    sys.exit(0)
