#   Manages everything related to data

#   Libraries
import os
import pickle
from abc import ABC
from datetime import date
from PIL import ImageTk
from typing import Dict, List, Literal, Type, Optional, Tuple, Union

import constants

#	TODO:
#	- Do teacher advisory cls
#	- Do section advisor
#	- Do section path changing

#   Code
class DataLoader(ABC):
	def __init__(self, path: str) -> None:
		self._path = path

	@property
	def path(self) -> str:
		return self._path

	@path.setter
	def path(self, value: str) -> None:
		#   Prevents changing paths if given value is the same
		if self._path != value:
			os.remove(self._path)
			self._path = value
			#   Automatically transfers the information to the new path
			self.dump()
	
	@staticmethod
	def construct(path: str) -> Type['DataLoader']:
		"""Construct a DataLoader from a path.

		Args:
			path (str): The path to construct the DataLoader from.

		Returns:
			DataLoader: The loaded DataLoader.
		"""

		with open(path, 'rb') as f:
			return pickle.load(f, encoding='utf-8')

	@staticmethod
	def constructs(s: bytes) -> Type['DataLoader']:
		"""Construct a DataLoader from a byte string.

		Args:
			s (str): The byte string to construct the DataLoader from.

		Returns:
			DataLoader: The loaded DataLoader.
		"""

		return pickle.loads(s, encoding='utf-8')

	def load(self) -> Type['DataLoader']:
		"""Load the data from a path specified in __init__.

		Returns:
			DataLoader: The loaded DataLoader.
		"""

		try:
			with open(self.path, 'rb') as f:
				d: DataLoader = pickle.load(f, encoding='utf-8')
		except OSError:
			self.dump()
			d = self
		finally:
			return d

	def loads(self, s: bytes) -> Type['DataLoader']:
		"""Load the data from a string.

		Args:
			s (str): The string to load the data from.

		Returns:
			DataLoader: The loaded DataLoader.
		"""

		d: DataLoader = pickle.loads(s)
		return d

	def dump(self) -> None:
		"""Dump the data onto a file specified in __init__.
		"""

		with open(self.path, 'wb') as f:
			pickle.dump(self, f)

	def dumps(self) -> bytes:
		"""Dump the data onto a byte string.
		"""

		return pickle.dumps(self)

class AppState(DataLoader):
	def __init__(self) -> None:
		super().__init__(constants.PATHS.APPSTATE.value)
		
		self.current_page = None
		self.previous_page = None

	def load(self) -> 'AppState':

		d: AppState = super().load()

		self.current_page = d.current_page
		self.previous_page = d.previous_page

		return d

	def loads(self, s: bytes) -> 'AppState':

		d: AppState = super().loads(s)

		self.current_page = d.current_page
		self.previous_page = d.previous_page

		return d

class Settings(DataLoader):
	def __init__(self) -> None:
		super().__init__(os.path.join(constants.PATHS.SETTINGS.value))

		self.expand: bool = constants.DEFAULT_SETTINGS.EXPAND.value
		self.restore_last: bool = constants.DEFAULT_SETTINGS.RESTORE_LAST.value
		self.title: str = constants.DEFAULT_SETTINGS.TITLE.value

	def load(self) -> 'Settings':
		
		d: Settings = super().load()

		self.expand = d.expand
		self.restore_last = d.restore_last
		self.title = d.title

		return d

	def loads(self, s: bytes) -> 'Settings':

		d: Settings = super().loads(s)

		self.expand = d.expand
		self.restore_last = d.restore_last
		self.title = d.title

		return d

	def restore_defaults(self) -> None:
		self.restore_last: bool = constants.DEFAULT_SETTINGS.RESTORE_LAST.value
		self.title: str = constants.DEFAULT_SETTINGS.TITLE.value

