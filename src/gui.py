#   Handles how the app looks

#   Libraries
import tkinter as tk
from abc import ABC, abstractmethod
from calendar import monthrange
from datetime import date
from tkinter import ttk
from typing import Any, Dict, Tuple

import data
import misc

#   Code
class Page(ABC, tk.Frame):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)
		self.parent = master
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

	@abstractmethod
	def reload_page(self, event=None) -> None:
		pass
	
class HomePage(Page):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		self.l_frm = tk.Frame(master=self)
		self.inner_l_frm = tk.Frame(master=self.l_frm)
		self.title = tk.Label(master=self.inner_l_frm, 
			text='School Database System')
		self.title.pack(expand=True, fill='x', side='top')

		self.top_search_frm = tk.Frame(master=self.inner_l_frm)
		self.search_bar_lbl = tk.Label(master=self.top_search_frm, text='Search:')
		self.search_bar = tk.Entry(master=self.top_search_frm, relief='groove', bd=2)
		self.search_bar_lbl.pack(side='left')
		self.search_bar.pack(expand=True, fill='x', side='right')
		self.top_search_frm.pack(fill='x', padx=20, pady=(20, 6))

		self.bottom_search_frm = tk.Frame(master=self.inner_l_frm)
		self.list_scrollbar = tk.Scrollbar(master=self.bottom_search_frm)
		self.list = tk.Listbox(master=self.bottom_search_frm, yscrollcommand=self.list_scrollbar.set, 
			relief='groove', bd=2)
		self.list_scrollbar.config(command=self.list.yview)
		for i in range(1, 101):
			self.list.insert(tk.END, f'Keon Clone {i}')
		self.list_scrollbar.pack(fill='y', side='right')
		self.list.pack(expand=True, fill='both', side='left')
		self.bottom_search_frm.pack(expand=True, fill='both', padx=20, pady=(6, 20))

		self.inner_l_frm.pack(expand=True, fill='x', padx=(30, 10))
		self.l_frm.pack(expand=True, fill='both', side='left')

		self.r_frm = tk.Frame(master=self)
		self.inner_r_frm = tk.Frame(master=self.r_frm)
		self.new_btn = tk.Button(master=self.inner_r_frm, text='New', height=3, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.new)
		self.open_btn = tk.Button(master=self.inner_r_frm, text='Open', height=3, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		self.open_recent_btn = tk.Button(master=self.inner_r_frm, text='Open Recent', 
			height=3, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		self.more_btn = tk.Button(master=self.inner_r_frm, text='More Actions', 
			height=3, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		self.exit_btn = tk.Button(master=self.inner_r_frm, text='Exit', height=3, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.parent.exit)
		self.new_btn.pack(expand=True, fill='x', padx=6, pady=(20, 2))
		self.open_btn.pack(expand=True, fill='x', padx=6, pady=2)
		self.open_recent_btn.pack(expand=True, fill='x', padx=6, pady=2)
		self.more_btn.pack(expand=True, fill='x', padx=6, pady=(2, 10))
		self.exit_btn.pack(expand=True, fill='x', padx=6, pady=10)
		self.inner_r_frm.pack(expand=True, fill='x', padx=(10, 30))
		self.r_frm.pack(expand=True, fill='both', side='right')
		
		self.search_bar_tooltip = Tooltip(self.search_bar, text='Search Bar', 
			font=('Bahnschrift Light', 10))
		self.new_btn_tooltip = Tooltip(self.new_btn, text='Create a New Profile', 
			font=('Bahnschrift Light', 10))
		self.open_btn_tooltip = Tooltip(self.open_btn, text='Access a Profile', 
			font=('Bahnschrift Light', 10))
		self.open_recent_btn_tooltip = Tooltip(self.open_recent_btn, text='Open a recently-accessed profile.', 
			font=('Bahnschrift Light', 10))
		self.more_btn_tooltip = Tooltip(self.more_btn, text='More Actions...', 
			font=('Bahnschrift Light', 10))
		self.exit_btn_tooltip = Tooltip(self.exit_btn, text='Exit SDS', 
			font=('Bahnschrift Light', 10))

		self.dynresize = DynamicResize(self)
		self.dynresize.add_child(self.title, 'Bahnschrift', 36, 40, 10)
		self.dynresize.add_child(self.search_bar_lbl, 'Bahnschrift Light', 16, 20, 6)
		self.dynresize.add_child(self.search_bar, 'Bahnschrift Light', 16, 20, 6)
		self.dynresize.add_child(self.list, 'Bahnschrift Light', 16, 20, 6)
		self.dynresize.add_child(self.new_btn, 'Bahnschrift Light', 14, 18, 6)
		self.dynresize.add_child(self.open_btn, 'Bahnschrift Light', 14, 18, 6)
		self.dynresize.add_child(self.open_recent_btn, 'Bahnschrift Light', 14, 18, 6)
		self.dynresize.add_child(self.more_btn, 'Bahnschrift Light', 14, 18, 6)
		self.dynresize.add_child(self.exit_btn, 'Bahnschrift Light', 14, 18, 6)

		self.reload_page()

	def reload_page(self, event=None) -> None:
		
		#	TODO: Work on themes for customizable look
		self.title.config(font=('Bahnschrift', 36))
		self.search_bar_lbl.config(font=('Bahnschrift Light', 16))
		self.search_bar.config(font=('Bahnschrift Light', 16))
		self.list.config(font=('Bahnschrift Light', 16))
		self.new_btn.config(font=('Bahnschrift Light', 14))
		self.open_btn.config(font=('Bahnschrift Light', 14))
		self.open_recent_btn.config(font=('Bahnschrift Light', 14))
		self.more_btn.config(font=('Bahnschrift Light', 14))
		self.exit_btn.config(font=('Bahnschrift Light', 14))

		self.search_bar_tooltip.font = ('Bahnschrift Light', 10)
		self.new_btn_tooltip.font = ('Bahnschrift Light', 10)
		self.open_btn_tooltip.font = ('Bahnschrift Light', 10)
		self.open_recent_btn_tooltip.font = ('Bahnschrift Light', 10)
		self.more_btn_tooltip.font = ('Bahnschrift Light', 10)
		self.exit_btn_tooltip.font = ('Bahnschrift Light', 10)

	def new(self, event=None) -> None:
		self.parent.pagemng.current_page = 'newpage'

class NewPage(Page):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		self.inner_frm = tk.Frame(master=self)
		self.title = tk.Label(master=self.inner_frm, text='Create New')
		self.student_btn = tk.Button(master=self.inner_frm, text='New Student', 
			height=3, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.student)
		self.teacher_btn = tk.Button(master=self.inner_frm, text='New Teacher', 
			height=3, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.teacher)
		self.section_btn = tk.Button(master=self.inner_frm, text='New Section', 
			height=3, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.section)
		self.back_btn = tk.Button(master=self.inner_frm, text='Back', 
			height=3, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.back)
		self.title.pack(expand=True, fill='x', side='top', pady=10)
		self.student_btn.pack(expand=True, fill='x', padx=10, pady=(10, 2))
		self.teacher_btn.pack(expand=True, fill='x', padx=10, pady=2)
		self.section_btn.pack(expand=True, fill='x', padx=10, pady=(2, 10))
		self.back_btn.pack(expand=True, fill='x', padx=10, pady=(10, 0))
		self.inner_frm.pack(expand=True, fill='x', padx=30)

		self.student_btn_tooltip = Tooltip(self.student_btn, 
			text='Create a New Student Profile', font=('Bahnschrift Light', 10))
		self.teacher_btn_tooltip = Tooltip(self.teacher_btn, 
			text='Create a New Teacher Profile', font=('Bahnschrift Light', 10))
		self.section_btn_tooltip = Tooltip(self.section_btn, 
			text='Create a New Section', font=('Bahnschrift Light', 10))
		self.back_btn_tooltip = Tooltip(self.back_btn, 
			text='Go Back to Previous Page', font=('Bahnschrift Light', 10))

		self.dynresize = DynamicResize(self)
		self.dynresize.add_child(self.title, 'Bahnschrift', 36, 40, 10)
		self.dynresize.add_child(self.student_btn, 'Bahnschrift Light', 16, 20, 6)
		self.dynresize.add_child(self.teacher_btn, 'Bahnschrift Light', 16, 20, 6)
		self.dynresize.add_child(self.section_btn, 'Bahnschrift Light', 16, 20, 6)
		self.dynresize.add_child(self.back_btn, 'Bahnschrift Light', 16, 20, 6)

		self.reload_page()

	def reload_page(self) -> None:
		
		self.title.config(font=('Bahnschrift', 36))
		self.student_btn.config(font=('Bahnschrift Light', 16))
		self.teacher_btn.config(font=('Bahnschrift Light', 16))
		self.section_btn.config(font=('Bahnschrift Light', 16))
		self.back_btn.config(font=('Bahnschrift Light', 16))

		self.student_btn_tooltip.font = ('Bahnschrift Light', 10)
		self.student_btn_tooltip.font = ('Bahnschrift Light', 10)
		self.teacher_btn_tooltip.font = ('Bahnschrift Light', 10)
		self.section_btn_tooltip.font = ('Bahnschrift Light', 10)
		self.back_btn_tooltip.font = ('Bahnschrift Light', 10)

	def back(self) -> None:

		self.parent.pagemng.back()

	def student(self) -> None:
		
		self.master.pagemng.pages['tempprofilepage'] = ProfilePage(self.master)
		self.master.pagemng.current_page = 'tempprofilepage'

	def teacher(self) -> None:

		pass

	def section(self) -> None:
		
		pass

class GeneralSection(Page):
	MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 
		'August', 'September', 'October', 'November', 'December')
	GENDERS = ('Male', 'Female')
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		#	Name
		self.name_frm = tk.Frame(master=self)
		self.lname_lbl = tk.Label(master=self.name_frm, text='Last Name')
		self.lname_entry = tk.Entry(master=self.name_frm, relief='groove', bd=2)
		self.fname_lbl = tk.Label(master=self.name_frm, text='First Name')
		self.fname_entry = tk.Entry(master=self.name_frm, relief='groove', bd=2)
		self.mname_lbl = tk.Label(master=self.name_frm, text='Middle Name')
		self.mname_entry = tk.Entry(master=self.name_frm, relief='groove', bd=2)

		self.lname_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.lname_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.fname_lbl.grid(column=3, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.fname_entry.grid(column=4, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.mname_lbl.grid(column=6, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.mname_entry.grid(column=7, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		
		self.name_frm.columnconfigure(1, weight=1)
		self.name_frm.columnconfigure(4, weight=1)
		self.name_frm.columnconfigure(7, weight=1)
		
		self.name_frm.pack(fill='x', padx=10, pady=2)

		#	Address
		self.address_frm = tk.Frame(master=self)
		self.address_lbl = tk.Label(master=self.address_frm, text='Address')
		self.address_entry = tk.Entry(master=self.address_frm, relief='groove', bd=2)

		self.address_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.address_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.address_frm.columnconfigure(1, weight=1)

		self.address_frm.pack(fill='x', padx=10, pady=2)

		#	Birthday
		self.bday_frm = tk.Frame(master=self)
		self.month_lbl = tk.Label(master=self.bday_frm, text='Month of Birth')
		self.month_cbox = ttk.Combobox(master=self.bday_frm, state="readonly", values=self.MONTHS)
		self.day_lbl = tk.Label(master=self.bday_frm, text='Day of Birth')
		self.day_entry = tk.Entry(master=self.bday_frm, relief='groove', bd=2)
		self.year_lbl = tk.Label(master=self.bday_frm, text='Year of Birth')
		self.year_entry = tk.Entry(master=self.bday_frm, relief='groove', bd=2)

		self.month_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.month_cbox.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.day_lbl.grid(column=3, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.day_entry.grid(column=4, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.year_lbl.grid(column=6, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.year_entry.grid(column=7, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		
		self.bday_frm.columnconfigure(1, weight=1)
		self.bday_frm.columnconfigure(4, weight=1)
		self.bday_frm.columnconfigure(7, weight=1)

		self.bday_frm.pack(fill='x', padx=10, pady=2)

		#	Contacts
		self.contacts_frm = tk.Frame(master=self)
		self.email_lbl = tk.Label(master=self.contacts_frm, text='Email Address')
		self.email_entry = tk.Entry(master=self.contacts_frm, relief='groove', bd=2)
		self.contact_lbl = tk.Label(master=self.contacts_frm, text='Contact Number')
		self.contact_entry = tk.Entry(master=self.contacts_frm, relief='groove', bd=2)

		self.email_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.email_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.contact_lbl.grid(column=3, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.contact_entry.grid(column=4, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		
		self.contacts_frm.columnconfigure(1, weight=1)
		self.contacts_frm.columnconfigure(4, weight=1)

		self.contacts_frm.pack(fill='x', padx=10, pady=2)

		#	Gender
		self.gender_frm = tk.Frame(master=self)
		self.gender_lbl = tk.Label(master=self.gender_frm, text='Gender / Sex')
		self.gender_cbox = ttk.Combobox(master=self.gender_frm, state="readonly", values=self.MONTHS)

		self.gender_cbox['values'] = self.GENDERS

		self.gender_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.gender_cbox.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		
		self.gender_frm.columnconfigure(1, weight=1)

		self.gender_frm.pack(fill='x', padx=10, pady=2)

		self.dynresize = DynamicResize(self.master.master)
		self.dynresize.add_child(self.lname_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.lname_entry, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.fname_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.fname_entry, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.mname_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.mname_entry, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.address_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.address_entry, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.month_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.month_cbox, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.day_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.day_entry, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.year_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.year_entry, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.contact_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.contact_entry, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.email_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.email_entry, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.gender_lbl, 'Bahnschrift Light', 12, 14, 4)
		self.dynresize.add_child(self.gender_cbox, 'Bahnschrift Light', 12, 14, 4)

		self.lname_entry_tooltip = Tooltip(self.lname_entry, text='Last Name')
		self.fname_entry_tooltip = Tooltip(self.fname_entry, text='First Name')
		self.mname_entry_tooltip = Tooltip(self.mname_entry, text='Full Middle Name')
		self.address_entry_tooltip = Tooltip(self.address_entry, text='Address')
		self.month_cbox_tooltip = Tooltip(self.month_cbox, text='Month of Birth')
		self.day_entry_tooltip = Tooltip(self.day_entry, text='Day of Birth')
		self.year_entry_tooltip = Tooltip(self.year_entry, text='Year of Birth')
		self.contact_entry_tooltip = Tooltip(self.contact_entry, text='Contact Number')
		self.email_entry_tooltip = Tooltip(self.email_entry, text='Email Address, Optional')
		self.gender_entry_tooltip = Tooltip(self.gender_cbox, text='Gender')

		self.reload_page()

	def reload_page(self, event=None) -> None:
		
		self.lname_lbl.config(font=('Bahnschrift Light', 12))
		self.lname_entry.config(font=('Bahnschrift Light', 12))
		self.fname_lbl.config(font=('Bahnschrift Light', 12))
		self.fname_entry.config(font=('Bahnschrift Light', 12))
		self.mname_lbl.config(font=('Bahnschrift Light', 12))
		self.mname_entry.config(font=('Bahnschrift Light', 12))

		self.address_lbl.config(font=('Bahnschrift Light', 12))
		self.address_entry.config(font=('Bahnschrift Light', 12))

		self.month_lbl.config(font=('Bahnschrift Light', 12))
		self.month_cbox.config(font=('Bahnschrift Light', 12))
		self.day_lbl.config(font=('Bahnschrift Light', 12))
		self.day_entry.config(font=('Bahnschrift Light', 12))
		self.year_lbl.config(font=('Bahnschrift Light', 12))
		self.year_entry.config(font=('Bahnschrift Light', 12))

		self.contact_lbl.config(font=('Bahnschrift Light', 12))
		self.contact_entry.config(font=('Bahnschrift Light', 12))
		self.email_lbl.config(font=('Bahnschrift Light', 12))
		self.email_entry.config(font=('Bahnschrift Light', 12))

		self.gender_lbl.config(font=('Bahnschrift Light', 12))
		self.gender_cbox.config(font=('Bahnschrift Light', 12))

		self.lname_entry_tooltip.font = ('Bahnschrift Light', 12)
		self.fname_entry_tooltip.font = ('Bahnschrift Light', 12)
		self.mname_entry_tooltip.font = ('Bahnschrift Light', 12)
		self.address_entry_tooltipfont = ('Bahnschrift Light', 12)
		self.month_cbox_tooltip.font = ('Bahnschrift Light', 12)
		self.day_entry_tooltip.font = ('Bahnschrift Light', 12)
		self.year_entry_tooltip.font = ('Bahnschrift Light', 12)
		self.contact_entry_tooltip.font = ('Bahnschrift Light', 12)
		self.email_entry_tooltip.font = ('Bahnschrift Light', 12)
		self.gender_entry_tooltip.font = ('Bahnschrift Light', 12)

class ProfilePage(Page):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master)

		self.sectionmng = PageManager()

		self.general_frm = tk.LabelFrame(master=self, text='General Information')
		self.general_toggle_btn = tk.Button(master=self.general_frm, text='Open Section', 
			height=1, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=lambda: self.set_section('general'))
		self.general_section = GeneralSection(master=self.general_frm)
		self.general_toggle_btn.pack(fill='x', padx=5, pady=5)
		self.general_frm.pack(fill='both', padx=10, pady=10)
		
		self.sectionmng.add_page('general', self.general_section)
		self.set_section('general')

		self.reload_page()

	def reload_page(self, event=None) -> None:
		pass

	def set_section(self, name: str) -> None:
		self.sectionmng.current_page = name

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
		if self.current_page is not value:
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
#   https://stackoverflow.com/questions/3221966/how-do-i-display-tooltips-in-tkinter
#   Though I have added some modifications
#   TODO: 
#   - Add fade in and out
class Tooltip:
	def __init__(self, widget, *, bd=1, bg='#FFFFEA', pad=(6, 3, 6, 3), 
		text='This is a tooltip', font=('Bahnschrift Light', 10), waittime=300, 
		wraplength=260):

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

	def tip_pos_calc(self, widget, label, tip_delta=(10, 6), pad=(6, 3, 6, 3)
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

class DynamicResize:
	def __init__(self, parent: tk.Widget) -> None:

		self.parent = parent
		self.children: Dict[tk.Widget, Dict[str, Any]] = {}
		self.parent.bind('<Configure>', self)

	def add_child(self, child: tk.Widget, font: str='Bahnschrift Light', 
		fontsize: int=16, maxfontsize: int=20, minfontsize: int=6) -> None:
		"""Add a child.

		Args:
			child (tk.Widget): The child to be added.
			font (str): The font to be used. Defaults to 'Bahnschrift Light.'
			fontsize (int): The fontsize to scale the child from. Defaults to 
			16.
			maxfontsize (int): The maximum fontsize. Defaults to 20.
			minfontsize (int): The minimum fontsize. Defaults to 6.
			overwrite (bool): Determines whether to overwrite an existing child
			or not. Defaults to True
		"""
			
		self.children[child] = {
			'font': font,
			'fontsize': fontsize,
			'maxfontsize': maxfontsize,
			'minfontsize': minfontsize
		}

	def del_child(self, child: tk.Widget) -> None:

		if self.children.pop(child, None) is None:
			raise KeyError(f'Child not in children.')

	def __call__(self, _=None) -> None:
		
		for child, values in self.children.items():
			try:
				if self.parent.winfo_height() > self.parent.winfo_width():
					ratio = (self.parent.winfo_width()/self.parent.winfo_screenwidth())
				else:
					ratio = (self.parent.winfo_height()/self.parent.winfo_screenheight())
				fontsize = round(ratio * values['fontsize'])
				if fontsize > values['maxfontsize']:
					fontsize = values['maxfontsize']
				elif fontsize < values['minfontsize']:
					fontsize = values['minfontsize']
				child.config(font=(values['font'], fontsize))
			except Exception:
				continue