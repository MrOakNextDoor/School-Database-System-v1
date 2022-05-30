#   Handles how the app looks

#   Libraries
import tkinter as tk
from typing import Dict, Tuple

#   Code
class Page(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self._visible = False

    @property
    def visible(self) -> bool:
        return self._visible
    
    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value
        if value:
            self.pack(expand=True, fill='both')
        else:
            self.pack_forget()

class PageManager:
    def __init__(self) -> None:
        
        self._current_page: str = None
        self.pages: Dict[str, Page] = {}
        self.previous_page: str = None

    @property
    def current_page(self) -> str:
        return self._current_page

    @current_page.setter
    def current_page(self, value: str) -> None:
        try:
            self.pages[self._current_page].visible = False
        except Exception:
            pass

        try:
            self.pages[value].visible = True
        except KeyError:
            raise KeyError(f'Page \"{value}\" not found.')
        else:
            self.previous_page = self._current_page
            self._current_page = value

    def back(self) -> None:
        """Load the previous page.
        """

        self.current_page = self.previous_page

    def add_page(self, name: str, page: Page, overwrite: bool=True) -> None:
        """Add a page to the page manager.

        Args:
            name (str): The name of the page.
            page (Page): The page to be added.
            overwrite (bool): Overwrite page with same name if True. 
            Defaults to True.
        """

        if overwrite:
            self.pages[name] = page
        else:
            if name in self.pages:
                raise ValueError(
                    f'Page with name \"{page}\" already exists. Consider setting overwrite to True to overwrite page with same name.')
            else:
                self.pages[name] = page

    def del_page(self, name: str) -> None:
        """Remove a page from the page manager.

        Args:
            name (str): The name of the page to be removed.
        """
        try:
            self.pages.pop(name)
        except KeyError:
            raise KeyError(f'Page \"{name}\" not found.')

#   From Erik Bethke from:
#   https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
#   Though I have added some modifications
#   TODO: 
#   - Add fade in and out
#   - Make tooltip vanish when mouse moves
class Tooltip:
    def __init__(self, widget, *, bd=1, bg='#FFFFEA', pad=(5, 3, 5, 3), 
        text='This is a tooltip', font=('Bahnschrift Light', 10), waittime=300, 
        wraplength=250):

        self.widget = widget
        self.text = text
        self.bd = bd
        self.bg = bg
        self.font = font
        self.waittime = waittime
        self.wraplength = wraplength

        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onLeave)

        self._pad = pad
        self._id = None
        self._tw = None

    def onEnter(self, *args) -> None:
        self.schedule()

    def onLeave(self, *args) -> None:
        self.unschedule()
        self.hide()

    def schedule(self) -> None:
        self.unschedule()
        self._id = self.widget.after(self.waittime, self.show)

    def unschedule(self) -> None:
        id_ = self._id
        self._id = None
        if id_:
            self.widget.after_cancel(id_)

    def show(self) -> None:

        pad = self._pad
        widget = self.widget
        self._tw = tk.Toplevel(widget)
        self._tw.overrideredirect(True)

        win = tk.Frame(self._tw, bg=self.bg, bd=self.bd, relief=tk.SOLID)
        label = tk.Label(win, text=self.text, justify=tk.LEFT, 
            bg=self.bg, wraplength=self.wraplength, font=self.font)

        label.grid(padx=(pad[0], pad[2]), pady=(pad[1], pad[3]), sticky=tk.NSEW)
        win.grid()

        x, y = self.tip_pos_calc(widget, label)

        self._tw.geometry(f"+{x}+{y}")

    def hide(self) -> None:
        tw = self._tw
        if tw:
            tw.destroy()
        self._tw = None

    def tip_pos_calc(self, widget, label, tip_delta=(10, 5), pad=(5, 3, 5, 3)
        ) -> Tuple[int, int]:

        w = widget

        s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

        width, height = (pad[0] + label.winfo_reqwidth() + pad[2], 
            pad[1] + label.winfo_reqheight() + pad[3])

        mouse_x, mouse_y = w.winfo_pointerxy()

        x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
        x2, y2 = x1 + width, y1 + height

        x_delta = x2 - s_width
        if x_delta < 0:
            x_delta = 0
        y_delta = y2 - s_height
        if y_delta < 0:
            y_delta = 0

        offscreen = (x_delta, y_delta) != (0, 0)

        if offscreen:

            if x_delta:
                x1 = mouse_x - tip_delta[0] - width

            if y_delta:
                y1 = mouse_y - tip_delta[1] - height

        offscreen_again = y1 < 0  # out on the top

        if offscreen_again:
            # No further checks will be done.

            # TIP:
            # A further mod might automagically augment the
            # wraplength when the tooltip is too high to be
            # kept inside the screen.
            y1 = 0

        return x1, y1
