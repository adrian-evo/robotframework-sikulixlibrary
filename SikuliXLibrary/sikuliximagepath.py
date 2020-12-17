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

        #print('SikuliXImagePath init')
        
    @keyword
    def imagePath_add(self, path):
        '''
        Used usually in any suite setup. Will add to SikuliX ImagePath a new directory where to find reference images
        
        | ImagePath Add | path |
        '''
        SikuliXJClass.ImagePath.add(path)

        imgPath = list(SikuliXJClass.ImagePath.get())
        for p in imgPath:
            #print("Image PATH: " + str(p))
            logger.trace("Image PATH: " + str(p))

    @keyword
    def imagePath_remove(self, path):
        '''
        Will remove from SikuliX ImagePath the given path

        | ImagePath Remove | path |
        '''
        SikuliXJClass.ImagePath.remove(path)

        imgPath = list(SikuliXJClass.ImagePath.get())
        for p in imgPath:
            #print("Image PATH: " + str(p))
            logger.trace("Image PATH: " + str(p))
