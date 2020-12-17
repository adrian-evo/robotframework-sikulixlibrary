"""
Description: SikuliX sample custom library, based on the new, SikuliX JPype based library, implementing 
keywords from ImageHorizonLibrary for convenience migration.
Check https://eficode.github.io/robotframework-imagehorizonlibrary/doc/ImageHorizonLibrary.html for details
"""

import SikuliXLibrary
from SikuliXLibrary import *

from robot.api.deco import *
from robot.api import logger


@library(scope='GLOBAL', version='0.1')
class ImageHorizonLibraryMigration(SikuliXLibrary):

    @not_keyword
    def __init__(self, sikuli_path='', image_path='', logImages=True, centerMode=False):
        super().__init__(sikuli_path, image_path, logImages, centerMode)

    @keyword
    def click_image(self, target):
        # always click on center of the target image
        self.region_click(target, 0, 0, False)

    @keyword
    def set_confidence(self, new_confidence):
        self.settings_set('MinSimilarity', float(new_confidence))

    @keyword
    def wait_for(self, reference_image, timeout=10):
        return self.region_wait(reference_image, timeout, True)
