# MIT license

from .version import __version__ as VERSION

from .sikulixregion import *
from .sikulixapp import *
from .sikuliximagepath import *
from .sikulixsettings import *


@library(scope='GLOBAL', version=VERSION)
class SikuliXLibrary(SikuliXRegion, 
                     SikuliXApp, 
                     SikuliXImagePath,
                     SikuliXSettings):
    
    ''' The all new, modern, SikuliX Robot Framework library for Python 3.x, based on JPype or Py4J Python modules.
    
    It can be enabled to use by choice any of the JPype or Py4J modules. This is done by creating SIKULI_PY4J environment variable 
    and setting to 1 for using Py4J. When not defined or set to 0, JPype is used instead. 
    Please note that on MacOS, only Py4J can be used, while on Windows or Ubuntu, any of them is working.
    
    So far, the only approach to use SikuliX Java library within Robot Framework was through Remote library and Jython 2.7.
    The existing ``robotframework-SikuliLibrary`` and other known custom implementations (e.g. mostly based on old 
    blog.mykhailo.com/2011/02/how-to-sikuli-and-robot-framework.html) are using Remote library approach only, which is now obsolete.
    
    In addition, also other popular libraries like ``ImageHorizonLibrary`` (built on top of pyautoguy), that is used currently due easier
    usage in comparison with previous SikuliX remote server implementations, can now be easily switched to this new library.
     
    With the help of this new library, SikuliX implementation can be used now natively with Robot Framework and Python 3.x:
    - robotremoteserver and Remote library are not needed anymore
    - debugging with Robot Editor - RED or Eclipse is finally possible for both Robot Framework and Python code
    
    - very easy to extend the library with new keywords, or overwrite existing keywords and methods by extending the main class, e.g.
    |    class ImageHorizonLibraryMigration(SikuliXLibrary):
    |        def click_image(self, reference_image):
    |            self.region_click(target, 0, 0, False)
    |            
    |    class SikuliLibraryMigration(SikuliXLibrary):
    |        def click(self, image, xOffset, yOffset):
    |            self.region_click(image, xOffset, yOffset, False)
    |
    |    class SikuliXCustomLibrary(SikuliXLibrary):
    |        def _passed(self, msg):
    |            logger.info('MY PASS MESSAGE: ' + msg)
    
    This library is using:
    |    [https://github.com/RaiMan/SikuliX1]
    |    [https://github.com/jpype-project/jpype]
    |    [https://github.com/bartdag/py4j]
    
    The keywords are matching as much as possible the original SikuliX functions so that it is easier to understand them from 
    the official documentation: https://sikulix-2014.readthedocs.io/en/latest/index.html
    E.g. SikuliX class Region.find(PS) function is translated into Python and Robot keyword as ``region_find(target, onScreen)``

        ``region_find = Region.find(PS)``, where PS is a Pattern or String that define the path to an image file
        
        Pattern will need the following parameters, provided as arguments to this keyword
            - target - a string naming an image file from known image paths (with or without .png extension)
            - similar - minimum similarity. If not given, the default is used. Can be set as ``img=similarity``
        - onScreen - reset the region to the whole screen, otherwise it will search on a region defined previously with set parameters keywords
            e.g. `Region SetRect` where the parameters can be from a previous match or known dimension, etc.
    
    Compared with other libraries, the import parameter ``centerMode`` will allow using click coordinates relative to center of the image,
    otherwise the click coordinates are relative to upper left corner (default).
    With this approach, it is very easy to capture a screenshot, open it e.g. in Paint in Windows and the coordinates shown in the lower left
    corner are the click coordinates that should be given to the click keyword:
     
        ``region_click = Region.click(PSMRL[, modifiers])``, where PSMRL is a pattern, a string, a match, a region or a location that evaluates to a click point.
        
        Currently only String, together with parameters that define a pattern will be accepted.
        Pattern will need the following parameters, provided as arguments to this keyword
            - target - a string naming an image file from known image paths (with or without .png extension)
            - similar - minimum similarity. If not given, the default is used. Can be set as img=similarity
            - dx, dy - define click point, either relative to center or relative to upper left corner (default with set_offsetCenterMode)
        - useLastMatch - if True, will assume the LastMatch can be used otherwise SikuliX will do a find on the target image and click in the center of it.
            
            if implicit find operation is needed, assume the region is the whole screen.
        
        Region Click with no arguments will either click the center of the last used Region or the lastMatch, if any is available.
    
    '''
    @not_keyword
    def __init__(self, sikuli_path='', image_path='', logImages=True, centerMode=False):
        '''
        | sikuli_path | Path to sikulix.jar file. If empty, it will try to use SIKULI_HOME environment variable. |
        | image_path |  Initial path to image library. More paths can be added later with the keyword `ImagePath Add` |
        | logImages | Default True, if screen captures of found images and whole screen if not found, are logged in the final result log.html file |
        | centerMode | Default False, if should calculate the click offset relative to center of the image or relative to upper left corner. |
        '''
        SikuliXJClass.__init__(self, sikuli_path)
        SikuliXImagePath.__init__(self, image_path)
        SikuliXRegion.__init__(self, logImages, centerMode)