class Section(DataLoader):
	def __init__(self, path: str, name: str, adviser: str) -> None:
		super().__init__(path)

		self.name: str = name
		self._adviser: str = adviser
		self.teachers: List[str] = []
		self.students: List[str] = []

	@property
	def path(self) -> str:
		return self._path
	
	@path.setter
	def path(self, value: str) -> None:
		#   Prevents changing paths if given value is the same
		if self._path != value:
			#	Deletes the old file from the old path
			os.remove(self._path)
			#	Sets the new path
			super().path = value
			#	Then letting all the students and teachers know 
			#	that the path has been changed

	def add(self, value: Union['Teacher', 'Student']) -> None:
		
		if isinstance(value, Teacher):
			if value.path not in self.teachers and not value.path == self.adviser.path:
				self.teachers.append(value.path)
		elif isinstance(value, Student):
			if value.path not in self.students:
				self.students.append(value.path)
		else:
			raise TypeError(f'Unsupported type: {type(value)}.')

	def remove(self, value: Union['Teacher', 'Student']) -> None:

		if isinstance(value, Teacher):
			self.teachers.remove(value.path)
		elif isinstance(value, Student):
			self.students.remove(value.path)
		else:
			raise TypeError(f'Unsupported type: {type(value)}.')

	def load(self) -> 'Section':

		d: Section = super().load()

		self.name = d.name
		self.adviser = d.adviser
		self.teachers = d.teachers
		self.students = d.students

		return d

	def loads(self, s: bytes) -> 'Section':

		d: Section = super().loads(s)

		self.name = d.name
		self.adviser = d.adviser
		self.teachers = d.teachers
		self.students = d.students

		return d

class Person(DataLoader):
	def __init__(self, path: str, pic: ImageTk.PhotoImage, 
		fname: str, bday: date, address: str, 
		sex: Literal['male', 'female'], contact_no: str=None, 
		email: str=None, mname: str=None, 
		lname: str=None) -> None:

		super().__init__(path)
		
		self._lname: str = None
		self._fname: str = None
		self._mname: str = None

		self.pic: ImageTk.PhotoImage = pic
		self.lname: str = lname
		self.fname: str = fname
		self.mname: str = mname
		self.bday: date = bday
		self.address: str = address
		self.sex: Literal['male', 'female'] = sex.lower()
		self.contact_no: str = contact_no
		self.email: str = email

	@property
	def lname(self) -> str:
		return self._lname

	@property
	def fname(self) -> str:
		return self.fname

	@property
	def mname(self) -> str:
		return self.mname

	@lname.setter
	def lname(self, value: Optional[str]) -> None:
		try:
			self._lname = value.title()
		except AttributeError:
			return

	@fname.setter
	def fname(self, value: Optional[str]) -> None:
		try:
			self._fname = value.title()
		except AttributeError:
			return

	@mname.setter
	def mname(self, value: Optional[str]) -> None:
		try:
			self._mname = value.title()
		except AttributeError:
			return

	def load(self) -> Type['Person']:
		
		d: Person = super().load()

		self.lname = d.lname
		self.fname = d.fname
		self.mname = d.mname
		self.bday = d.bday
		self.address = d.address
		self.sex = d.sex
		self.contact_no = d.contact_no
		self.email = d.email

		return d

	def loads(self, s: bytes) -> Type['Person']:

		d: Person = super().loads(s)

		self.lname = d.lname
		self.fname = d.fname
		self.mname = d.mname
		self.bday = d.bday
		self.address = d.address
		self.sex = d.sex
		self.contact_no = d.contact_no
		self.email = d.email

		return d

class Student(Person):
	def __init__(self, path: str, pic: ImageTk.PhotoImage, 
		fname: str, bday: date, address: str, 
		sex: Literal['male', 'female'],lrn: str, 
		sy: Tuple[int, int], contact_no: str=None, 
		email: str=None, mname: str=None, 
		lname: str=None) -> None:

		super().__init__(path, pic, fname, bday, 
		address, sex, contact_no, email, mname, 
		lname)

		self.lrn: str= lrn
		self.sy: Tuple[int, int] = sy

	def load(self) -> 'Student':

		d: Student = super().load()

		self.lrn = d.lrn
		self.sy = d.sy

		return d

	def loads(self, s: bytes) -> 'Student':

		d: Student = super().loads(s)

		self.lrn = d.lrn
		self.sy = d.sy

		return d

class Teacher(Person):
	def __init__(self, path: str, pic: ImageTk.PhotoImage, 
		fname: str, bday: date, address: str, 
		sex: Literal['male', 'female'], 
		advisory_cls: Section=None, contact_no: str=None, 
		email: str=None, mname: str=None, lname: str=None
		) -> None:

		super().__init__(path, pic, fname, bday, 
		address, sex, contact_no, email, mname, 
		lname)

		self._advisory_cls: str = None

		self.advisory_cls: str = advisory_cls

	@property
	def path(self) -> str:
		return self._path

	@property
	def advisory_cls(self) -> Section:
		pass

	@path.setter
	def path(self, value: str) -> None:
		super().path = value
		try:
			Section.construct(self.advisory_cls)
		except AttributeError:
			return

	@advisory_cls.setter
	def advisory_cls(self, value: str) -> None:
		pass