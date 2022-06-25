#   Handles how the app looks

#   Libraries
import tkinter as tk
from PIL import ImageTk, Image
from abc import ABC, abstractmethod
from datetime import date
from tkcalendar import DateEntry
from tkinter import messagebox as msgbox
from tkinter import ttk
from typing import Any, Dict, Tuple

import data
import misc

#	TODO: Add the one-window birthday entry

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
		
		self.master.pagemng.pages['pfppage'] = StudentProfilePage(self.master)
		self.master.pagemng.current_page = 'pfppage'

	def teacher(self) -> None:

		self.master.pagemng.pages['pfppage'] = TeacherProfilePage(self.master)
		self.master.pagemng.current_page = 'pfppage'

	def section(self) -> None:
		
		pass
		
class ProfilePage(Page):
	MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 
		'August', 'September', 'October', 'November', 'December')
	GENDERS = ('Male', 'Female')
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		self._edit = True

		self.tabmng = ttk.Notebook(master=self)
		self.tabmng.pack(fill='both', expand=True)

		#	General Frame
		self.general_frm = tk.Frame(self)

		#	Profile Pic
		self.pfp_frm = tk.Frame(self.general_frm)
		self.img = ImageTk.PhotoImage(Image.open(r"E:\New Keonosis\Photos\General\keon_and_potatoes.jpg").resize((200, 200)))
		self.pfp_lbl = tk.Label(self.pfp_frm, image=self.img)
		self.pfp_lbl.pack(expand=True, fill='both')

		self.pfp_frm.pack(fill='x', padx=10, pady=2)

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
		self.bday_lbl = tk.Label(master=self.bday_frm, text='Birthday')
		self.bday_cbox = DateEntry(master=self.bday_frm, relief='groove', bd=2, state='readonly', 
			firstweekday='sunday')

		self.bday_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.bday_cbox.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

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
		self.gender_cbox = ttk.Combobox(master=self.gender_frm, state="readonly", values=self.GENDERS)

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
		self.btns_frm.pack()
		
		self.dynresize = DynamicResize(self.master)
		self.dynresize.add_child(self.lname_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.lname_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.fname_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.fname_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.mname_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.mname_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.address_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.address_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.bday_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.bday_cbox, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.contact_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.contact_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.email_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.email_entry, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.gender_lbl, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.gender_cbox, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.edit_toggle_btn, 'Bahnschrift Light', 14, 16, 6)
		self.dynresize.add_child(self.back_btn, 'Bahnschrift Light', 14, 16, 6)

		self.lname_entry_tooltip = Tooltip(self.lname_entry, text='Last Name')
		self.fname_entry_tooltip = Tooltip(self.fname_entry, text='First Name')
		self.mname_entry_tooltip = Tooltip(self.mname_entry, text='Full Middle Name, Optional')
		self.address_entry_tooltip = Tooltip(self.address_entry, text='Address')
		self.bday_entry_tooltip = Tooltip(self.bday_cbox, text='Birthday in MM/DD/YYYY format')
		self.contact_entry_tooltip = Tooltip(self.contact_entry, text='Contact Number, Optional')
		self.email_entry_tooltip = Tooltip(self.email_entry, text='Email Address, Optional')
		self.gender_cbox_tooltip = Tooltip(self.gender_cbox, text='Gender')
		self.edit_toggle_btn_tooltip = Tooltip(self.edit_toggle_btn, text='Save the Profile')
		self.back_btn_tooltip = Tooltip(self.back_btn, text='Go Back to Menu')

		#	Note: Call self.reload_page() on subclasses
		self.master.protocol('WM_DELETE_WINDOW', self.exit)
	
	@property
	def edit(self) -> bool:
		return self._edit

	@edit.setter
	def edit(self, value: bool) -> None:
		self._edit = value
		if self.edit:
			self.unlock()
		else:
			self.lock()
			self.save()

		self.reload_page()

	@staticmethod
	def from_profile(master: tk.Widget, profile: data.Person) -> 'ProfilePage':
		
		p = ProfilePage(master)
		p.edit = False

		return p
	
	def lock(self, event=None) -> None:
		"""Locks all of the widgets so they cannot be modified"""

		self.lname_entry.config(state='disabled')
		self.fname_entry.config(state='disabled')
		self.mname_entry.config(state='disabled')
		self.address_entry.config(state='disabled')
		self.bday_cbox.config(state='disabled')
		self.contact_entry.config(state='disabled')
		self.email_entry.config(state='disabled')
		self.gender_cbox.config(state='disabled')
		
	def back(self, event=None) -> None:

		if self.edit:
			response = msgbox.askyesnocancel(self.master.settings.title, 
				'Do you want to save the profile?')
			if response == True:
				self.edit = False
			elif response == False:
				pass
			elif response is None:
				return

		self.master.pagemng.current_page = 'homepage'
		self.master.pagemng.previous_page = None

	def unlock(self, event=None) -> None:
		"""Unlocks all of the widgets so they can be modified"""

		self.lname_entry.config(state='normal')
		self.fname_entry.config(state='normal')
		self.mname_entry.config(state='normal')
		self.address_entry.config(state='normal')
		self.bday_cbox.config(state='readonly')
		self.contact_entry.config(state='normal')
		self.email_entry.config(state='normal')
		self.gender_cbox.config(state='normal')

	def exit(self) -> None:
		if self.edit:
			response = msgbox.askyesnocancel(self.master.settings.title, 
				'Do you want to save the profile?')
			if response == True:
				self.edit = False
			elif response == False:
				pass
			elif response is None:
				return

		self.master.exit()

	def save(self) -> None:
		
		#	Do some saving of the info here
		pass

	def toggle_edit(self) -> None:
		self.edit = not self.edit

	def reload_page(self, event=None) -> None:
		
		self.lname_lbl.config(font=('Bahnschrift Light', 14))
		self.lname_entry.config(font=('Bahnschrift Light', 14))
		self.fname_lbl.config(font=('Bahnschrift Light', 14))
		self.fname_entry.config(font=('Bahnschrift Light', 14))
		self.mname_lbl.config(font=('Bahnschrift Light', 14))
		self.mname_entry.config(font=('Bahnschrift Light', 14))

		self.address_lbl.config(font=('Bahnschrift Light', 14))
		self.address_entry.config(font=('Bahnschrift Light', 14))

		self.bday_lbl.config(font=('Bahnschrift Light', 14))
		self.bday_cbox.config(font=('Bahnschrift Light', 14))

		self.contact_lbl.config(font=('Bahnschrift Light', 14))
		self.contact_entry.config(font=('Bahnschrift Light', 14))
		self.email_lbl.config(font=('Bahnschrift Light', 14))
		self.email_entry.config(font=('Bahnschrift Light', 14))

		self.gender_lbl.config(font=('Bahnschrift Light', 14))
		self.gender_cbox.config(font=('Bahnschrift Light', 14))

		self.edit_toggle_btn.config(font=('Bahnschrift Light', 14))
		self.back_btn.config(font=('Bahnschrift Light', 14))

		self.lname_entry_tooltip.font = ('Bahnschrift Light', 10)
		self.fname_entry_tooltip.font = ('Bahnschrift Light', 10)
		self.mname_entry_tooltip.font = ('Bahnschrift Light', 10)
		self.address_entry_tooltip.font = ('Bahnschrift Light', 10)
		self.bday_entry_tooltip.font = ('Bahnschrift Light', 10)
		self.contact_entry_tooltip.font = ('Bahnschrift Light', 10)
		self.email_entry_tooltip.font = ('Bahnschrift Light', 10)
		self.gender_cbox_tooltip.font = ('Bahnschrift Light', 10)
		self.edit_toggle_btn_tooltip.font = ('Bahnschrift Light', 10)
		self.back_btn_tooltip.font = ('Bahnschrift Light', 10)

		if self.edit:
			self.edit_toggle_btn.config(text='Save')
		else:
			self.edit_toggle_btn.config(text='Edit')
	
