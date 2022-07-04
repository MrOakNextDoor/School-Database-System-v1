#   Manages everything related to data

#   Libraries
import os
import pickle
from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict, List, Literal, Optional, Tuple, Type, Union

from PIL import ImageTk

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

class Section(DataLoader):
	def __init__(self, path: str, name: str, grade: str) -> None:
		super().__init__(path)

		self.name: str = name
		self.grade: str = grade
		self.adviser: str = None
		self.teachers: List[str] = []
		self.students: List[str] = []

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
	def __init__(self, path: str, pic: str, 
		fname: str, bday: date, address: str, 
		sex: Literal['male', 'female'], contact_no: str=None, 
		email: str=None, mname: str=None, 
		lname: str=None) -> None:

		super().__init__(path)
		
		self._lname: str = None
		self._fname: str = None
		self._mname: str = None
		
		self.pic: str = pic
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

	def get_full_name(self, fmt: str='{f} {m} {l}') -> str:
		"""Return the full name of the Person with a format.

		Args:
			fmt (str): The format to be used.
		"""
		return fmt.format(f=self.fname, m=self.mname, l=self.lname)

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
	def __init__(self, path: str, pic: str, 
		fname: str, bday: date, address: str, 
		sex: Literal['male', 'female'], lrn: str, 
		sy: Tuple[int, int], parents: List[str], 
		grade_lvl: str, section: str=None, 
		contact_no: str=None, email: str=None, 
		mname: str=None, lname: str=None) -> None:

		super().__init__(path, pic, fname, bday, 
		address, sex, contact_no, email, mname, 
		lname)

		self.parents: List[str] = parents
		self.grade_lvl: str = grade_lvl
		self.lrn: str = lrn
		self.sy: Tuple[int, int] = sy
		self.section: str = section

	def load(self) -> 'Student':

		d: Student = super().load()

		self.parents = d.parents
		self.grade_lvl = d.grade_lvl
		self.lrn = d.lrn
		self.sy = d.sy
		self.section = d.section

		return d

	def loads(self, s: bytes) -> 'Student':

		d: Student = super().loads(s)

		self.parents = d.parents
		self.grade_lvl = d.grade_lvl
		self.lrn = d.lrn
		self.sy = d.sy
		self.section = d.section

		return d

class Teacher(Person):
	def __init__(self, path: str, pic: str, 
		fname: str, bday: date, address: str, 
		sex: Literal['male', 'female'], 
		advisory_cls: str=None, sections: List[str]=None, contact_no: str=None, 
		email: str=None, mname: str=None, lname: str=None
		) -> None:

		super().__init__(path, pic, fname, bday, 
		address, sex, contact_no, email, mname, 
		lname)
		
		self.advisory_cls: str = advisory_cls
		self.sections: List[str] = sections

	def load(self) -> 'Teacher':
		
		d: Teacher = super().load()

		self.advisory_cls = d.advisory_cls
		self.sections = d.sections

		return d

	def loads(self, s: bytes) -> 'Teacher':
		
		d: Teacher = super().loads(s)

		self.advisory_cls = d.advisory_cls
		self.sections = d.sections

		return d

class PathLoader(ABC):
	def __init__(self, path: str) -> None:
		self.path: str = path
		self.items: List[Type['DataLoader']] = []

	def get_all(self) -> List[str]:
		return [f for f in os.listdir(self.path) if f.endswith('.pkl')]

	@abstractmethod
	def load(self) -> None:
		self.items.clear()
		for path in self.get_all():
			self.items.append(DataLoader.construct(os.path.join(self.path, path)))

class SectionLoader(PathLoader):
	def load(self) -> None:
		self.items.clear()
		for path in self.get_all():
			self.items.append(Section.construct(os.path.join(self.path, path)))

class StudentLoader(PathLoader):
	def load(self) -> None:
		self.items.clear()
		for path in self.get_all():
			self.items.append(Student.construct(os.path.join(self.path, path)))

class TeacherLoader(PathLoader):
	def load(self) -> None:
		self.items.clear()
		for path in self.get_all():
			self.items.append(Teacher.construct(os.path.join(self.path, path)))

def search(profiles: List[Union[Person, Section]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
	
	results = []

	for p in profiles:
		profile = {key: value for key, value in p.__dict__.items() if not key.startswith('_')}
		profile['type'] = type(p).__name__

		try:
			profile['name'] = p.get_full_name()
			profile.pop('fname')
			profile.pop('mname')
			profile.pop('lname')
		except AttributeError:
			pass

		try:
			checks = []

			for key, value in filters.items():
				if isinstance(profile[key], str):
					checks.append(profile[key] in value)
				else:
					checks.append(profile[key] == value)
			
			if all(checks):
				results.append(p)

		except KeyError:
			continue

	return results
