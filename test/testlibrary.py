# Python test case to demonstrate SikuliX library keywords usage with Python


from SikuliXLibrary import *
import time
import os


if __name__ == "__main__":
    # local path for image files. Images below have iNotepad prefix so that to differentiate from text Notepad
    img_path = './img'
    if not os.path.exists(img_path):
        print ("Wrong image path")
        sys.exit()
        
    # local path for sikulix.jar, or empty if SIKULI_HOME environment variable should be used
    sikuli_path = ''
    #if not os.path.exists(sikuli_path):
    #    print ("Wrong sikuli path")
    #    sys.exit()

    lib = SikuliXLibrary(sikuli_path, img_path, logImages=False)

    lib.set_sikuli_resultDir('.')
    lib.region_setAutoWait(5)
    # coordinates relative to upper left corner
    lib.set_offsetCenterMode(False)
    
    # for demo purpose
    lib.settings_setShowActions(True)
    lib.settings_set('Highlight', True)
    prev = lib.settings_set('WaitAfterHighlight', float(3.0))
    print (prev)
    
    # default min similarity
    lib.settings_set('MinSimilarity', float(0.9))
    
    print ('=======Step1: open Notepad')
    lib.app_open("C:\\Windows\\System32\\notepad.exe")
    lib.region_wait('iNotepad.PNG')
    
    # message is Notepad2 not found after removing path
    print ('=======Step2: iNotepad2 image should not be found')
    lib.imagePath_remove(img_path)
    lib.region_exists('iNotepad2.PNG')
    
    print ('=======Step3: iNotepad2 should be found after adding image path')
    lib.imagePath_add(img_path)
    lib.region_exists('iNotepad2')
    
    #sys.exit()
    
    lib.region_paste('Welcome to the all new SikuliX RF library')
    time.sleep(3)
    
    print ('=======Step4: delete all typed text')
    lib.region_type(text='A', modifier='SikuliXJClass.Key.CTRL')
    lib.region_type('SikuliXJClass.Key.DELETE')

    lib.region_paste('Welcome to the all new SikuliX RF library ', 'iNotepad=0.7', 14, 60)    
    lib.region_wait('iNotepad typed')
    lib.region_type('SikuliXJClass.Key.BACKSPACE')

    print ('=======Step5: get all region text by OCR')
    text = lib.region_text('iNotepad typed')
    print (text)

    print ('=======Step6: type new line and new text')
    lib.region_type('SikuliXJClass.Key.ENTER')
    lib.region_paste('Based on JPype Python module')
    
    print ('=======Step7: search and highlight Untitled text')
    found = lib.region_existsText('Untitled')
    print (found)
    lib.region_highlight(3)
    lib.region_highlightAllOff()
    
    print ('=======Step8: right click on iNotepad - will fail if SKIP is not used next')
    lib.region_setFindFailedResponse('SKIP')
    lib.region_rightClick('iNotepad', 48, 14)

    print ('=======Step9: use correct image for right click')
    lib.region_setFindFailedResponse('ABORT')
    lib.settings_set('MinSimilarity', float(0.7))
    lib.region_rightClick('iNotepad typed', 48, 14)

    # coordinates relative to upper left corner of the image
    lib.region_click('iNotepad menu', 54, 80)
    lib.app_focus('Notepad')
    
    lib.region_click('iNotepad typed', 50, 12)
    # use previous found region
    lib.region_rightClick(None, 0, 0, True)

    print ('=======Step10: same as step 9, with coordinates relative to center')
    # coordinates relative to center of the image
    lib.set_offsetCenterMode(True)
    lib.region_click('iNotepad menu', -10, 10)
    lib.app_focus('Notepad')

    print ('=======Step11: dragDrop Notepad')
    lib.set_offsetCenterMode(False)
    prev = lib.settings_set('DelayBeforeDrop', float(2.0))
    lib.region_dragDrop('iNotepad typed', 'iNotepad typed', 50, 12, 100, 12)
    
    print ('=======Step12: delete everything and close Notepad')
    lib.region_type(text='A', modifier='SikuliXJClass.Key.CTRL')
    lib.region_type('SikuliXJClass.Key.DELETE')
    
    lib.app_close('Notepad')
    print ("done")
    lib.destroy_vm()
