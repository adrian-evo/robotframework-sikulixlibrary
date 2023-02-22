# MIT license

from .sikulixjclass import *

class SikuliXSettings(SikuliXJClass):
    '''
        SikuliX Settings class
    '''
    @keyword
    def settings_set(self, variable, value):
        '''
        Set the value for any public Settings class variable, see http://doc.sikuli.org/globals.html. There are
        many documented and even more undocumented settings that you can manipulate to alter SikuliX' behavior.
        These settings include:
        
        | | Name | type | default | Usage |
        | *Behavior* |
        | | ThrowException | boolean | true | Throw FindFailed exception |
        | | WheelNatural | boolean | true | Setting to false reverses the wheel direction |
        | | checkMousePosition | boolean | true | Setting to false supresses error message in RobotDesktop |
        | | ActionLogs | boolean | true | Switched to show or hide the respective action message in the log file |
        | | InfoLogs | boolean | true | Switched to show or hide the respective info message type in the  file |
        | | DebugLogs | boolean | false | Switched to show or hide the respective debug message in the log file |
        | | ProfileLogs | boolean | false | - |
        | | TraceLogs | boolean | false | - |
        | | LogTime | boolean | false | - |
        | *Timing* |
        | | AutoWaitTimeout | float | 3.0 | Timeout for Range Wait operations in seconds |
        | | WaitScanRate | float | 3.0 | Specify the number of times actual search operations are performed per \
            second while waiting for a pattern to appear or vanish. |
        | | ObserveScanRate | float | 3.0 |  Specify the number of times actual search operations are performed per \
            second while waiting for a pattern to appear or vanish. |
        | | RepeatWaitTime | int | 1 | Seconds for visual to vanish after action |
        | | DelayBeforeMouseDown | double | 0.3 | Delay time for mouse interaction | 
        | | DelayAfterDrag | double | 0.3 | Specifies the waiting time after mouse down at the source location \
            as a decimal value (seconds). | 
        | | DelayBeforeDrag | double | -0.3 | Delay time for mouse interaction | 
        | | DelayBeforeDrop | double | 0.3 | Specifies the waiting time before mouse up at the target location \
            as a decimal value (seconds). | 
        | | TypeDelay | double | 0.0 | Delay time between two characters, must be < 1 second | 
        | | ClickDelay | double | 0.0 | Delay time between two mouse down and mouse up, must be < 1 second. \
            Note: ClickDelay is reset to 0.0 on every mouse click | 
        | | SlowMotionDelay | float | 2.0 | Control the duration of the visual effect (seconds). | 
        | | MoveMouseDelay | float | 0.5 | Control the time taken for mouse movement to a target location by \
            setting this value to a decimal value (default 0.5). The unit is seconds. Setting it to 0 will \
            switch off any animation (the mouse will “jump” to the target location). | 
        | *Show Actions* |
        | | ShowActions | boolean | false | Use `setShowActions` to change the value of this setting |
        | | Highlight | boolean | false | Highlight every match (show red rectangle around) |
        | | DefaultHighlightTime | float | 2.0 | Time in seconds to show highlighting rectangle |
        | | DefaultHighlightColor | String | "RED" | Color for highlighting rectangle |
        | | HighlightTransparent | boolean | false | - |
        | | WaitAfterHighlight | double | 0.3 | - |
        | *Image Recognition and OCR* |
        | | MinSimilarity | double | 0.7 | Similarity required for a positive match 0.0...1.0 | 
        | | InputFontMono | boolean | false | - |
        | | InputFontSize | int | 14 | - |
        | | OcrLanguageDefault | string | "eng" | OCR expected language |
        
         Example usage
        | ${prev} | Settings Set | MinSimilarity | ${0.9} |
        | Settings Set | Highlight | ${True} |
        '''
        if useJpype:
            target = SikuliXJClass.Settings.class_.getDeclaredField(variable)
        else:
            target = get_java_class(SikuliXJClass.Settings).getDeclaredField(variable)

        previous = target.get(None)
        variable_type = str(target.getGenericType())
        logger.trace('Setting {}({}) to {}'.format(variable, variable_type, value))
        if variable_type == 'int':
            target.set(None, JInt(value))
        elif variable_type == 'float':
            target.set(value, JFloat(value))
        elif variable_type == 'double':
            target.set(None, JDouble(value))
        elif variable_type == 'boolean':
            target.set(None, JBoolean(value))
        else:
            target.set(None, value)

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
        
        | ${val} | Settings IsShowAction |
        '''
        return SikuliXJClass.Settings.isShowActions()
