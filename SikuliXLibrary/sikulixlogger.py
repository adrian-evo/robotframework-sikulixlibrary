# MIT license

from .sikulixjclass import *
from os.path import relpath
import datetime, shutil


class SikuliXLogger():
    '''
        Class handling the logging of source images, matches and screenshots within robot log.html file
    '''
    resultDir: str = '.'

    @not_keyword
    def __init__(self, logImages=True):
        self.passedLogImages = False
        self.failedLogImages = False           
        self.notFoundLogImages = False

        if logImages:
            self.passedLogImages = True
            self.failedLogImages = True
            
        #libLogger.debug('SikuliXLogger init')

    @keyword
    def set_sikuli_resultDir(self, path):
        '''
        Used to set the directory where to save the screenshots for the log file

        | Set Sikuli ResultDir | path |
        '''
        SikuliXLogger.resultDir = path

    @keyword
    def set_passedLogImages(self, mode):
        '''
        Enable or disable logging of the images when keyword passes

        | Set PassedLogImages | ${True} |
        '''
        scr = self.passedLogImages
        self.passedLogImages = mode
        return scr
        
    @keyword
    def set_failedLogImages(self, mode):
        '''
        Enable or disable logging of the images when keyword fails

        | Set FailedLogImages | ${True} |
        '''
        scr = self.failedLogImages
        self.failedLogImages = mode
        return scr

    @keyword
    def set_notFoundLlogImages(self, mode):
        '''
        Enable or disable logging of the images when the image is not found (for keywords that does not throw exception)

        | Set NotFoundLogImages | ${True} |
        '''
        scr = self.notFoundLogImages
        self.notFoundLogImages = mode
        return scr

    @keyword
    def log_warning(self, msg):
        '''
        Print text in the log with the label WARNING:

        | Log Warning | msg |
        '''
        logger.warn("WARNING: %s" % msg)

    @not_keyword
    def _screenshot(self, folder="/screenshots/", region=None):
        # generate unique name for screenshot filename
        if region == None:
            br = SikuliXJClass.Screen().getBottomRight()
            region = (0, 0, br.x, br.y)
        
        name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f') + ".png"
        img_src = str(self.appScreen.capture(*region).getFile())
        full_folder = SikuliXLogger.resultDir + folder

        if img_src == None:
            return 'Screen capture failed (check resolution)'

        try:
            logger.trace("Screenshot: " + img_src)
            logger.trace("Matches: " + full_folder + name)
            shutil.copy(img_src, full_folder + name)
        except IOError:
            logger.error('FAIL: Capture screenshot path: ' + full_folder + name)

        return full_folder + name

    @not_keyword
    def _passed(self, msg, mode=None):
        libLogger.debug('PASS %s' % msg)
        logger.info('PASS: ' + msg)

        # matched image
        last_match: SikuliXJClass.Match = self.appRegion.getLastMatch()
        # score of match
        score: float = float(last_match.getScore())

        if self.passedLogImages:
            if mode == None:
                # source image
                src_img: str = str(self.appPattern.getFilename())
    
                # get relative path from result directory (log.html)
                rel_path = relpath(src_img, SikuliXLogger.resultDir)
                logger.debug('Source Image: <img src="%s" />' % rel_path, True)

            # screenshot of matched image
            region = (last_match.getX(), last_match.getY(), last_match.getW(), last_match.getH())
            name = self._screenshot("/matches/", region)
            rel_path = relpath(name, SikuliXLogger.resultDir)
            logger.debug('Best Match:   <img src="%s" />' % rel_path, True)
        
        logger.info("Matched with score: %s" % score)

    @not_keyword
    def _failed(self, msg, seconds, mode=None):
        libLogger.debug('FAIL %s' % msg)
        logger.error('FAIL: ' + msg)

        if self.failedLogImages:
            if mode == None:
                # source image
                src_img: str = str(self.appPattern.getFilename())
                rel_path = relpath(src_img, SikuliXLogger.resultDir)
                logger.info('Source Image: <img src="%s" />' % rel_path, True, True)
    
            # screenshot
            name = self._screenshot("/screenshots/")
            rel_path = relpath(name, SikuliXLogger.resultDir)
            logger.info('No Match: <img src="%s" />' % rel_path, True, True)

        if mode == None:        
            wait: float = float(self.appRegion.getAutoWaitTimeout())
            if seconds > 0:
                wait: float = seconds
            logger.debug('Image not visible after ' + str(wait) + ' seconds')
        raise Exception(msg)

    @not_keyword
    def _notfound(self, msg, seconds, mode=None):
        libLogger.debug('NOT FOUND %s' % msg)
        if self.notFoundLogImages:
            if mode == None:
                # source image
                src_img: str = str(self.appPattern.getFilename())
                rel_path = relpath(src_img, SikuliXLogger.resultDir)
                logger.info('Source Image: <img src="%s" />' % rel_path, True, True)
    
            # screenshot
            name = self._screenshot("/screenshots/")
            rel_path = relpath(name, SikuliXLogger.resultDir)
            logger.info('Not Found: <img src="%s" />' % rel_path, True, True)
        
        if mode == None:
            wait: float = float(self.appRegion.getAutoWaitTimeout())
            if seconds > 0:
                wait: float = seconds
            logger.debug('Image not visible after ' + str(wait) + ' seconds')
