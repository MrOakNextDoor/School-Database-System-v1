#   Manages everything related to data

#   Libraries
import os
import pickle
from abc import ABC
from datetime import date
from typing import Dict, List, Literal, Tuple, Type, Union

import constants


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
			with open(self.path, 'rb') as f:
				d: DataLoader = pickle.load(f, encoding='utf-8')
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
	def __init__(self, grade: int, name: str) -> None:
		super().__init__(os.path.join(constants.PATHS.SECTIONS, 
			f'G{grade}_{name.title().replace(" ", "")}'))
		
		self.adviser: str | Teacher = None
		self.grade: int = grade
		self.name: str = name.title().replace(' ', '')
		self.students: Dict[str, Student] = {}

	@property
	def path(self) -> str:
		return self._path

	@path.setter
	def path(self, value: str) -> None:
		super().path = value
		for student in self.students.values():
			self.students[student].section = self.path

	def load(self) -> 'Section':
		
		d: Section = super().load()

		self.adviser = d.adviser
		self.grade = d.grade
		self.name = d.name
		self.students = d.students
		
		return d

	def loads(self, s: bytes) -> 'Section':

		d: Section = super().loads(s)

		self.adviser = d.adviser
		self.grade = d.grade
		self.name = d.name
		self.students = d.students
		
		return d

	def add_student(self, student: 'Student', overwrite: bool=True) -> None:
		"""Add a Student to the Section.

		Args:
			student (Student): The student to be added.
			overwrite (bool, optional): Determines whether to overwrite an 
			existing student or not.
		"""
		
		if overwrite:
			student.grade = self.grade
			student.section = self.path
			self.students[student.path] = student
		else:
			if student.path in self.students:
				raise ValueError(
					'Student already in students. Consider setting overwrite to True.')
			else:
				student.grade = self.grade
				student.section = self.path
				self.students[student.path] = student

	def del_student(self, student: Union['Student', str]) -> None:

		try:
			if isinstance(student, str):
				self.students[student].section = None
				self.students.pop(student)
			elif isinstance(student, Student):
				self.students[student.path].section = None
				self.students.pop(student.path)
			else:
				raise TypeError(f'Unsupported type \'{type(student)}\'')
		except KeyError:
			raise KeyError('Student not in students.')

class Person(DataLoader):
	def __init__(self, path: str, fname: str, lname: str, address: str, 
		bday: date, sex: Literal['M', 'F'], contact_no: str=None, 
		email: str=None, mname: str=None) -> None:
		super().__init__(path)
		
		self.fname: str = fname.title()
		self._mname: str = mname.title() if mname is not None else None
		self.lname: str = lname.title()
		self.address: str = address
		self.bday: date = bday
		self.contact_no: str = contact_no
		self.email: str = email
		self.sex: Literal['M', 'F'] = sex.upper()

	@property
	def mname(self) -> str:
		return self._mname
	
	@mname.setter
	def mname(self, value: str) -> None:
		self._mname = value.title() if value is not None else None

	def load(self) -> Type['Person']:

		d: Person = super().load()

		self.fname = d.fname
		self.mname = d.mname
		self.lname = d.lname
		self.address = d.address
		self.bday = d.bday
		self.contact_no = d.contact_no
		self.email = d.email
		self.sex = d.sex
		
		return d

	def loads(self, s: bytes) -> Type['Person']:

		d: Person = pickle.loads(s, encoding='utf-8')

		self.fname = d.fname
		self.mname = d.mname
		self.lname = d.lname
		self.address = d.address
		self.bday = d.bday
		self.contact_no = d.contact_no
		self.email = d.email
		self.sex = d.sex

class Student(Person):
	def __init__(self, path: str, fname: str, lname: str, address: str, 
		bday: date, grade: str, sex: Literal['M', 'F'], lrn: str, 
		sy: Tuple[int, int], contact_no: str=None, email: str=None, 
		mname: str=None, section: str=None, guardians: List[str]=None
		) -> None:
		super().__init__(path, fname, lname, address, bday, contact_no, sex, 
			email, mname)
		
		self.lrn: str = lrn
		self.grade: str = grade
		self.guardians: List[str] = guardians
		self.section: str = section
		self.sy: Tuple[int, int] = sy

	def load(self) -> 'Student':
		
		d: Student = super().load()

		self.grade = d.grade
		self.lrn = d.lrn
		self.guardians = d.guardians
		self.section = d.section
		self.sy = d.sy

		return d

	def loads(self, s: bytes) -> 'Student':
		
		d: Student = super().load(s)

		self.grade = d.grade
		self.lrn = d.lrn
		self.guardians = d.guardians
		self.section = d.section
		self.sy = d.sy

		return d

class Teacher(Person):
	def __init__(self, fname: str, lname: str, address: str, 
		bday: date, contact_no: str, sex: Literal['M', 'F'], email: str=None, 
		advisory_class: Section=None, mname: str=None) -> None:
		super().__init__(fname, lname, address, bday, contact_no, sex, email, 
			mname)

		self.advisory_class: Section = advisory_class

	def load(self) -> 'Teacher':

		d: Teacher = super().load()

		self.advisory_class = d.advisory_class

	def loads(self, s: bytes) -> 'Teacher':
		
		d: Teacher = super().loads(s)

		self.advisory_class = d.advisory_class
