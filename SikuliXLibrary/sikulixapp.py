# MIT license

from .sikulixjclass import *


class SikuliXApp(SikuliXJClass):
    '''
        SikuliX Application class (App) methods
    '''
    @keyword
    def app_open(self, application):
        '''
        Open the specified application (e.g. notepad.exe). Check https://sikulix-2014.readthedocs.io/en/latest/appclass.html for more
        
        The string application must allow the system to locate the application in the system specific manner. 
        If this is not possible you might try the full path to an application executable.

        Optionally you might add parameters, that will be given to the application at time of open.
        
        There are 2 options:
            - put the application string in apostrophes and the rest following the second apostrophes will be taken as parameter string
            - put `` -- `` (space 2 hyphens! space) between the applications name or path (no apostrophes!) and the parameter string.

        | App Open | C:/Windows/System32/notepad.exe |
        | App Open | "C:/Windows/System32/notepad.exe"path_to_my_txt_file |
        | App Open | C:/Windows/System32/notepad.exe -- path_to_my_txt_file |
        '''
        SikuliXJClass.App.open(application)

    @keyword
    def app_focus(self, title):
        '''
        Switch the input focus to a running application, having a front-most window with a matching title.

        | App Focus | Notepad |
        '''
        SikuliXJClass.App.focus(title)

    @keyword
    def app_close(self, app):
        '''
        It closes the running application matching the given string.

        | App Close | Notepad |
        '''
        SikuliXJClass.App.close(app)
