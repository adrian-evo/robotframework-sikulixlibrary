# MIT license

from .sikulixjclass import *


class SikuliXSettings(SikuliXJClass):
    '''
        SikuliX Settings class
    '''
    @keyword
    def settings_set(self, variable, value):
        '''
        Set the value for any public Settings class variable. See http://doc.sikuli.org/globals.html for details and
        different variable names that can be set: MinSimilarity, Highlight, ActionLogs, MoveMouseDelay and so on.
 
        | ${prev} | Settings Set | MinSimilarity | ${0.9} |
        | Settings Set | Highlight | ${True} |
        '''
        if useJpype:
            previous = SikuliXJClass.Settings.class_.getDeclaredField(variable).get(None)
            SikuliXJClass.Settings.class_.getDeclaredField(variable).set(None, value)
        else:
            #previous = SikuliXJClass.Settings().getClass().getDeclaredField(variable).get(None)
            #SikuliXJClass.Settings().getClass().getDeclaredField(variable).set(None, value)

            previous = get_java_class(SikuliXJClass.Settings).getDeclaredField(variable).get(None)
            get_java_class(SikuliXJClass.Settings).getDeclaredField(variable).set(None, value)

        return previous

    @keyword
    def settings_get(self, variable):
        '''
        Return the value for any public Settings class variable. See http://doc.sikuli.org/globals.html for details and
        different variable names that can be set: MinSimilarity, Highlight, ActionLogs, MoveMouseDelay and so on.

        | ${val} | Settings Get | MinSimilarity |
        '''
        if useJpype:
            return SikuliXJClass.Settings.class_.getDeclaredField(variable).get(None)
        else:
            #return SikuliXJClass.Settings().getClass().getDeclaredField(variable).get(None)
            return get_java_class(SikuliXJClass.Settings).getDeclaredField(variable).get(None)

    @keyword
    def settings_setShowActions(self, mode):
        '''
        If set to True, when a script is run, SikuliX shows a visual effect (a blinking double lined red circle) 
        on the spot where the action will take place before executing actions. Default False
        
        | Settings SetShowAction | ${True} |
        '''
        SikuliXJClass.Settings.setShowActions(mode)

    @keyword
    def settings_isShowActions(self):
        '''
        Return show action mode
        
        | ${val} | Settings isShowAction |
        '''
        return SikuliXJClass.Settings.isShowActions()
