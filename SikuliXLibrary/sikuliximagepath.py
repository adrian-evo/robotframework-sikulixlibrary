# MIT license

from .sikulixjclass import *


class SikuliXImagePath(SikuliXJClass):
    '''
        SikuliX ImagePath class, handling the locations (paths) from where to load the reference images to search for
    '''
    @not_keyword
    def __init__(self, image_path=''):
        if image_path != '':
            SikuliXJClass.ImagePath.add(image_path)

        libLogger.debug('SikuliXImagePath init')
        
    @keyword
    def imagePath_add(self, path):
        '''
        Used usually in any suite setup. Will add to SikuliX ImagePath a new directory where to find reference images
        Note: paths must be specified using the correct path separators (slash on Mac and Unix and double blackslashes 
        on Windows). In Robot Framework you can use the `${/}` construct as universal separator.
        
        | ImagePath Add | path |
        '''
        SikuliXJClass.ImagePath.add(path)

    @keyword
    def imagePath_remove(self, path):
        '''
        Will remove from SikuliX ImagePath the given path

        | ImagePath Remove | path |
        '''
        SikuliXJClass.ImagePath.remove(path)
            
    @keyword
    def imagePath_reset(self):
        '''
        Will reset the SikuliX ImagePath and thereby remove all previous entries

        | ImagePath Reset | 
        '''
        SikuliXJClass.ImagePath.reset()
            
    @keyword
    def imagePath_dump(self):
        '''
        Retrieves the full list of image paths and logs these as trace messagesin the log file.
        '''
        imgPath = list(SikuliXJClass.ImagePath.getPaths())
        for p in imgPath:
            logger.trace("Image PATH: " + str(p))
