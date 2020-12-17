# MIT license

import jpype
import jpype.imports
from jpype.types import *

from robot.api.deco import *
from robot.api import logger

import os
import datetime
import shutil
from os.path import relpath


class SikuliXJClass():
    '''
        Main class holding JPype JClasses used by SikuliX library
    '''
    Initialized = False

    Screen = None
    Region = None
    Pattern = None
    Match = None
    Key = None
    KeyModifier = None
    App = None
    FindFailed = None
    ImagePath = None
    Settings = None


    @not_keyword
    def __init__(self, sikuli_path=''):
        if not SikuliXJClass.Initialized:
            self._jvm_sikuli_init(sikuli_path)
            SikuliXJClass.Initialized = True

        #print ('SikuliXJClass init')

    @not_keyword
    def _jvm_sikuli_init(self, sikuli_path):
        # Launch the JVM
        if (sikuli_path == ''):
            sikuli_home = os.getenv('SIKULI_HOME')
            if not sikuli_home:
                raise Exception("SIKULI_HOME not defined or SikuliX paths missing.")
            sikuli_path = os.path.join(sikuli_home, 'sikulix.jar')
        try:
            #java_path = jpype.getDefaultJVMPath()
            jpype.addClassPath(sikuli_path)
            jpype.startJVM()
            #jpype.startJVM(java_path, "-ea", "-Djava.class.path=%s" % sikuli_path)
        except:
            raise Exception("Fail to start JVM. Check Java and SikuliX paths.")
        
        if not jpype.isJVMStarted():
            raise Exception("Fail to start JVM. Check Java and SikuliX paths.")
        
        SikuliXJClass.ImagePath = JClass("org.sikuli.script.ImagePath")
        SikuliXJClass.Screen = JClass("org.sikuli.script.Screen")
        SikuliXJClass.Region = JClass("org.sikuli.script.Region")
        SikuliXJClass.Pattern = JClass('org.sikuli.script.Pattern')
        SikuliXJClass.Match = JClass('org.sikuli.script.Match')
        
        SikuliXJClass.Key = JClass('org.sikuli.script.Key')
        SikuliXJClass.KeyModifier = JClass('org.sikuli.script.KeyModifier')
        SikuliXJClass.App = JClass('org.sikuli.script.App')
        SikuliXJClass.FindFailed = JClass('org.sikuli.script.FindFailed')
        SikuliXJClass.Settings = JClass('org.sikuli.basics.Settings')
        
    @keyword
    def destroy_vm(self):
        '''
            Shutdown the Java Virtual Machine used by JPype
        '''
        SikuliXJClass.Initialized = False
        jpype.shutdownJVM()
