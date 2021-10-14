# MIT license

import os, time, subprocess, logging, sys
from py4j.java_gateway import GatewayParameters

# Check which Python Java bridge to use between JPype and Py4J. When SIKULI_PY4J environment variable is defined with value 1
# use Py4J, otherwise if not defined or has value 0, use JPype
useJpype = True
if os.getenv('SIKULI_PY4J') == '1':
    useJpype = False

# On MacOs always use Py4J, unless SIKULI_PY4J is set to 0 (e.g. for experiments)
if sys.platform.startswith('darwin'):
    useJpype = False

# Override MacOS Py4J forcing, e.g. for experiments
if os.getenv('SIKULI_PY4J') == '0':
    useJpype = True


if useJpype:
    import jpype
    import jpype.imports
    from jpype.types import *
else:
    from py4j.java_gateway import (
        JavaGateway, Py4JNetworkError, get_field, get_method, get_java_class)

from robot.api.deco import *
from robot.api import logger

libLogger = logging.getLogger(__name__)
libLogger.setLevel(level=logging.INFO)
logging.getLogger("py4j").setLevel(logging.ERROR)


class SikuliXJClass():
    '''
        Main class holding JPype JClasses or Py4J gateway classes used by SikuliX library
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
        self._init_python_console_logger()
        libLogger.debug('PY4J env variable: %s' % os.getenv('SIKULI_PY4J'))
        if not SikuliXJClass.Initialized:
            if useJpype:
                self._jvm_sikuli_init(sikuli_path)
            else:
                self._py4j_sikuli_init(sikuli_path)
            SikuliXJClass.Initialized = True

        libLogger.debug('SikuliXJClass init')

    @not_keyword
    def _init_python_console_logger(self):
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        libLogger.addHandler(consoleHandler)

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
            raise FileNotFoundError(sikuli_path)
        libLogger.debug('Use SikuliX file: %s' % sikuli_path)
        
        return sikuli_path

    @not_keyword
    def _jvm_sikuli_init(self, sikuli_path):
        libLogger.info('JPype init')
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
        libLogger.info('Py4J init')
        sikuli_path = self._handle_sikuli_path(sikuli_path)
        
        # wait for gateway
        def wait_for_gateway(func, max_tries, sleep_time):
            for _ in range(0, max_tries):
                try:
                    f = func()
                    print(f)
                    return f
                except:
                    libLogger.info('Gateway not ready. Waiting.')
                    time.sleep(sleep_time)
            raise Exception("Fail to start Py4J. SikuliX not running")

        # Check if already running
        manuallyStarted = False
        try:
            JavaGW = JavaGateway(gateway_parameters=GatewayParameters(eager_load=True))    
            libLogger.info("JVM accepting connection")
            manuallyStarted = True
        except Py4JNetworkError:
            libLogger.debug("No JVM listening")
        except Exception:
            libLogger.error("Other JVM exception")
        
        # Launch the JVM
        if not manuallyStarted:
            SikuliXJClass.Py4JProcess = subprocess.Popen(['java', '-jar', sikuli_path, '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            libLogger.info('JVM started: %s' % SikuliXJClass.Py4JProcess)
            JavaGW = JavaGateway()
            wait_for_gateway(lambda : JavaGW.jvm.System.getProperty("java.runtime.name"), 20, 0.5)
        
        SikuliXJClass.JavaGW = JavaGW

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
    def log_java_bridge(self):
        '''
            Log within Robot Framework which java bridge was used
        '''
        if not SikuliXJClass.JavaGW == None:
            if SikuliXJClass.Py4JProcess:
                logger.info('Using Py4J, started automatically')
            else:
                logger.info('Using Py4J, started manually')
        else:
            logger.info('Using JPype')
        
    @keyword
    def destroy_vm(self):
        '''
            Shutdown the Java Virtual Machine used by JPype or JavaGateway from Py4J
        '''
        SikuliXJClass.Initialized = False
        if useJpype:
            jpype.shutdownJVM()
        elif SikuliXJClass.Py4JProcess:
            SikuliXJClass.JavaGW.shutdown()
            SikuliXJClass.Py4JProcess.kill()