class StudentProfilePage(ProfilePage):
	GRADE_LVLS = ('Preparatory', 'Kinder I', 'Kinder II', 'Grade I', 'Grade II', 
		'Grade III', 'Grade IV', 'Grade V', 'Grade VI')
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		#	Parents in General Frame
		self.parents_frm = tk.Frame(master=self.general_frm)
		self.parents_lbl = tk.Label(master=self.parents_frm, text='Parents (Separate w/ Comma)')
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
		self.grade_cbox = ttk.Combobox(master=self.grade_frm, state="readonly", values=self.GRADE_LVLS)

		self.grade_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.grade_cbox.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.grade_frm.columnconfigure(1, weight=1)

		self.grade_frm.pack(fill='x', padx=10, pady=2)

		#	Section
		self.section_frm = tk.Frame(master=self.student_frm)
		self.section_lbl = tk.Label(master=self.section_frm, text='Section')
		self.section_entry = tk.Entry(master=self.section_frm, relief='groove', bd=2)

		self.section_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.section_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.section_frm.columnconfigure(1, weight=1)

		self.section_frm.pack(fill='x', padx=10, pady=2)
		
		self.student_frm.pack(expand=True, fill='both')

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

		self.parent_entry_tooltip = Tooltip(self.parents_entry, text='Parents, Separate w/ Comma, Optional')
		self.lrn_entry_tooltip = Tooltip(self.lrn_entry, text='Learner\'s Reference Number')
		self.grade_cbox_tooltip = Tooltip(self.grade_cbox, text='Grade Level')
		self.section_entry_tooltip = Tooltip(self.section_entry, text='Section / Class Name, Optional')

		self.reload_page()
	
	def lock(self, event=None) -> None:
		super().lock(event)

		self.parents_entry.config(state='disabled')
		self.lrn_entry.config(state='disabled')
		self.grade_cbox.config(state='disabled')
		self.section_entry.config(state='disabled')

	def unlock(self, event=None) -> None:

		super().unlock(event)

		self.parents_entry.config(state='normal')
		self.lrn_entry.config(state='normal')
		self.grade_cbox.config(state='readonly')
		self.section_entry.config(state='normal')

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
		
		self.parent_entry_tooltip.font = ('Bahnschrift Light', 10) 
		self.lrn_entry_tooltip.font = ('Bahnschrift Light', 10)
		self.grade_cbox_tooltip.font = ('Bahnschrift Light', 10)
		self.section_entry_tooltip.font = ('Bahnschrift Light', 10)

