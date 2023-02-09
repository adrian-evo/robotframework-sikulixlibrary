# MIT license

from .sikulixjclass import *


class SikuliXDebug(SikuliXJClass):
    '''
        SikuliX Debug class
    '''
    @keyword
    def set_debug(self, variable, value):
        '''
        Sets the debug level of the SikuliX core engine. 
        Default is 0, more output is generated using level 3.
        
        Example
        | Set Debug | 3 |
        '''
        SikuliXJClass.Debug.setGlobalDebug(value)
        
