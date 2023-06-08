from enum import Enum

class FacesError(Enum):
    """Faces Error Strings"""
    GT_ONE_FACE = 'More than one face detected.'
    LT_ONE_FACE = "Couldn't detect any face."