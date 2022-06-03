#   File to hold constants

#   Libraries
import os.path
from enum import Enum

#   Code
class DEFAULT_SETTINGS(Enum):
	EXPAND: bool = False
	RESTORE_LAST: bool = False
	TITLE: str = 'School Database System'

class PATHS(Enum):
	APPSTATE: str = os.path.join('data', 'appstate.pickle')
	SETTINGS: str = os.path.join('data', 'settings.pickle')

	SECTIONS: str = os.path.join('data', 'sections')
	STUDENTS: str = os.path.join('data', 'students')
	TEACHERS: str = os.path.join('data', 'teachers')

