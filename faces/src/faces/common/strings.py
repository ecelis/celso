"""
Strings for for Celso by @ecelis

   Copyright 2023 Ernesto A. Celis de la Fuente

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from enum import Enum

class FacesError(Enum):
    """Faces Error Strings"""
    GT_ONE_FACE = 'More than one face detected.'
    LT_ONE_FACE = "Couldn't detect any face."
    VALUE_ERROR = 'Value error'
    NO_MATCH = 'No matches'
