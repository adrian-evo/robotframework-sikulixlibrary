"""
Description: SikuliX sample custom library, based on the new, SikuliX JPype or Py4J based library, implementing custom 
keywords (e.g. oneOfTheRegionsShouldExist) and/or override existing keywords for custom functionality (e.g. _passed).
"""


from SikuliXLibrary import SikuliXLibrary

from robot.api.deco import *
from robot.api import logger


@library(scope='GLOBAL', version='0.1')
class SikuliXCustomLibrary(SikuliXLibrary):

    @not_keyword
    def __init__(self, sikuli_path='', image_path='', logImages=True, centerMode=False):
        super().__init__(sikuli_path, image_path, logImages, centerMode)

    # Custom _passed method
    @not_keyword
    def _passed(self, msg):
        #logger.info('PASS: ' + msg)
        super()._passed(msg)

    # Custom _failed method
    @not_keyword
    def _failed(self, msg, seconds):
        #logger.info('FAILED: ' + msg)
        super()._failed(msg, 0)

    # Custom _notfound method
    @not_keyword
    def _notfound(self, msg, seconds):
        #logger.info('NOT FOUND: ' + msg)
        super()._notfound(msg, 0)

    # Sample custom keyword that will wait for the image to appear on screen and if not will try 
    # again a second search with a decreased similarity with 0.1 value (if repeat flag is set to true)
    @keyword
    def regionWaitRepeat(self, img, timeout=0, repeatFindWithLowerSimilar=False):
        '''
        Check the given image exists on screen, then try again with decreased similarity
        '''
        if not repeatFindWithLowerSimilar:
            found = self.region_wait(img, timeout)
        else:
            found = self.region_exists(img, timeout)
        if not found and repeatFindWithLowerSimilar:
            logger.warn('WARNING: Use decreased similiarity for a new search')
            # check the same image again by decreasing the minimum similarity
            minSimilar = self.settings_get('MinSimilarity')
            target = img + '=' + str(minSimilar - float(0.1))
            self.region_wait(target, timeout)

    # Sample custom keyword that will wait for first given image to appear on screen and if not will wait
    # for the second given image to appear on screen.
    @keyword
    def oneOfTheRegionsShouldExist(self, img1, img2, timeout=0):
        '''
        One of the two given images should be found on screen
        '''
        if not self.region_exists(img1, timeout):        
            logger.warn('WARNING: First image not found, wait for the second.')
            self.region_wait(img2, timeout)

    # Sample custom keyword that will simply rename the original SikuliXLibrary keyword for convenience
    # and easy of understanding the code
    @keyword
    def waitUntilScreenContains(self, target, timeout=0, onScreen=True):
        self.region_wait(target, timeout, onScreen)

    @keyword
    def waitUntilScreenDoesNotContain(self, target, timeout=0, onScreen=True):
        self.region_waitVanish(target, timeout, onScreen)
