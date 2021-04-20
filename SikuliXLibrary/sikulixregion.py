# MIT license

from .sikulixjclass import *
from .sikulixlogger import *


class SikuliXRegion(SikuliXJClass, SikuliXLogger):
    '''
        SikuliX Region class and all interactions with the region
    '''
    @not_keyword
    def __init__(self, logImages=True, centerMode=False):
        SikuliXLogger.__init__(self, logImages)

        self.appCoordinates = (0, 0, 1920, 1080)
        self.appScreen = SikuliXJClass.Screen()
        self.appRegion = SikuliXJClass.Region(*self.appCoordinates)
        self.appPattern = SikuliXJClass.Pattern()
        self.appMatch = SikuliXJClass.Match()
        
        self.offsetCenterMode = centerMode
        
        libLogger.debug('SikuliXRegion init')
        
    # Region - Set operations
    @keyword
    def set_offsetCenterMode(self, mode):
        '''
        Set to use click coordinates relative to center of the image (True) or relative to upper left corner (default False).
        
        With this approach, it is very easy to capture a screenshot, open it e.g. in Paint in Windows and the coordinates shown in lower left
        corner are the click coordinates that should be given to the mouse action keywords.
        
        | Set OffsetCenterMode | ${True} |
        '''
        self.offsetCenterMode = mode

    @keyword
    def region_setAutoWait(self, seconds):
        '''
        Set the maximum waiting time for all subsequent find operations in that Region.
        
        | Region SetAutoWait | ${5} |
        '''
        self.appRegion.setAutoWaitTimeout(float(seconds))

    @keyword
    def region_getAutoWait(self):
        '''
        Get the current value of the maximum waiting time for find operation in this region.
        
        | ${wait} | Region GetAutoWait |
        '''
        return self.appRegion.getAutoWaitTimeout()

    @keyword
    def region_setFindFailedResponse(self, val):
        '''
        Define the response if SikuliX cannot find the image.  
        
        Check https://sikulix-2014.readthedocs.io/en/latest/region.html for response options.
        - PROMPT will ask user for the next action
        - ABORT the execution of test
        - SKIP the step
        - RETRY to search again for image
        
        | Region SetFindFailedResponse | SKIP |
        '''
        if useJpype:
            jVal = SikuliXJClass.FindFailedResponse.class_.getDeclaredField(val).get(None)
        else:
            jVal = get_java_class(SikuliXJClass.FindFailedResponse).getDeclaredField(val).get(None)
        self.appRegion.setFindFailedResponse(jVal)

    @keyword
    def region_getFindFailedResponse(self):
        '''
        Return the response set if SikuliX cannot find the image.  
        
        | ${val} | Region SetFindFailedResponse |
        '''
        return self.appRegion.getFindFailedResponse()

    @keyword
    def region_setRect(self, x, y, w, h):
        '''
        Set position and dimension of the current region to new values. Upper left corner, width and height.
        
        Current region as full screen:
        | Region | SetRect | 0 | 0 | 1920 | 1080 | 
        '''
        self.appRegion.setRect(x, y, w, h)
        
    # Region - find operations
    @not_keyword
    def _prepare_pattern(self, target, dx=0, dy=0):
        # similarity given as img=similarity
        if "=" in target:
            text = target.split('=')
            pattern = SikuliXJClass.Pattern(text[0])
            pattern.similar(float(text[1]))
        else:
            pattern = SikuliXJClass.Pattern(target)

        # if dx and dy are not given, no target offset is given and click is center of image
        if dx == 0 and dy == 0:
            return pattern
        
        # calculate offset relative to upper left corner.
        if not self.offsetCenterMode:
            dx -= pattern.getImage().getW() / 2
            dy -= pattern.getImage().getH() / 2

        return pattern.targetOffset(int(dx), int(dy))

    @not_keyword
    def _prepare_lastMatch(self, dx, dy):
        # calculate offset relative to upper left corner.
        self.appMatch = self.appRegion.getLastMatch()

        # if dx and dy are not given, no target offset is given and click is center of image
        if dx == 0 and dy == 0:
            return
        
        if not self.offsetCenterMode:
            dx -= self.appMatch.getW() / 2
            dy -= self.appMatch.getH() / 2

        self.appMatch.setTargetOffset(int(dx), int(dy))

    @not_keyword
    def _region_findOperation(self, type, target, seconds=0, onScreen=True):
        if onScreen == True:
            self.appRegion.setRect(self.appScreen)

        self.appPattern = self._prepare_pattern(target)
        try:
            if seconds == 0:
                logger.trace("Call findOperation with arguments: %s" % type)
                logger.trace(self.appRegion)
                logger.trace(self.appPattern)
                if useJpype:
                    res = SikuliXJClass.Region.class_.getDeclaredMethod(type, JObject).invoke(self.appRegion, self.appPattern)
                else:
                    #print(self.appRegion)
                    #print(get_java_class(SikuliXJClass.Region))
                    #print(get_method(self.appRegion, type))
                    res = get_method(self.appRegion, type)(self.appPattern)
            else:
                logger.trace("Call findOperation with arguments: %s, %s seconds" % (type, seconds))
                logger.trace(self.appRegion)
                logger.trace(self.appPattern)
                if useJpype:
                    res = SikuliXJClass.Region.class_.getDeclaredMethod(type, JObject, JDouble).invoke(self.appRegion, self.appPattern, seconds)
                else:
                    res = get_method(self.appRegion, type)(self.appPattern, float(seconds))

        except: # except should happen only for find or wait
            self._failed("Image not visible on screen: " + target, seconds)
            raise Exception("_Find text method Failed")

        if res:
            if type == 'waitVanish':
                logger.info('PASS: ' + 'Image vanished from screen')
            else:
                self._passed("Image visible on screen")
        else:
            self._notfound("Image not visible on screen: " + target, seconds)

        return res
            
    @keyword
    def region_find(self, target, onScreen=True):
        '''
        Find a particular pattern, which is the given image. It searches within the region and returns the best match, 
        that shows a similarity greater than the minimum similarity given by the pattern. If no similarity was set for the pattern 
        by e.g. `Settings Set` before, a default minimum similarity of 0.7 is set automatically.

        From SikuliX documentation: Region.find(PS), where PS is a Pattern or String that define the path to an image file
        Pattern will need the following parameters, provided as arguments on this keyword
            - target - a string naming an image file from known image paths (with or without .png extension)
            - similar - minimum similarity. If not given, the default is used. Can be set as img=similarity
        - onScreen - reset the region to the whole screen, otherwise will search on a region defined previously with set parameters keywords
            e.g. `Region SetRect` where the parameters can be from a previous match or known dimensions, etc.
        
        Region Find does not wait for the appearance until timeout expires and throws FindFailed if not found.
            
        | Region Find | image.png=0.7 | 
        | Region Find | image | onScreen=${False} |
        
        '''
        return self._region_findOperation('find', target, 0, onScreen)

    @keyword
    def region_wait(self, target, seconds=0, onScreen=True):
        '''
        Wait until the particular pattern, which is the given image appears in the current region. See Region Find for more details.
        
        Region Wait repeat search until timeout expires and throws FindFailed if not found.
        
        seconds: granularity is milliseconds. If not specified, the auto wait timeout value set by `Region SetAutoWaitTimeout`  is used

        | Region Wait | image.png=0.7 | 10s |
        | Region Wait | image | onScreen=${False} |
        
        '''
        return self._region_findOperation('wait', target, seconds, onScreen)

    @keyword
    def region_waitVanish(self, target, seconds=0, onScreen=True):
        '''
        Wait until the particular pattern, which is the given image vanishes the current screen. See `Region Find` for more details.
        
        Region WaitVanish repeat search until timeout expires and does not throw exception.

        | Region WaitVanish | image | 10s |
        '''
        return self._region_findOperation('waitVanish', target, seconds, onScreen)

    @keyword
    def region_exists(self, target, seconds=0, onScreen=True):
        '''
        Wait until the particular pattern, which is the given image appears in the current region. See `Region Find` for more details.
        
        Region Exists repeat search until timeout expires but does not throws FindFailed if not found.
        
        seconds: granularity is milliseconds. If not specified, the auto wait timeout value set by `Region SetAutoWaitTimeout`  is used

        | Region Exists | image.png=0.7 | 10s |
        | Region Exists | image | onScreen=${False} |
        
        '''
        return self._region_findOperation('exists', target, seconds, onScreen)

    @keyword
    def region_has(self, target, seconds=0, onScreen=True):
        '''
        Similar with `Region Exists` as convenience wrapper intended to be used in logical expressions.
        '''
        return self._region_findOperation('has', target, seconds, onScreen)

    # Region - mouse actions
    @not_keyword
    def _region_mouseAction(self, action='click', target=None, dx=0, dy=0, useLastMatch=False):
        # 1st case, target none - click on default
        if target == None:
            logger.trace(self.appRegion)
            if useJpype:
                return SikuliXJClass.Region.class_.getDeclaredMethod(action).invoke(self.appRegion)
            else:
                return get_method(self.appRegion, action)()
            #return self.appRegion.click()

        # 2nd case, define a Pattern from image name - implicit find operation is processed first. 
        if not useLastMatch:
            pattern = self._prepare_pattern(target, dx, dy)
            self.appRegion.setRect(self.appScreen)
            logger.trace(self.appRegion)
            logger.trace(pattern)
            if useJpype:
                return SikuliXJClass.Region.class_.getDeclaredMethod(action, JObject).invoke(self.appRegion, pattern) 
            else:
                return get_method(self.appRegion, action)(pattern)

        # 3rd case, match can be given only as lastMatch. Target offset can be null or specified.
        if useLastMatch:
            self._prepare_lastMatch(dx, dy)
            logger.trace(self.appRegion)
            logger.trace(self.appMatch)
            if useJpype:
                return SikuliXJClass.Region.class_.getDeclaredMethod(action, JObject).invoke(self.appRegion, self.appMatch)
            else:
                return get_method(self.appRegion, action)(self.appMatch)

        # 4th case, region - not implemented
        # 5th case, location - not implemented

    @keyword
    def region_click(self, target=None, dx=0, dy=0, useLastMatch=False):
        '''
        Perform a mouse click on the click point using the left button.
        
        From SikuliX documentation: Region.click(PSMRL[, modifiers]), where PSMRL is a pattern, a string, a match, a region or a location that evaluates to a click point.

        Currently only String, together with parameters that define a pattern will be accepted.
        Pattern will need the following parameters, provided as arguments on this keyword
            - target - a string naming an image file from known image paths (with or without .png extension)
            - similar - minimum similarity. If not given, the default is used. Can be set as img=similarity
            - dx, dy - define click point, either relative to center or relative to upper left corner (default with `Set OffsetCenterMode`)
        - useLastMatch - if True, will assume the LastMatch can be used otherwise SikuliX will do a find on the target image and click in the center of it.
            if implicit find operation is needed, assume the region is the whole screen.
        
        Region Click with no arguments will either click the center of the last used Region or the lastMatch, if any is available.
        
        | Region Click | image.png=0.7 | dx | dy |
        | Region Click | image | dx | dy | useLastMatch=${True} |
        '''
        return self._region_mouseAction('click', target, dx, dy, useLastMatch)

    @keyword
    def region_doubleClick(self, target=None, dx=0, dy=0, useLastMatch=False):
        '''
        Perform a mouse double-click on the click point using the left button. See `Region Click` for details.

        | Region DoubleClick | image | dx | dy |
        '''
        return self._region_mouseAction('doubleClick', target, dx, dy, useLastMatch)

    @keyword
    def region_rightClick(self, target=None, dx=0, dy=0, useLastMatch=False):
        '''
        Perform a mouse click on the click point using the right button. See `Region Click` for details.

        | Region RightClick | image | dx | dy |
        '''
        return self._region_mouseAction('rightClick', target, dx, dy, useLastMatch)

    @keyword
    def region_hover(self, target=None, dx=0, dy=0, useLastMatch=False):
        '''
        Move the mouse cursor to hover above a click point defined by a target image and coordinates, i.e. to display a tooltip. See `Region Click` for details.

        | Region Hover | image | dx | dy |
        '''
        return self._region_mouseAction('hover', target, dx, dy, useLastMatch)

    @keyword
    def region_mouseMove(self, xoff, yoff):
        '''
        Move the mouse pointer from it’s current position to the position given by the offset values (<0 left, up >0 right, down)
        
        | Region MouseMove | x | y |
        '''
        return self.appScreen.mouseMove(xoff, yoff)
    
    # Region - highlights operations
    @keyword
    def region_highlight(self, seconds=0, useLastMatch=True):
        '''
        Highlight toggle (switched on if off and vice versa) for the current region (defined with `Region setRect`) or last match region. 
        
        For last match to be used, a last match operation needs to be performed first (e.g. find, wait, existsText and so on).
        
        | Region Highlight | 10 |
        '''
        if useLastMatch:
            self._prepare_lastMatch(0, 0)
            if self.appMatch == None:
                return 0
            logger.trace(self.appMatch)
            if seconds == 0:   
                return self.appMatch.highlight()
            else:
                return self.appMatch.highlight(float(seconds))
        else:
            logger.trace(self.appRegion)
            if seconds == 0:   
                return self.appRegion.highlight()
            else:
                return self.appRegion.highlight(float(seconds))

    @keyword
    def region_highlightAllOff(self):
        '''
        Switch off all currently active highlights.
        
        | Region HighlightAllOff |
        '''
        return self.appScreen.highlightAllOff()

    # Region - keyboard operations
    @keyword
    def region_paste(self, text, target=None, dx=0, dy=0):
        '''
        Paste the text at a click point defined by a target image and coordinates. See `Region Click` for more details.
        
        From SikuliX documentation: Region.click([PSMRL,] text), where PSMRL is a pattern, a string, a match, a region or a location that evaluates to a click point.
        
        Currently only String, together with parameters that define a pattern will be accepted.
        Pattern will need the following parameters, provided as arguments on this keyword
            - target - a string naming an image file from known image paths (with or without .png extension)
            - similar - minimum similarity. If not given, the default is used. Can be set as img=similarity
            - dx, dy - define click point, either relative to center or relative to upper left corner (default with `set offsetCenterMode`)
        
        If target is omitted, it performs the paste on the current focused component (normally an input field).
        
        | Region Paste | text | image.png=0.7 | dx | dy |
        | Region Paste | text | dx | dy |
        '''
        # 1st case, target none - click on default
        if target == None:
            return self.appScreen.paste(text)

        # 2nd case, define a Pattern from image name - implicit find operation is processed first. 
        pattern = self._prepare_pattern(target, dx, dy)
        self.appRegion.setRect(self.appScreen)
        return self.appRegion.paste(pattern, text)

    @keyword
    def region_type(self, text, target=None, dx=0, dy=0, modifier=None):
        '''
        Type the text at the current focused input field or at a click point specified by target image.
        
        From SikuliX documentation: Region.type([PSMRL,] text[, modifiers]), where PSMRL is a pattern, a string, a match, a region or a location that evaluates to a click point.
        
        Special keys (ENTER, TAB, BACKSPACE) can be incorporated into text using the constants defined in Class Key using the format SikuliXJClass.Key.Key_String
        e.g. SikuliXJClass.Key.ENTER for both key and modifier. Key modifiers can be ALT, CTRL, etc.
        
        Best Practice: As a general guideline, the best choice is to use `Region Paste` for readable text and 
        Region Type for action keys like TAB, ENTER, ESC. Use one Region Type for each key or key combination 
        and be aware, that in some cases a short wait after a type might be necessary to give the target application some time to react and be prepared for the next SikuliX action.

        | Region Type | text=A | modifier=SikuliXJClass.Key.CTRL |
        | Region Type | SikuliXJClass.Key.DELETE |

        '''
        key = text
        mod = None        

        if "SikuliXJClass.Key" in text:
            s_key = text.split(".")[2]
            try:
                #key = SikuliXJClass.Key.class_.getDeclaredField(s_key).get(None)
                key = SikuliXJClass.Key().getClass().getDeclaredField(s_key).get(None)
            except:
                key = s_key
        if modifier and "SikuliXJClass.Key" in modifier:
            s_key = modifier.split(".")[2]
            #mod = SikuliXJClass.Key.class_.getDeclaredField(s_key).get(None)
            mod = SikuliXJClass.Key().getClass().getDeclaredField(s_key).get(None)
        
        # 1st case, target none - click on default
        if target == None:
            if modifier == None:
                return self.appScreen.type(key)
            else:
                return self.appScreen.type(key, mod)

        # 2nd case, define a Pattern from image name - implicit find operation is processed first. 
        pattern = self._prepare_pattern(target, dx, dy)
        self.appRegion.setRect(self.appScreen)
        if modifier == None:
            return self.appRegion.type(pattern, key)
        else:
            return self.appRegion.type(pattern, key, mod)

    @keyword
    def region_dragDrop(self, target1, target2, dx1=0, dy1=0, dx2=0, dy2=0, useLastMatch=False):
        '''
        Perform a drag-and-drop operation from a starting click point to the target click point indicated by the two target images respectively.

        From SikuliX documentation: Region.dragDrop(PSMRL, PSMRL[, modifiers]), where PSMRL is a pattern, a string, a match, a region or a location that evaluates to a click point.
        
        Currently only String, together with parameters that define a pattern will be accepted.
        Pattern will need the following parameters, provided as arguments on this keyword
            - target - a string path to an image file
            - similar - minimum similarity. If not given, the default is used. Can be set as img=similarity
            - dx, dy - define click point, either relative to center or relative to upper left corner (default with Set OffsetCenterMode)
        - useLastMatch - if True, will assume the LastMatch can be used otherwise SikuliX will do a find on the target image and click in the center of it.
            
            if implicit find operation is needed, assume the region is the whole screen.
            
            target1 and target2 can be the same image with different click points or separate images
            
        | Region DragDrop | image1=0.7 | image2 | dx1 | dy1 | dx2 | dy2 |
        '''
        # define a Pattern from second image name - implicit find operation is processed first. 
        pattern2 = self._prepare_pattern(target2, dx2, dy2)
        logger.trace(pattern2)

        # match can be given only as lastMatch. Target offset can be null or specified.
        if useLastMatch:
            self._prepare_lastMatch(dx1, dy1)
            self.appRegion.setRect(self.appScreen)
            #return SikuliXJClass.Region.class_.getDeclaredMethod("dragDrop", JObject, JObject).invoke(self.appRegion, self.appMatch, pattern2)
            self.appRegion.dragDrop(self.appMatch, pattern2)
        # define a Pattern from first image name - implicit find operation is processed first. 
        if not useLastMatch:
            pattern1 = self._prepare_pattern(target1, dx1, dy1)
            logger.trace(pattern1)
            self.appRegion.setRect(self.appScreen)
            #return SikuliXJClass.Region.class_.getDeclaredMethod("dragDrop", JObject, JObject).invoke(self.appRegion, pattern1, pattern2) 
            self.appRegion.dragDrop(pattern1, pattern2)

    # Region - find text operations
    def _region_findTextOperation(self, type, text, seconds=0, onScreen=True):
        if onScreen == True:
            self.appRegion.setRect(self.appScreen)

        try:
            if seconds == 0:
                logger.trace("Call findTextOperation with arguments: %s" % type)
                logger.trace(self.appRegion)
                if useJpype:
                    res = SikuliXJClass.Region.class_.getDeclaredMethod(type, JString).invoke(self.appRegion, text)
                else:
                    res = get_method(self.appRegion, type)(text)
            else:
                logger.trace("Call findTextOperation with arguments: %s, %s seconds" % (type, seconds))
                logger.trace(self.appRegion)
                if useJpype:
                    res = SikuliXJClass.Region.class_.getDeclaredMethod(type, JString, JDouble).invoke(self.appRegion, text, seconds)
                else:
                    res = get_method(self.appRegion, type)(text, float(seconds))

        except: # except should happen only for find or wait
            self._failed("Text not visible on screen: " + text, seconds)
            raise Exception("_Find text method Failed")

        if res:
            if type == 'waitVanish':
                logger.info('PASS: ' + 'Text vanished from screen')
            else:
                self._passed("Text visible on screen")
        else:
            self._notfound("Text not visible on screen: " + text, seconds)

        return res

    @keyword
    def region_findText(self, text, onScreen=True):
        '''
        Search for given text on screen or within current region. Does not repeat search and throws FindFailed if not found.
        
        From SikuliX documentation: Region.findText(String), where text is the string to search for on screen. The autoWaitTimeout is used.
        onScreen - reset the region to the whole screen, otherwise will search on a region defined previously with set parameters keywords
            e.g. `Region SetRect` where the parameters can be from a previous match or known dimension, etc.
        
        Be aware other than the image search functions, the text search functions search from top left to bottom right. 
        So if there is more than one possible match in a region, always the top left match is found. With image search it 
        is still so, that it cannot be foreseen, which of the possible matches is returned as the result. In doubt you have 
        to use the functions, that return all matches in a region and then filter the result to your needs.
        
        | Region FindText | text |
        '''
        return self._region_findTextOperation('findText', text, 0, onScreen)

    @keyword
    def region_waitText(self, text, seconds=0, onScreen=True):
        '''
        Wait for the given text to appear on screen or current region. Repeat search and throws if not found during the given
        timeout in seconds or as autoWaitTimeout previously.
        
        | Region WaitText | text | ${10} |
        '''
        return self._region_findTextOperation('waitText', text, seconds, onScreen)

    @keyword
    def region_waitVanishText(self, text, seconds=0, onScreen=True):
        ''' 
        According to SikuliX documentation, not implemented yet.
        '''
        return self._region_findTextOperation('waitVanishText', text, seconds, onScreen)

    @keyword
    def region_existsText(self, text, seconds=0, onScreen=True):
        '''
        Wait for the given text to appear on screen or current region. Repeat search and does not throws error if not found during the given
        timeout in seconds or as autoWaitTimeout previously.
        
        | Region ExistsText | text | ${10} |
        '''
        return self._region_findTextOperation('existsText', text, seconds, onScreen)

    @keyword
    def region_hasText(self, text, seconds=0, onScreen=True):
        '''
        Search for given text on screen or within current region. Does not repeat search and does not throws FindFailed if not found.

        | Region HasText | text |
        '''
        return self._region_findTextOperation('hasText', text, seconds, onScreen)

    # Region - read text by OCR operations
    @keyword
    def region_text(self, img):
        '''
        Extract and return text from the given found image on screen (by using OCR)
        
        | Region Text | image.png |
        '''
        self.region_find(img)
        self.appMatch = self.appRegion.getLastMatch()
        text = self.appMatch.text()
        return str(text)
