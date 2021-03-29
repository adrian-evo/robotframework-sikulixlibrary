# MIT license

import os, datetime, time, shutil, subprocess, logging
from os.path import relpath
from py4j.java_gateway import launch_gateway

# Check which Python Java bridge to use between JPype and PY4J. When SIKULI_Py4J environment variable is defined with value 1
# use Py4J, otherwise if not defined or has value 0, use JPype
useJpype = True
if os.getenv('SIKULI_PY4J') == '1':
    useJpype = False

if useJpype:
    import jpype
    import jpype.imports
    from jpype.types import *
else:
    from py4j.java_gateway import (
        JavaGateway, get_field, get_method, get_java_class)

from robot.api.deco import *
from robot.api import logger


class SikuliXJClass():
    '''
        Main class holding JPype JClasses or py4j gateway classes used by SikuliX library
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
    FindFailedResponse = None
    ImagePath = None
    Settings = None
    JavaGW = None
    Py4JProcess = None


    @not_keyword
    def __init__(self, sikuli_path=''):
        if not SikuliXJClass.Initialized:
            if useJpype:
                self._jvm_sikuli_init(sikuli_path)
            else:
                self._py4j_sikuli_init(sikuli_path)
            SikuliXJClass.Initialized = True

        print ('SikuliXJClass init')
        logging.getLogger("py4j").setLevel(logging.ERROR)


    @not_keyword
    def _handle_sikuli_path(self, sikuli_path):
        # Check type of sikuli_path: empty for path from SIKULI_HOME + sikulix.jar, not empty might be either jar name or full path
        if (sikuli_path == '') or not os.path.isabs(sikuli_path):
            sikuli_home = os.getenv('SIKULI_HOME')
            if not sikuli_home:
                raise Exception("SIKULI_HOME environment variable not defined or full SikuliX path is missing.")
            if (sikuli_path == ''):
                sikuli_path = os.path.join(sikuli_home, 'sikulix.jar')
            else:
                sikuli_path = os.path.join(sikuli_home, sikuli_path)

        if not os.path.isfile(sikuli_path):
            raise Exception("SikuliX jar file is missing.")
        print('Use SikuliX file: ', sikuli_path)
        
        return sikuli_path

    @not_keyword
    def _jvm_sikuli_init(self, sikuli_path):
        print('JPype init')
        sikuli_path = self._handle_sikuli_path(sikuli_path)
        # Launch the JVM
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
        SikuliXJClass.FindFailedResponse = JClass('org.sikuli.script.FindFailedResponse')
        SikuliXJClass.Settings = JClass('org.sikuli.basics.Settings')

    @not_keyword
    def _py4j_sikuli_init(self, sikuli_path):
        print ('Py4J init')
        sikuli_path = self._handle_sikuli_path(sikuli_path)
        
        # wait for gateway
        def wait_for_gateway(func, max_tries, sleep_time):
            for _ in range(0, max_tries):
                try:
                    f = func()
                    print(f)
                    return f
                except:
                    print('Gateway not ready. Waiting.')
                    time.sleep(sleep_time)
            raise Exception("Fail to start Py4J. SikuliX not running")

        # Launch the JVM
        SikuliXJClass.Py4JProcess = subprocess.Popen(['java', '-jar', sikuli_path, '-p'], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        JavaGW = JavaGW = JavaGateway()
        print(SikuliXJClass.Py4JProcess)
        SikuliXJClass.JavaGW = JavaGW
        wait_for_gateway(lambda : JavaGW.jvm.System.getProperty("java.runtime.name"), 20, 0.5)

        SikuliXJClass.ImagePath = JavaGW.jvm.org.sikuli.script.ImagePath
        SikuliXJClass.Screen = JavaGW.jvm.org.sikuli.script.Screen
        SikuliXJClass.Region = JavaGW.jvm.org.sikuli.script.Region
        SikuliXJClass.Pattern = JavaGW.jvm.org.sikuli.script.Pattern
        SikuliXJClass.Match = JavaGW.jvm.org.sikuli.script.Match
        
        SikuliXJClass.Key = JavaGW.jvm.org.sikuli.script.Key
        SikuliXJClass.KeyModifier = JavaGW.jvm.org.sikuli.script.KeyModifier
        SikuliXJClass.App = JavaGW.jvm.org.sikuli.script.App
        SikuliXJClass.FindFailed = JavaGW.jvm.org.sikuli.script.FindFailed
        SikuliXJClass.FindFailedResponse = JavaGW.jvm.org.sikuli.script.FindFailedResponse
        SikuliXJClass.Settings = JavaGW.jvm.org.sikuli.basics.Settings
        
    @keyword
    def destroy_vm(self):
        '''
            Shutdown the Java Virtual Machine used by JPype or JavaGateway from py4j
        '''
        SikuliXJClass.Initialized = False
        if useJpype:
            jpype.shutdownJVM()
        else:
            SikuliXJClass.JavaGW.shutdown()
            SikuliXJClass.Py4JProcess.kill()