class TeacherProfilePage(ProfilePage):
	def __init__(self, master: tk.Widget) -> None:
		super().__init__(master=master)

		#	Teacher Frame
		self.teacher_frm = tk.Frame(master=self)

		#	Learners Reference Number
		self.advisorycls_frm = tk.Frame(master=self.teacher_frm)
		self.advisorycls_lbl = tk.Label(master=self.advisorycls_frm, text='Advisory Class')
		self.advisorycls_entry = tk.Entry(master=self.advisorycls_frm, relief='groove', bd=2)

		self.advisorycls_lbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky='nsew', padx=6, pady=2)
		self.advisorycls_entry.grid(column=1, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=6, pady=2)

		self.advisorycls_frm.columnconfigure(1, weight=1)

		self.advisorycls_frm.pack(fill='x', padx=10, pady=2)

		self.teacher_frm.pack(expand=True, fill='both')

		self.tabmng.add(self.teacher_frm, text='Teacher\'s Information')

		self.dynresize.add_child(self.advisorycls_entry, 'Bahnschrift Light', 14, 16, 6)

		self.advisorycls_entry_tooltip = Tooltip(self.advisorycls_entry, text='Advisory Class, Optional')

		self.reload_page()

	def lock(self, event=None) -> None:

		super().lock(event)

		self.advisorycls_entry.config(state='disabled')

	def unlock(self, event=None) -> None:
		
		super().unlock(event)

		self.advisorycls_entry.config(state='normal')

	def reload_page(self, event=None) -> None:

		super().reload_page(event)

		self.advisorycls_entry.config(font=('Bahnschrift Light', 14))

		self.advisorycls_entry_tooltip.font = ('Bahnschrift Light', 10)

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