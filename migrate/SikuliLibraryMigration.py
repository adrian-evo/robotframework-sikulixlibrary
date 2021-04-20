"""
Description: SikuliX sample custom library, based on the new SikuliX JPype or Py4J library, implementing 
keywords from SikuliLibrary (robotframework-sikulilibrary) for convenience migration.
Check http://rainmanwy.github.io/robotframework-SikuliLibrary/doc/SikuliLibrary.html for details
"""

from SikuliXLibrary import SikuliXLibrary

from robot.api.deco import *
from robot.api import logger


@library(scope='GLOBAL', version='0.1')
class SikuliLibraryMigration(SikuliXLibrary):

    @not_keyword
    def __init__(self, sikuli_path='', image_path='', logImages=True, centerMode=False):
        super().__init__(sikuli_path, image_path, logImages, centerMode)

    @keyword
    def add_image_path(self, path):
        self.imagePath_add(path)

    @keyword
    def click_(self, image, xOffset=0, yOffset=0):
        # this library is using offset center mode
        self.offsetCenterMode = True
        self.region_click(image, xOffset, yOffset, False)

    @keyword
    def exists(self, image, timeout=0):
        return self.region_exists(image, timeout, True)

    @keyword
    def get_text(self, img):
        return self.region_text(img)
    
    @keyword
    def wait_until_screen_contain(self, image, timeout):
        self.region_wait(image, timeout, True)

    @keyword
    def wait_until_screen_not_contain(self, image, timeout):
        self.region_waitVanish(image, timeout, True)
