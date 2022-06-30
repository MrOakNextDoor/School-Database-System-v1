#   File to hold constants

#   Libraries
import os.path
from enum import Enum
from PIL import Image

#   Code
class DEFAULT_SETTINGS(Enum):
	EXPAND: bool = False
	RESTORE_LAST: bool = False
	TITLE: str = 'School Database System'

class PATHS(Enum):
	APPSTATE: str = os.path.join('data', 'appstate.pkl')
	SETTINGS: str = os.path.join('data', 'settings.pkl')

	SECTIONS: str = os.path.join('data', 'sections')
	STUDENTS: str = os.path.join('data', 'students')
	TEACHERS: str = os.path.join('data', 'teachers')

class FILENAME_FORMATS(Enum):
	STUDENT: str = 'student_{lname}_{fname}_{mname}.pkl'
	TEACHER: str = 'teacher_{lname}_{fname}_{mname}.pkl'
	SECTION: str = 'section_{glvl}_{name}.pkl'

TITLE = 'School Database System'

SUPPORTED_IMG_TYPES = [[f'{f} File', ext] for ext
	, f in Image.registered_extensions().items() if f in Image.OPEN]
SUPPORTED_IMG_TYPES.insert(0, ['All Files', '*'])
GRADE_LVLS = ('Preparatory', 'Kinder I', 'Kinder II', 'Grade I', 'Grade II', 
	'Grade III', 'Grade IV', 'Grade V', 'Grade VI')
GENDERS = ('Male', 'Female')
