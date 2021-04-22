# Python test case to demonstrate SikuliX library keywords usage with Python


from SikuliXLibrary import SikuliXLibrary
import time, os, sys

if __name__ == "__main__":
    start_time = time.time()
    # local path for image files.
    img_path = os.getcwd() + '/img/Ubuntu'
    print(img_path)
    if not os.path.exists(img_path):
        print("Wrong image path")
        sys.exit()

    # sikuli_path: empty for path from SIKULI_HOME + sikulix.jar, not empty might be either SIKULI_HOME + given jar name or full path
    sikuli_path = 'sikulixide-2.0.5.jar'

    lib = SikuliXLibrary(sikuli_path, img_path, logImages=False)
    lib.log_java_bridge()

    lib.set_sikuli_resultDir('.')
    pre = lib.region_getAutoWait()
    lib.region_setAutoWait(5)
    print('Region AutWaitTimeout (3.0 -> 5.0): %s -> %s' % (pre, lib.region_getAutoWait()))
    # coordinates relative to upper left corner
    lib.set_offsetCenterMode(False)
    
    # for demo purpose
    pre = lib.settings_isShowActions()
    lib.settings_setShowActions(True)
    print('Settings ShowActions (False -> True): %s -> %s' % (pre, lib.settings_isShowActions()))

    pre = lib.settings_set('Highlight', True)
    print('Settings Highlight (False -> True): %s -> %s' % (pre, lib.settings_get('Highlight')))

    pre = lib.settings_set('WaitAfterHighlight', 0.5)
    print('Settings WaitAfterHighlight (0.3 -> 0.5): %s -> %s' % (pre, lib.settings_get('WaitAfterHighlight')))
    
    # default min similarity
    pre = lib.settings_set('MinSimilarity', float(0.9))
    print('Settings MinSimilarity (0.7 -> 0.9): %s -> %s' % (pre, lib.settings_get('MinSimilarity')))

    print('=======Step: open Leafpad')
    
    # TODO: Enable after https://github.com/RaiMan/SikuliX1/issues/438 is fixed
    #lib.app_open("leafpad")

    lib.region_wait('Leafpad')
    print('Wait with timeout: 1 second')
    lib.region_wait('Leafpad', 1)

    def exit_here():
        lib.app_close('Leafpad')
        print("done")
        lib.destroy_vm()
        print('Run time: %s seconds' % (time.time() - start_time))
        sys.exit()

    #exit_here()
        
    # message is Leafpad2 not found after removing path
    print('=======Step: Leafpad2 image should not be found')
    lib.imagePath_remove(img_path)
    res = lib.region_exists('Leafpad2')
    print('Exists (None): ', res)
    
    print('=======Step: Leafpad2 should be found after adding image path')
    lib.imagePath_add(img_path)
    res = lib.region_has('Leafpad2', 10)
    print('Exist - Has (True): ', res)
    
    #sys.exit()
    
    lib.region_paste('Welcome to the all new SikuliX RF library')
    time.sleep(3)

    print('=======Step: waitVanish - use SKIP to avoid exception')
    pre = lib.region_getFindFailedResponse()
    lib.region_setFindFailedResponse('SKIP')
    print('FindFailed (ABORT -> SKIP): %s -> %s' % (pre, lib.region_getFindFailedResponse()))
    res = lib.region_waitVanish('Leafpad typed', 5)
    print('Not vanished: ', res)
    pre = lib.region_getFindFailedResponse()
    lib.region_setFindFailedResponse('ABORT')
    print('FindFailed (SKIP -> ABORT): %s -> %s' % (pre, lib.region_getFindFailedResponse()))
    
    print('=======Step: delete all typed text')
    lib.region_type(text='A', modifier='SikuliXJClass.Key.CTRL')
    lib.region_type('SikuliXJClass.Key.DELETE')

    print('=======Step: waitVanish after delete')
    res = lib.region_waitVanish('Leafpad typed', 5)
    print('Vanished: ', res)

    lib.region_paste('Welcome to the all new SikuliX RF library ', 'Leafpad=0.7', 14, 60)    
    lib.region_wait('Leafpad typed', 10)
    lib.region_type('SikuliXJClass.Key.BACKSPACE')

    print('=======Step: get all region text by OCR')
    text = lib.region_text('Leafpad typed')
    print('OCR text: ', text)

    print('=======Step: type new line and new text')
    lib.region_type('SikuliXJClass.Key.ENTER')
    if os.getenv('SIKULI_PY4J') == '1':
        lib.region_paste('Based on Py4J Python module')
    else:
        lib.region_paste('Based on JPype Python module')
    
    print('=======Step: search and highlight Untitled text')
    found = lib.region_existsText('Untitled')
    print('Text found (Match): ', found)
    lib.region_highlight(3)
    lib.region_highlightAllOff()

    print ('=======Step: double click found text, by using last match')
    lib.region_doubleClick(useLastMatch=True)
    time.sleep(3)
    lib.region_waitText('Untitled', 5)
    lib.region_doubleClick(useLastMatch=True)
    
    print('=======Step: right click on Leafpad - will fail if SKIP is not used next')
    lib.region_setFindFailedResponse('SKIP')
    print('FindFailed (SKIP): ', lib.region_getFindFailedResponse())
    lib.region_rightClick('Leafpad', 48, 14)
    
    lib.region_setRect(1, 2, 500, 300)
    ret = lib.region_find('Leafpad', onScreen=False)
    print('Find on screen should fail: ', ret)

    print ('=======Step: use correct image for right click')
    lib.region_setFindFailedResponse('ABORT')
    print('FindFailed (ABORT): ', lib.region_getFindFailedResponse())
    
    pre = lib.settings_set('MinSimilarity', float(0.7))
    print('Settings MinSimilarity (0.9 -> 0.7): %s -> %s' % (pre, lib.settings_get('MinSimilarity')))

    res = lib.region_has('Leafpad typed=0.99')
    print('Has with 0.99 similiarity: (None)', res)
    
    #lib.region_rightClick('Leafpad typed', 48, 14)

    # coordinates relative to upper left corner of the image
    #lib.region_click('Leafpad menu', 54, 80)
    #lib.app_focus('Leafpad')
    
    #lib.region_click('Leafpad typed', 50, 12)
    # use previous found region
    #lib.region_rightClick(None, 0, 0, True)

    #print('=======Step: click with coordinates relative to center')
    # coordinates relative to center of the image
    #lib.set_offsetCenterMode(True)
    #lib.region_click('Leafpad menu', -10, 10)
    #lib.app_focus('Leafpad')

    #print('=======Step: dragDrop Leapfad')
    #lib.set_offsetCenterMode(False)
    #prev = lib.settings_set('DelayBeforeDrop', float(2.0))
    #lib.region_dragDrop('Leafpad typed', 'Leafpad typed', 50, 12, 100, 12)
    
    #print('=======Step: delete everything')
    #lib.region_type(text='A', modifier='SikuliXJClass.Key.CTRL')
    #lib.region_type('SikuliXJClass.Key.DELETE')
    
    print('=======Step: hover, click, double click')
    lib.region_hover('Leafpad typed', dx=10, dy=10)
    lib.region_mouseMove(100, 200)
    lib.region_doubleClick('Leafpad', 100, 300)
    
    exit_here()
