#   Handles how the app looks

#   Libraries
import tkinter as tk
import os
from abc import ABC, abstractmethod
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from tkinter import filedialog, ttk
from tkinter import messagebox as msgbox
from typing import Any, Dict, Tuple, List

import constants
import data
import misc

#   Code
class Page(ABC, tk.Frame):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)
		self.master = master
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
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.open)
		self.open_recent_btn = tk.Button(master=self.inner_r_frm, text='Open Recent', 
			height=3, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.open_recent)
		self.more_btn = tk.Button(master=self.inner_r_frm, text='More Actions', 
			height=3, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		self.exit_btn = tk.Button(master=self.inner_r_frm, text='Exit', height=3, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.master.exit)
		self.new_btn.pack(expand=True, fill='x', padx=6, pady=(20, 2))
		self.open_btn.pack(expand=True, fill='x', padx=6, pady=2)
		self.open_recent_btn.pack(expand=True, fill='x', padx=6, pady=2)
		self.more_btn.pack(expand=True, fill='x', padx=6, pady=(2, 10))
		self.exit_btn.pack(expand=True, fill='x', padx=6, pady=10)
		self.inner_r_frm.pack(expand=True, fill='x', padx=(10, 30))
		self.r_frm.pack(expand=True, fill='both', side='right')
		
		self.search_bar_tt = Tooltip(self.search_bar, text='Search Bar', 
			font=('Bahnschrift Light', 10))
		self.new_btn_tt = Tooltip(self.new_btn, text='Create a New Profile', 
			font=('Bahnschrift Light', 10))
		self.open_btn_tt = Tooltip(self.open_btn, text='Access a Profile', 
			font=('Bahnschrift Light', 10))
		self.open_recent_btn_tt = Tooltip(self.open_recent_btn, text='Open a recently-accessed profile.', 
			font=('Bahnschrift Light', 10))
		self.more_btn_tt = Tooltip(self.more_btn, text='More Actions...', 
			font=('Bahnschrift Light', 10))
		self.exit_btn_tt = Tooltip(self.exit_btn, text='Exit SDS', 
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

		self.search_bar_tt.font = ('Bahnschrift Light', 10)
		self.new_btn_tt.font = ('Bahnschrift Light', 10)
		self.open_btn_tt.font = ('Bahnschrift Light', 10)
		self.open_recent_btn_tt.font = ('Bahnschrift Light', 10)
		self.more_btn_tt.font = ('Bahnschrift Light', 10)
		self.exit_btn_tt.font = ('Bahnschrift Light', 10)

	def new(self, event=None) -> None:
		self.master.pagemng.current_page = 'newpage'

	def open(self, event=None) -> None:
		self.master.pagemng.current_page = 'openpage'

	def open_recent(self, event=None) -> None:
		# self.master.pagemng.current_page = 
		pass

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

		self.dynresize = DynamicResize(self)
		self.dynresize.add_child(self.title, 'Bahnschrift', 36, 40, 10)
		self.dynresize.add_child(self.student_btn, 'Bahnschrift Light', 16, 20, 6)
		self.dynresize.add_child(self.teacher_btn, 'Bahnschrift Light', 16, 20, 6)
		self.dynresize.add_child(self.section_btn, 'Bahnschrift Light', 16, 20, 6)
		self.dynresize.add_child(self.back_btn, 'Bahnschrift Light', 16, 20, 6)

		self.student_btn_tt = Tooltip(self.student_btn, 
			text='Create a New Student Profile', font=('Bahnschrift Light', 10))
		self.teacher_btn_tt = Tooltip(self.teacher_btn, 
			text='Create a New Teacher Profile', font=('Bahnschrift Light', 10))
		self.section_btn_tt = Tooltip(self.section_btn, 
			text='Create a New Section', font=('Bahnschrift Light', 10))
		self.back_btn_tt = Tooltip(self.back_btn, 
			text='Go Back to Previous Page', font=('Bahnschrift Light', 10))

		self.reload_page()

	def reload_page(self) -> None:
		
		self.title.config(font=('Bahnschrift', 36))
		self.student_btn.config(font=('Bahnschrift Light', 16))
		self.teacher_btn.config(font=('Bahnschrift Light', 16))
		self.section_btn.config(font=('Bahnschrift Light', 16))
		self.back_btn.config(font=('Bahnschrift Light', 16))

		self.student_btn_tt.font = ('Bahnschrift Light', 10)
		self.student_btn_tt.font = ('Bahnschrift Light', 10)
		self.teacher_btn_tt.font = ('Bahnschrift Light', 10)
		self.section_btn_tt.font = ('Bahnschrift Light', 10)
		self.back_btn_tt.font = ('Bahnschrift Light', 10)

	def back(self) -> None:

		self.master.pagemng.back()

	def student(self) -> None:
		
		self.master.pagemng.pages['pfppage'] = StudentProfilePage(self.master)
		self.master.pagemng.current_page = 'pfppage'

	def teacher(self) -> None:

		self.master.pagemng.pages['pfppage'] = TeacherProfilePage(self.master)
		self.master.pagemng.current_page = 'pfppage'

	def section(self) -> None:
		
		self.master.pagemng.pages['pfppage'] = SectionProfilePage(self.master)
		self.master.pagemng.current_page = 'pfppage'

class OpenPage(Page):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		self.inner_frm = tk.Frame(master=self)
		self.title = tk.Label(master=self.inner_frm, text='Open a Profile')
		self.back_btn = tk.Button(master=self.inner_frm, text='Back', 

			height=3, relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.back)

		self.title.pack(expand=True, fill='x', side='top', pady=10)
		self.back_btn.pack(expand=True, fill='x', padx=10, pady=(10, 0))

		self.dynresize = DynamicResize(self)
		self.dynresize.add_child(self.title, 'Bahnschrift', 36, 40, 10)
		self.dynresize.add_child(self.back_btn, 'Bahnschrift Light', 16, 20, 6)

		self.back_btn_tt = Tooltip(self.back_btn, 
			text='Go Back to Previous Page', font=('Bahnschrift Light', 10))
		self.inner_frm.pack(expand=True, fill='x', padx=30)

		self.reload_page()

	def reload_page(self, event=None) -> None:
		pass

	def back(self) -> None:

		self.master.pagemng.back()

class ProfilePage(Page):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		self._edit = True

		self.tabmng = ttk.Notebook(master=self)
		self.tabmng.pack(fill='both', expand=True)

		#	General Frame
		self.general_frm = tk.Frame(self)

		#	Profile Pic
		self.img = None
		self.img_path = None
		self.pic_frm = tk.Frame(self.general_frm)
		self.inner_pic_frm = tk.Frame(self.pic_frm, width=150, height=150)
		self.pic_btn = tk.Button(master=self.inner_pic_frm, text='Select Picture', 
			relief='solid', bd=1, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.select_pic)
		self.pic_btn.pack(expand=True, fill='both')
		self.inner_pic_frm.pack()
		self.inner_pic_frm.pack_propagate(False)
		self.pic_frm.pack(fill='x', padx=10, pady=2)

		#	Name
		self.name_frm = tk.Frame(master=self.general_frm)
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
		self.address_frm = tk.Frame(master=self.general_frm)
		self.address_lbl = tk.Label(master=self.address_frm, text='Address')
		self.address_entry = tk.Entry(master=self.address_frm, relief='groove', bd=2)

		self.address_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.address_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.address_frm.columnconfigure(1, weight=1)

		self.address_frm.pack(fill='x', padx=10, pady=2)

		#	Birthday
		self.bday_frm = tk.Frame(master=self.general_frm)
		self.bday_lbl = tk.Label(master=self.bday_frm, text='Date of Birth')
		self.bday_entry = DateEntry(master=self.bday_frm, relief='groove', bd=2, state='readonly', 
			firstweekday='sunday')

		self.bday_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.bday_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.bday_frm.columnconfigure(1, weight=1)

		self.bday_frm.pack(fill='x', padx=10, pady=2)

		#	Contacts
		self.contacts_frm = tk.Frame(master=self.general_frm)
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
		self.gender_frm = tk.Frame(master=self.general_frm)
		self.gender_lbl = tk.Label(master=self.gender_frm, text='Gender / Sex')
		self.gender_cbox = ttk.Combobox(master=self.gender_frm, state='readonly', values=constants.GENDERS)

		self.gender_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.gender_cbox.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		
		self.gender_frm.columnconfigure(1, weight=1)

		self.gender_frm.pack(fill='x', padx=10, pady=2)

		self.general_frm.pack(expand=True, fill='both')

		self.tabmng.add(self.general_frm, text='General Information')

		#	Buttons
		self.btns_frm = tk.Frame(self)
		self.back_btn = tk.Button(master=self, text='Back', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.back)
		self.edit_toggle_btn = tk.Button(master=self, text='Save', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.toggle_edit)

		self.back_btn.pack(expand=True, fill='x', padx=(10, 5), pady=10, side='left')
		self.edit_toggle_btn.pack(expand=True, fill='x', padx=(5, 10), pady=10, side='right')
		self.btns_frm.pack(fill='x')
		
		self.dynresize = DynamicResize(self.master)
		self.dynresize.add_child(self.pic_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.lname_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.lname_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.fname_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.fname_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.mname_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.mname_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.address_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.address_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.bday_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.bday_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.contact_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.contact_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.email_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.email_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.gender_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.gender_cbox, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.edit_toggle_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.back_btn, 'Bahnschrift Light', 14, 16, 6)

		self.pic_btn_tt = Tooltip(self.pic_btn, text='Click to Select Picture')
		self.lname_entry_tt = Tooltip(self.lname_entry, text='Last Name, Optional')
		self.fname_entry_tt = Tooltip(self.fname_entry, text='First Name')
		self.mname_entry_tt = Tooltip(self.mname_entry, text='Full Middle Name, Optional')
		self.address_entry_tt = Tooltip(self.address_entry, text='Address')
		self.bday_entry_tt = Tooltip(self.bday_entry, text='Birthday in MM/DD/YYYY format')
		self.contact_entry_tt = Tooltip(self.contact_entry, text='Contact Number, Optional')
		self.email_entry_tt = Tooltip(self.email_entry, text='Email Address, Optional')
		self.gender_cbox_tt = Tooltip(self.gender_cbox, text='Gender')
		self.edit_toggle_btn_tt = Tooltip(self.edit_toggle_btn, text='Save the Profile')
		self.back_btn_tt = Tooltip(self.back_btn, text='Go Back to Menu')

		#	Note: Call self.reload_page() on subclasses
		self.master.protocol('WM_DELETE_WINDOW', self.exit)
	
	@property
	def edit(self) -> bool:
		return self._edit

	@edit.setter
	def edit(self, value: bool) -> None:
		if value:
			self.unlock()
			self._edit = value
		else:
			if self.save():
				self.lock()
				self._edit = value
			else:
				return

		self.reload_page()

	def back(self, event=None) -> None:

		if self.edit:
			response = msgbox.askyesnocancel(constants.TITLE, 
				'Do you want to save the profile?')
			if response == True:
				self.edit = False
			elif response == False:
				pass
			elif response is None:
				return

		self.master.protocol('WM_DELETE_WINDOW', self.master.exit)

		self.master.pagemng.current_page = 'homepage'
		self.master.pagemng.previous_page = None

	def lock(self, event=None) -> None:
		"""Locks all of the widgets so they cannot be modified"""
		
		self.lname_entry.config(state='disabled')
		self.fname_entry.config(state='disabled')
		self.mname_entry.config(state='disabled')
		self.address_entry.config(state='disabled')
		self.bday_entry.config(state='disabled')
		self.contact_entry.config(state='disabled')
		self.email_entry.config(state='disabled')
		self.gender_cbox.config(state='disabled')

	def unlock(self, event=None) -> None:
		"""Unlocks all of the widgets so they can be modified"""
		
		self.lname_entry.config(state='normal')
		self.fname_entry.config(state='normal')
		self.mname_entry.config(state='normal')
		self.address_entry.config(state='normal')
		self.bday_entry.config(state='readonly')
		self.contact_entry.config(state='normal')
		self.email_entry.config(state='normal')
		self.gender_cbox.config(state='normal')

	def exit(self, event=None) -> None:
		if self.edit:
			response = msgbox.askyesnocancel(constants.TITLE, 
				'Do you want to save the profile?')
			if response == True:
				self.edit = False
			elif response == False:
				pass
			elif response is None:
				return

		self.master.exit()

	def toggle_edit(self) -> None:
		self.edit = not self.edit

	def select_pic(self, event=None) -> None:

		if not self.edit:
			return

		self.img_path = filedialog.askopenfilename(
			filetypes=constants.SUPPORTED_IMG_TYPES)

		try:
			with Image.open(self.img_path) as img:
				self.img = ImageTk.PhotoImage(img.resize((150, 150)))
				self.pic_btn.config(text='', image=self.img)
		except AttributeError:
			pass
		except Exception:
			msgbox.showerror(constants.TITLE, 
				'An error occured while processing your image.')

	def reload_page(self, event=None) -> None:
		
		self.pic_btn.config(font=('Bahnschrift Light', 14))

		self.lname_lbl.config(font=('Bahnschrift Light', 14))
		self.lname_entry.config(font=('Bahnschrift Light', 14))
		self.fname_lbl.config(font=('Bahnschrift Light', 14))
		self.fname_entry.config(font=('Bahnschrift Light', 14))
		self.mname_lbl.config(font=('Bahnschrift Light', 14))
		self.mname_entry.config(font=('Bahnschrift Light', 14))

		self.address_lbl.config(font=('Bahnschrift Light', 14))
		self.address_entry.config(font=('Bahnschrift Light', 14))

		self.bday_lbl.config(font=('Bahnschrift Light', 14))
		self.bday_entry.config(font=('Bahnschrift Light', 14))

		self.contact_lbl.config(font=('Bahnschrift Light', 14))
		self.contact_entry.config(font=('Bahnschrift Light', 14))
		self.email_lbl.config(font=('Bahnschrift Light', 14))
		self.email_entry.config(font=('Bahnschrift Light', 14))

		self.gender_lbl.config(font=('Bahnschrift Light', 14))
		self.gender_cbox.config(font=('Bahnschrift Light', 14))

		self.edit_toggle_btn.config(font=('Bahnschrift Light', 14))
		self.back_btn.config(font=('Bahnschrift Light', 14))

		self.pic_btn_tt.font = ('Bahnschrift Light', 10)
		self.lname_entry_tt.font = ('Bahnschrift Light', 10)
		self.fname_entry_tt.font = ('Bahnschrift Light', 10)
		self.mname_entry_tt.font = ('Bahnschrift Light', 10)
		self.address_entry_tt.font = ('Bahnschrift Light', 10)
		self.bday_entry_tt.font = ('Bahnschrift Light', 10)
		self.contact_entry_tt.font = ('Bahnschrift Light', 10)
		self.email_entry_tt.font = ('Bahnschrift Light', 10)
		self.gender_cbox_tt.font = ('Bahnschrift Light', 10)
		self.edit_toggle_btn_tt.font = ('Bahnschrift Light', 10)
		self.back_btn_tt.font = ('Bahnschrift Light', 10)

		if self.edit:
			self.edit_toggle_btn.config(text='Save')
		else:
			self.edit_toggle_btn.config(text='Edit')
	
class StudentProfilePage(ProfilePage):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		self.active_profile = None
		self.section_path = None

		#	Parents in General Frame
		self.parents_frm = tk.Frame(master=self.general_frm)
		self.parents_lbl = tk.Label(master=self.parents_frm, text='Parents/Guardians (Separate w/ Comma)')
		self.parents_entry = tk.Entry(master=self.parents_frm, relief='groove', bd=2)

		self.parents_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.parents_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.parents_frm.columnconfigure(1, weight=1)
		self.parents_frm.pack(fill='x', padx=10, pady=2)

		#	Student Frame
		self.student_frm = tk.Frame(master=self)

		#	Learners Reference Number
		self.lrn_frm = tk.Frame(master=self.student_frm)
		self.lrn_lbl = tk.Label(master=self.lrn_frm, text='Learner\'s Reference Number (LRN)')
		self.lrn_entry = tk.Entry(master=self.lrn_frm, relief='groove', bd=2)

		self.lrn_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.lrn_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.lrn_frm.columnconfigure(1, weight=1)

		self.lrn_frm.pack(fill='x', padx=10, pady=2)
		
		#	Grade Level
		self.grade_frm = tk.Frame(master=self.student_frm)
		self.grade_lbl = tk.Label(master=self.grade_frm, text='Grade Level')
		self.grade_cbox = ttk.Combobox(master=self.grade_frm, state='readonly', values=constants.GRADE_LVLS)

		self.grade_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.grade_cbox.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.grade_frm.columnconfigure(1, weight=1)

		self.grade_frm.pack(fill='x', padx=10, pady=2)

		#	Section
		self.section_frm = tk.Frame(master=self.student_frm)
		self.section_lbl = tk.Label(master=self.section_frm, text='Section, Optional')
		self.section_entry = tk.Entry(master=self.section_frm, relief='groove', bd=2)

		self.section_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.section_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.section_frm.columnconfigure(1, weight=1)

		self.section_frm.pack(fill='x', padx=10, pady=2)
		
		self.student_frm.pack(expand=True, fill='both')

		#	School Year
		self.sy_frm = tk.Frame(master=self.student_frm)
		self.sy1_lbl = tk.Label(master=self.sy_frm, text='School Year (From)')
		self.sy_from_entry = tk.Entry(master=self.sy_frm, relief='groove', bd=2)
		self.sy2_lbl = tk.Label(master=self.sy_frm, text='School Year (To)')
		self.sy_to_entry = tk.Entry(master=self.sy_frm, relief='groove', bd=2)

		self.sy1_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.sy_from_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.sy2_lbl.grid(column=3, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.sy_to_entry.grid(column=4, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		
		self.sy_frm.columnconfigure(1, weight=1)
		self.sy_frm.columnconfigure(4, weight=1)

		self.sy_frm.pack(fill='x', padx=10, pady=2)

		#	Grades Frame
		self.grades_frm = tk.Frame(master=self)

		self.grades_frm.pack(expand=True, fill='both')

		self.tabmng.add(self.student_frm, text='Student\'s Information')
		self.tabmng.add(self.grades_frm, text='Grades and Attendance')

		self.dynresize.add_child(self.parents_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.parents_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.lrn_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.lrn_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.grade_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.grade_cbox, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.section_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.section_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.sy1_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.sy_from_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.sy2_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.sy_to_entry, 'Bahnschrift Light', 14, 16, 6)

		self.parent_entry_tt = Tooltip(self.parents_entry, text='Parents, Separate w/ Comma, Optional')
		self.lrn_entry_tt = Tooltip(self.lrn_entry, text='Learner\'s Reference Number')
		self.grade_cbox_tt = Tooltip(self.grade_cbox, text='Grade Level')
		self.section_entry_tt = Tooltip(self.section_entry, text='Section / Class Name, Optional')
		
		self.section_entry.bind('<ButtonRelease-1>', self.section_link)

		self.reload_page()
	
	def save(self) -> bool:

		required = {
			'Picture': misc.convert_blank(self.img_path),
			'First Name': misc.convert_blank(self.fname_entry.get()),
			'Address': misc.convert_blank(self.address_entry.get()),
			'Gender': misc.convert_blank(self.gender_cbox.get()),
			'Parents': misc.convert_blank(self.parents_entry.get()),
			'Learner\'s Reference Number': misc.convert_blank(self.lrn_entry.get()),
			'School Year (From)': misc.convert_blank(self.sy_from_entry.get()),
			'School Year (To)': misc.convert_blank(self.sy_to_entry.get()),
			'Grade Level': misc.convert_blank(self.grade_cbox.get())
		}

		for key, info in required.items():
			if info is None:
				msgbox.showerror(constants.TITLE, f'{key} required.')
				return False

		section = misc.convert_blank(self.section_entry.get())
		self.section_path = None
		if section is not None:
			sections = {section.name: section.path for section in \
				self.master.sectionloader.items if section.grade_lvl == required['Grade Level']}
			try:
				self.section_path = sections[section]
			except KeyError:
				msgbox.showerror(constants.TITLE, f'The section \'{section}\' does not exist.')
				self.section_entry.delete(0, 'end')
				return

		try:
			self.active_profile.path = os.path.join(constants.PATHS.STUDENTS.value,
					constants.FILENAME_FORMATS.STUDENT.value.format(
						lname=self.lname_entry.get().replace(' ', ''),
						fname=required['First Name'].replace(' ', ''),
						mname=self.mname_entry.get().replace(' ', '')))
			self.active_profile.pic = required['Picture']
			self.active_profile.fname = required['First Name']
			self.active_profile.bday = self.bday_entry.get_date()
			self.active_profile.address = required['Address']
			self.active_profile.sex = required['Gender']
			self.active_profile.lrn = required['Learner\'s Reference Number']
			self.active_profile.sy = (required['School Year (From)'], 
				required['School Year (To)'])
			self.active_profile.grade_lvl = required['Grade Level']
			self.active_profile.section = self.section_path
			self.active_profile.contact_no = misc.convert_blank(self.contact_entry.get())
			self.active_profile.email = misc.convert_blank(self.email_entry.get())
			self.active_profile.mname = misc.convert_blank(self.mname_entry.get())
			self.active_profile.lname = misc.convert_blank(self.lname_entry.get())
		except (AttributeError, OSError):
			self.active_profile = data.Student(
				os.path.join(constants.PATHS.STUDENTS.value,
					constants.FILENAME_FORMATS.STUDENT.value.format(
						lname=self.lname_entry.get().replace(' ', ''),
						fname=required['First Name'].replace(' ', ''),
						mname=self.mname_entry.get().replace(' ', ''))), 
				required['Picture'], 
				required['First Name'],
				self.bday_entry.get_date(),
				required['Address'],
				required['Gender'],
				required['Learner\'s Reference Number'],
				(required['School Year (From)'], required['School Year (To)']),
				required['Parents'].split(','),
				required['Grade Level'],
				self.section_path,
				misc.convert_blank(self.contact_entry.get()),
				misc.convert_blank(self.email_entry.get()),
				misc.convert_blank(self.mname_entry.get()),
				misc.convert_blank(self.lname_entry.get()))
			
		self.active_profile.dump()

		return True

	def lock(self, event=None) -> None:
		super().lock(event)

		self.parents_entry.config(state='disabled')
		self.lrn_entry.config(state='disabled')
		self.grade_cbox.config(state='disabled')
		self.section_entry.config(state='disabled')
		self.sy_from_entry.config(state='disabled')
		self.sy_to_entry.config(state='disabled')

	def unlock(self, event=None) -> None:

		super().unlock(event)

		self.parents_entry.config(state='normal')
		self.lrn_entry.config(state='normal')
		self.grade_cbox.config(state='readonly')
		self.section_entry.config(state='normal')
		self.sy_from_entry.config(state='normal')
		self.sy_to_entry.config(state='normal')

	def reload_page(self, event=None) -> None:

		super().reload_page(event)

		self.parents_lbl.config(font=('Bahnschrift Light', 14))
		self.parents_entry.config(font=('Bahnschrift Light', 14))

		self.lrn_lbl.config(font=('Bahnschrift Light', 14))
		self.lrn_entry.config(font=('Bahnschrift Light', 14))

		self.grade_lbl.config(font=('Bahnschrift Light', 14))
		self.grade_cbox.config(font=('Bahnschrift Light', 14))

		self.section_lbl.config(font=('Bahnschrift Light', 14))
		self.section_entry.config(font=('Bahnschrift Light', 14))

		self.sy1_lbl.config(font=('Bahnschrift Light', 14))
		self.sy_from_entry.config(font=('Bahnschrift Light', 14))
		self.sy2_lbl.config(font=('Bahnschrift Light', 14))
		self.sy_to_entry.config(font=('Bahnschrift Light', 14))
		
		self.parent_entry_tt.font = ('Bahnschrift Light', 10) 
		self.lrn_entry_tt.font = ('Bahnschrift Light', 10)
		self.grade_cbox_tt.font = ('Bahnschrift Light', 10)
		self.section_entry_tt.font = ('Bahnschrift Light', 10)
		if self.edit:
			self.section_entry_tt.text = 'Section, Optional'
		else:
			self.section_entry_tt.text = 'Section, Click to Open'

	def section_link(self, event=None) -> None:
		
		if not self.edit and self.section_path is not None:
			if os.path.exists(self.section_path):
				self.master.protocol('WM_DELETE_WINDOW', self.master.exit)

				# self.master.pagemng.pages['pfppage'] = SectionProfilePage.construct
				self.master.pagemng.previous_page = None

class TeacherProfilePage(ProfilePage):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		self.active_profile = None
		self.teacher_frm = tk.Frame(self)
		self.sections = []

		#	Advisory Section Input:
		self.advisorycls_input_frm = tk.Frame(self.teacher_frm)
		self.advisorycls_input_lbl = tk.Label(master=self.advisorycls_input_frm, text='Advisory Class')
		self.advisorycls_input_entry = tk.Entry(master=self.advisorycls_input_frm, relief='groove', bd=2)

		self.advisorycls_input_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.advisorycls_input_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.advisorycls_input_frm.columnconfigure(1, weight=1)
		self.advisorycls_input_frm.pack(fill='x', padx=10, pady=2)

		#	Section
		self.section_frm = tk.Frame(self.teacher_frm)

		#	Input for the sections
		self.section_input_frm = tk.Frame(self.section_frm)
		self.section_input_lbl = tk.Label(master=self.section_input_frm, text='Section')
		self.section_input_entry = tk.Entry(master=self.section_input_frm, relief='groove', bd=2)

		self.section_input_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.section_input_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.section_input_frm.columnconfigure(1, weight=1)

		self.inner_section_frm = tk.Frame(self.section_frm)
		self.section_list_scrollbar = tk.Scrollbar(master=self.inner_section_frm)
		self.section_list = tk.Listbox(master=self.inner_section_frm, yscrollcommand=self.section_list_scrollbar.set, 
			relief='groove', bd=2)
		self.section_list_scrollbar.config(command=self.section_list.yview)
		self.section_list_scrollbar.pack(fill='y', side='right')
		self.section_list.pack(expand=True, fill='both', side='left')

		self.section_btns_frm = tk.Frame(self.section_frm)
		self.add_section_btn = tk.Button(master=self.section_btns_frm, text='Add', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.add_section)
		self.remove_section_btn = tk.Button(master=self.section_btns_frm, text='Remove', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		self.open_section_btn = tk.Button(master=self.section_btns_frm, text='Open', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')

		self.add_section_btn.grid(column=0, row=0, sticky='nsew', padx=6, pady=2)
		self.remove_section_btn.grid(column=1, row=0, sticky='nsew', padx=6, pady=2)
		self.open_section_btn.grid(column=2, row=0, sticky='nsew', padx=6, pady=2)
		self.section_btns_frm.columnconfigure(0, weight=1)
		self.section_btns_frm.columnconfigure(1, weight=1)
		self.section_btns_frm.columnconfigure(2, weight=1)

		self.section_input_frm.pack(fill='x', pady=2)
		self.inner_section_frm.pack(fill='x', pady=2)
		self.section_btns_frm.pack(fill='x', pady=2)
		self.section_frm.pack(fill='x', padx=10, pady=2)

		self.teacher_frm.pack(expand=True, fill='both')

		self.tabmng.add(self.teacher_frm, text='Teacher\'s Information')

		self.dynresize.add_child(self.advisorycls_input_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.advisorycls_input_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.section_input_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.section_input_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.section_list, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.add_section_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.remove_section_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.open_section_btn, 'Bahnschrift Light', 14, 16, 6)

		self.advisorycls_input_entry_tt = Tooltip(self.advisorycls_input_entry, text='Advisory Class, Optional')
		self.section_input_entry_tt = Tooltip(self.section_input_entry, text='Add a Section')
		self.section_list_tt = Tooltip(self.section_list, text='All the Sections the Teacher Holds')
		self.add_section_btn_tt = Tooltip(self.add_section_btn, text='Add a Section')
		self.remove_section_btn_tt = Tooltip(self.remove_section_btn, text='Remove the Selected Section')
		self.open_section_btn_tt = Tooltip(self.open_section_btn, text='Open the Selected Section')

		self.advisorycls_input_entry.bind('<ButtonRelease-1>', self.section_link)

	def lock(self, event=None) -> None:

		super().lock(event)

		self.advisorycls_input_entry.config(state='disabled')
		self.section_input_entry.config(state='disabled')
		self.add_section_btn.config(state='disabled')
		self.remove_section_btn.config(state='disabled')

	def unlock(self, event=None) -> None:
		
		super().unlock(event)
		self.advisorycls_input_entry.config(state='disabled')
		self.section_input_entry.config(state='disabled')
		self.add_section_btn.config(state='disabled')
		self.remove_section_btn.config(state='disabled')

	def reload_page(self, event=None) -> None:

		super().reload_page(event)

		self.advisorycls_input_lbl.config(font=('Bahnschrift Light', 14))
		self.advisorycls_input_entry.config(font=('Bahnschrift Light', 14))
		self.section_input_lbl.config(font=('Bahnschrift Light', 14))
		self.section_input_entry.config(font=('Bahnschrift Light', 14))
		self.section_list.config(font=('Bahnschrift Light', 14))
		self.add_section_btn.config(font=('Bahnschrift Light', 14))
		self.remove_section_btn.config(font=('Bahnschrift Light', 14))
		self.open_section_btn.config(font=('Bahnschrift Light', 14))

		self.advisorycls_input_entry_tt.font = ('Bahnschrift Light', 10)
		self.section_input_entry_tt.font = ('Bahnschrift Light', 10)
		self.section_list_tt.font = ('Bahnschrift Light', 10)
		self.add_section_btn_tt.font = ('Bahnschrift Light', 10)
		self.remove_section_btn_tt.font = ('Bahnschrift Light', 10)
		self.open_section_btn_tt.font = ('Bahnschrift Light', 10)

		self.upd_section_list()

	def save(self, event=None) -> None:
		
		required = {
			'Picture': misc.convert_blank(self.img_path),
			'First Name': misc.convert_blank(self.fname_entry.get()),
			'Address': misc.convert_blank(self.address_entry.get()),
			'Gender': misc.convert_blank(self.gender_cbox.get()),
		}

		for key, info in required.items():
			if info is None:
				msgbox.showerror(constants.TITLE, f'{key} required.')
				return False

		section = misc.convert_blank(self.advisorycls_input_entry.get())
		self.section_path = None
		if section is not None:
			sections = {section.name: section.path for section in \
				self.master.sectionloader.items}
			try:
				self.section_path: str = sections[section]
			except KeyError:
				msgbox.showerror(constants.TITLE, f'The section \'{section}\' does not exist.')
				self.advisorycls_input_entry.delete(0, 'end')
				return

		self.upd_section_list(event)

		try:
			self.active_profile.path = os.path.join(constants.PATHS.STUDENTS.value,
					constants.FILENAME_FORMATS.STUDENT.value.format(
						lname=self.lname_entry.get().replace(' ', ''),
						fname=required['First Name'].replace(' ', ''),
						mname=self.mname_entry.get().replace(' ', '')))
			self.active_profile.pic = required['Picture']
			self.active_profile.fname = required['First Name']
			self.active_profile.bday = self.bday_entry.get_date()
			self.active_profile.address = required['Address']
			self.active_profile.sex = required['Gender']
			self.active_profile.advisory_cls = self.section_path
			self.active_profile.contact_no = misc.convert_blank(self.contact_entry.get())
			self.active_profile.email = misc.convert_blank(self.email_entry.get())
			self.active_profile.mname = misc.convert_blank(self.mname_entry.get())
			self.active_profile.lname = misc.convert_blank(self.lname_entry.get())
		except (AttributeError, OSError):
			self.active_profile = data.Teacher(
				os.path.join(constants.PATHS.TEACHERS.value,
					constants.FILENAME_FORMATS.TEACHER.value.format(
						lname=self.lname_entry.get().replace(' ', ''),
						fname=required['First Name'].replace(' ', ''),
						mname=self.mname_entry.get().replace(' ', ''))), 
				required['Picture'], 
				required['First Name'],
				self.bday_entry.get_date(),
				required['Address'],
				required['Gender'],
				self.section_path,
				[data.Section.construct(item[1]) for item in self.sections],
				misc.convert_blank(self.contact_entry.get()),
				misc.convert_blank(self.email_entry.get()),
				misc.convert_blank(self.mname_entry.get()),
				misc.convert_blank(self.lname_entry.get()))

		self.active_profile.sections = self.sections
			
		self.active_profile.dump()

		return True

	def add_section(self, event=None) -> None:

		target = misc.convert_blank(self.section_input_entry.get())
		self.section_path = None
		if target is not None:
			sections = {section.name: section.path for section in \
				self.master.sectionloader.items}
			try:
				section_path = sections[target]
				self.active_profile.append([target, section_path])
				self.upd_section_list(self, event)
			except KeyError:
				msgbox.showerror(constants.TITLE, f'The section \'{target}\' does not exist.')
				return

	def upd_section_list(self, event=None) -> None:

		self.section_list.delete(0, 'end')
		self.sections = [item for item in self.sections if os.path.exists(item[1])]
		self.section_list.insert('end', *[item[0] for item in self.sections])

	def section_link(self, event=None) -> None:
		
		if not self.edit and self.section_path is not None:
			if os.path.exists(self.section_path):
				self.master.protocol('WM_DELETE_WINDOW', self.master.exit)

				self.master.pagemng.pages['pfppage'] = \
					SectionProfilePage.load(data.Section.construct(self.section_path))
				self.master.pagemng.previous_page = None

class SectionProfilePage(Page):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		self._edit = True
		self.adviser_path = None
		self.active_section = None
		self.teachers = []
		self.students = []

		#	Tab Manager
		self.tabmng = ttk.Notebook(master=self)
		self.tabmng.pack(fill='both', expand=True)

		#	General Frame
		self.general_frm = tk.Frame(self)

		#	Section Name
		self.name_frm = tk.Frame(self.general_frm)
		self.name_lbl = tk.Label(master=self.name_frm, text='Section Name')
		self.name_entry = tk.Entry(master=self.name_frm, relief='groove', bd=2)

		self.name_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.name_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.name_frm.columnconfigure(1, weight=1)
		self.name_frm.pack(fill='x', padx=10, pady=2)
		
		#	Grade Level
		self.grade_frm = tk.Frame(master=self.general_frm)
		self.grade_lbl = tk.Label(master=self.grade_frm, text='Grade Level')
		self.grade_cbox = ttk.Combobox(master=self.grade_frm, state="readonly", values=constants.GRADE_LVLS)

		self.grade_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.grade_cbox.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.grade_frm.columnconfigure(1, weight=1)
		self.grade_frm.pack(fill='x', padx=10, pady=2)

		#	Adviser
		self.adviser_frm = tk.Frame(self.general_frm)
		self.adviser_lbl = tk.Label(master=self.adviser_frm, text='Adviser')
		self.adviser_entry = tk.Entry(master=self.adviser_frm, relief='groove', bd=2)

		self.adviser_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.adviser_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.adviser_frm.columnconfigure(1, weight=1)
		self.adviser_frm.pack(fill='x', padx=10, pady=2)

		#	Teacher List
		self.teachers_lbl = tk.Label(master=self.general_frm, text='Teachers', anchor='w')
		self.teachers_lbl.pack(fill='x', padx=10, pady=2)
		self.teachers_frm = tk.Frame(self.general_frm)
		self.teacher_entry = tk.Entry(master=self.teachers_frm, relief='groove', bd=2)
		self.teacher_entry.pack(fill='x', padx=10, pady=2)
		self.inner_teachers_frm = tk.Frame(self.teachers_frm)
		self.teachers_list_scrollbar = tk.Scrollbar(master=self.inner_teachers_frm)
		self.teachers_list = tk.Listbox(master=self.inner_teachers_frm, yscrollcommand=self.teachers_list_scrollbar.set, 
			relief='groove', bd=2)
		self.teachers_list_scrollbar.config(command=self.teachers_list.yview)
		for i in range(1, 101):
			self.teachers_list.insert(tk.END, f'Keon Clone {i} as Teacher Keon {i}')
		self.teachers_list_scrollbar.pack(fill='y', side='right')
		self.teachers_list.pack(expand=True, fill='both', side='left')
		self.teachers_btns_frm = tk.Frame(self.teachers_frm)
		self.add_teacher_btn = tk.Button(master=self.teachers_btns_frm, text='Add', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		self.remove_teacher_btn = tk.Button(master=self.teachers_btns_frm, text='Remove', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		self.open_teacher_btn = tk.Button(master=self.teachers_btns_frm, text='Open', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		
		self.add_teacher_btn.grid(column=0, row=0, sticky='nsew', padx=6, pady=2)
		self.remove_teacher_btn.grid(column=1, row=0, sticky='nsew', padx=6, pady=2)
		self.open_teacher_btn.grid(column=2, row=0, sticky='nsew', padx=6, pady=2)
		self.teachers_btns_frm.columnconfigure(0, weight=1)
		self.teachers_btns_frm.columnconfigure(1, weight=1)
		self.teachers_btns_frm.columnconfigure(2, weight=1)
		self.inner_teachers_frm.pack(fill='x', padx=10, pady=2)
		self.teachers_btns_frm.pack(fill='x', padx=10, pady=2)
		self.teachers_frm.pack(fill='x', padx=10, pady=2)

		#	Student List
		self.students_lbl = tk.Label(master=self.general_frm, text='Students', anchor='w')
		self.students_lbl.pack(fill='x', padx=10, pady=2)
		self.student_frm = tk.Frame(self.general_frm)
		self.teacher_entry = tk.Entry(master=self.student_frm, relief='groove', bd=2)
		self.teacher_entry.pack(fill='x', padx=10, pady=2)
		self.inner_student_frm = tk.Frame(self.student_frm)
		self.student_list_scrollbar = tk.Scrollbar(master=self.inner_student_frm)
		self.students_list = tk.Listbox(master=self.inner_student_frm, yscrollcommand=self.student_list_scrollbar.set, 
			relief='groove', bd=2)
		self.student_list_scrollbar.config(command=self.students_list.yview)
		for i in range(1, 101):
			self.students_list.insert(tk.END, f'Keon Clone {i} as Student Keon {i}')
		self.student_list_scrollbar.pack(fill='y', side='right')
		self.students_list.pack(expand=True, fill='both', side='left')
		self.student_btns_frm = tk.Frame(self.student_frm)
		self.add_student_btn = tk.Button(master=self.student_btns_frm, text='Add', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		self.remove_student_btn = tk.Button(master=self.student_btns_frm, text='Remove', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		self.open_student_btn = tk.Button(master=self.student_btns_frm, text='Open', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb')
		
		self.add_student_btn.grid(column=0, row=0, sticky='nsew', padx=6, pady=2)
		self.remove_student_btn.grid(column=1, row=0, sticky='nsew', padx=6, pady=2)
		self.open_student_btn.grid(column=2, row=0, sticky='nsew', padx=6, pady=2)
		self.student_btns_frm.columnconfigure(0, weight=1)
		self.student_btns_frm.columnconfigure(1, weight=1)
		self.student_btns_frm.columnconfigure(2, weight=1)
		self.inner_student_frm.pack(fill='x', padx=10, pady=2)
		self.student_btns_frm.pack(fill='x', padx=10, pady=2)
		self.student_frm.pack(fill='x', padx=10, pady=2)

		self.general_frm.pack(expand=True, fill='both')
		self.tabmng.add(self.general_frm, text='General Information')

		self.btns_frm = tk.Frame(self)
		self.back_btn = tk.Button(master=self, text='Back', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.back)
		self.edit_toggle_btn = tk.Button(master=self, text='Save', height=2, 
			relief='solid', bd=0, bg='#e6e6e6', activebackground='#ebebeb',
			command=self.toggle_edit)
		self.back_btn.pack(expand=True, fill='x', padx=(10, 5), pady=10, side='left')
		self.edit_toggle_btn.pack(expand=True, fill='x', padx=(5, 10), pady=10, side='right')
		self.btns_frm.pack(fill='x')

		self.dynresize = DynamicResize(self.master)
		self.dynresize.add_child(self.name_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.name_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.grade_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.grade_cbox, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.adviser_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.adviser_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.teachers_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.teachers_list, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.add_teacher_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.remove_teacher_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.open_teacher_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.students_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.students_list, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.add_student_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.remove_student_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.open_student_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.back_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.edit_toggle_btn, 'Bahnschrift Light', 14, 16, 6)

		self.name_entry_tt = Tooltip(self.name_entry, text='Name of the Section')
		self.grade_cbox_tt = Tooltip(self.grade_cbox, text='Grade Level of the Section')
		self.adviser_entry_tt = Tooltip(self.adviser_entry, text='Adviser of the Section')
		self.edit_toggle_btn_tt = Tooltip(self.edit_toggle_btn, text='Save the Profile')
		self.teachers_list_tt = Tooltip(self.teachers_list, text='List of Teachers in this Section')
		self.add_teacher_btn_tt = Tooltip(self.add_teacher_btn, text='Add a Teacher to the Section')
		self.remove_teacher_btn_tt = Tooltip(self.remove_teacher_btn, text='Remove a Teacher from the Section')
		self.open_teacher_btn_tt = Tooltip(self.open_teacher_btn, text='Open a Teacher\'s Profile')
		self.student_list_tt = Tooltip(self.students_list, text='List of Teachers in this Section')
		self.add_teacher_btn_tt = Tooltip(self.add_teacher_btn, text='Add a Teacher to the Section')
		self.remove_teacher_btn_tt = Tooltip(self.remove_teacher_btn, text='Remove a Teacher from the Section')
		self.open_teacher_btn_tt = Tooltip(self.open_teacher_btn, text='Open a Teacher\'s Profile')
		self.back_btn_tt = Tooltip(self.back_btn, text='Go Back to Menu')

		self.master.protocol('WM_DELETE_WINDOW', self.exit)
		self.reload_page()

	@property
	def edit(self) -> bool:
		return self._edit

	@edit.setter
	def edit(self, value: bool) -> None:
		if value:
			self.unlock()
			self._edit = value
		else:
			if self.save():
				self.lock()
				self._edit = value
			else:
				return

		self.reload_page()

	def reload_page(self, event=None) -> None:

		self.name_lbl.config(font=('Bahnschrift Light', 14))
		self.name_entry.config(font=('Bahnschrift Light', 14))
		self.grade_lbl.config(font=('Bahnschrift Light', 14))
		self.grade_cbox.config(font=('Bahnschrift Light', 14))
		self.adviser_lbl.config(font=('Bahnschrift Light', 14))
		self.adviser_entry.config(font=('Bahnschrift Light', 14))
		self.teachers_lbl.config(font=('Bahnschrift Light', 14))
		self.teachers_list.config(font=('Bahnschrift Light', 14))
		self.add_teacher_btn.config(font=('Bahnschrift Light', 14))
		self.remove_teacher_btn.config(font=('Bahnschrift Light', 14))
		self.open_teacher_btn.config(font=('Bahnschrift Light', 14))
		self.students_lbl.config(font=('Bahnschrift Light', 14))
		self.students_list.config(font=('Bahnschrift Light', 14))
		self.add_student_btn.config(font=('Bahnschrift Light', 14))
		self.remove_student_btn.config(font=('Bahnschrift Light', 14))
		self.open_student_btn.config(font=('Bahnschrift Light', 14))
		self.back_btn.config(font=('Bahnschrift Light', 14))
		self.edit_toggle_btn.config(font=('Bahnschrift Light', 14))

		self.name_entry_tt.font = ('Bahnschrift Light', 10)
		self.grade_cbox_tt.font = ('Bahnschrift Light', 10)
		self.adviser_entry_tt.font = ('Bahnschrift Light', 10)
		self.edit_toggle_btn_tt.font = ('Bahnschrift Light', 10)
		self.teachers_list_tt.font = ('Bahnschrift Light', 10)
		self.add_teacher_btn_tt.font = ('Bahnschrift Light', 10)
		self.remove_teacher_btn_tt.font = ('Bahnschrift Light', 10)
		self.open_teacher_btn_tt.font = ('Bahnschrift Light', 10)
		self.student_list_tt.font = ('Bahnschrift Light', 10)
		self.add_teacher_btn_tt.font = ('Bahnschrift Light', 10)
		self.remove_teacher_btn_tt.font = ('Bahnschrift Light', 10)
		self.open_teacher_btn_tt.font = ('Bahnschrift Light', 10)
		self.back_btn_tt.font = ('Bahnschrift Light', 10)
		
		self.upd_lists()
	
	def back(self, event=None) -> None:

		if self.edit:
			response = msgbox.askyesnocancel(constants.TITLE, 
				'Do you want to save the profile?')
			if response == True:
				self.edit = False
			elif response == False:
				pass
			elif response is None:
				return

		self.master.protocol('WM_DELETE_WINDOW', self.master.exit)

		self.master.pagemng.current_page = 'homepage'
		self.master.pagemng.previous_page = None

	def exit(self, event=None) -> None:
		if self.edit:
			response = msgbox.askyesnocancel(constants.TITLE, 
				'Do you want to save the profile?')
			if response == True:
				self.edit = False
			elif response == False:
				pass
			elif response is None:
				return

		self.master.exit()

	def lock(self) -> None:
		
		self.name_entry.config(state='disabled')
		self.grade_cbox.config(state='disabled')
		self.adviser_entry.config(state='disabled')
		self.add_teacher_btn.config(state='disabled')
		self.remove_teacher_btn.config(state='disabled')
		self.add_student_btn.config(state='disabled')
		self.remove_student_btn.config(state='disabled')

	def unlock(self) -> None:

		self.name_entry.config(state='normal')
		self.grade_cbox.config(state='normal')
		self.adviser_entry.config(state='normal')
		self.add_teacher_btn.config(state='normal')
		self.remove_teacher_btn.config(state='normal')
		self.add_student_btn.config(state='normal')
		self.remove_student_btn.config(state='normal')

	def save(self, event=None) -> bool:

		required = {
			'Name': misc.convert_blank(self.name_entry.get()),
			'Grade Level': misc.convert_blank(self.grade_cbox.get())
		}

		for key, info in required.items():
			if info is None:
				msgbox.showerror(constants.TITLE, f'{key} required.')
				return False

		adviser = misc.convert_blank(self.adviser_entry.get())
		self.adviser_path = None
		if adviser is not None:
			advisers = {adviser.name: adviser.path for adviser in \
				self.master.teacherloader.items}
			try:
				self.adviser_path: str = advisers[adviser]
			except KeyError:
				msgbox.showerror(constants.TITLE, f'Teacher \'{adviser}\' does not exist.')
				return

		self.upd_lists(event)

		try:
			self.active_section.path = os.path.join(constants.PATHS.SECTIONS.value,
					constants.FILENAME_FORMATS.SECTION.value.format(
						glvl=required['Grade Level'].replace(' ', ''),
						name=required['Name'].replace(' ', '')))
			self.active_section.grade = required['Grade Level']
			self.active_section.name = required['Name']
		except (AttributeError, OSError):
			self.active_section = data.Section(
				os.path.join(constants.PATHS.SECTIONS.value,
					constants.FILENAME_FORMATS.SECTION.value.format(
						glvl=required['Grade Level'].replace(' ', ''),
						name=required['Name'].replace(' ', ''))),
				required['Name'],
				required['Grade Level'])

		self.active_section.students = self.students
		self.active_section.teachers = self.teachers
			
		self.active_section.dump()

		return True

	def toggle_edit(self, event=None) -> None:
		self.edit = not self.edit

	def upd_lists(self, event=None) -> None:
		
		self.teachers_list.delete(0, 'end')
		self.teachers = [item for item in self.teachers if os.path.exists(item[1])]
		self.teachers_list.insert('end', *[item[0] for item in self.teachers])

		self.students_list.delete(0, 'end')
		self.students = [item for item in self.students if os.path.exists(item[1])]
		self.students_list.insert('end', *[item[0] for item in self.students])

	def add_student(self, event=None) -> None:
		pass

	def add_teacher(self, event=None) -> None:
		pass

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

#   From Erik Bethke from
#   https://stackoverflow.com/questions/3221966/how-do-i-display-tts-in-tkinter
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
			# wraplength when the tt is too high to be
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
