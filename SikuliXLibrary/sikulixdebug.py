# MIT license

from .sikulixjclass import *


class SikuliXDebug(SikuliXJClass):
    '''
        SikuliX Debug class
    '''
    @keyword
    def set_debug(self, value):
        '''
        Sets the debug level of the SikuliX core engine. This data is logged to the console (stdout).
        Default is 0, more output is generated using level 3. Higher values may give more output.
        
        Example
        | Set Debug | 3 |
        '''
        SikuliXJClass.Debug.setGlobalDebug(int(value))
        
