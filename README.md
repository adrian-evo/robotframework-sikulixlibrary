# robotframework-sikulixlibrary
The all new, modern, SikuliX Robot Framework library for Python 3.x, based on JPype or Py4J Python modules.

[JPype](https://github.com/jpype-project/jpype) is a Python module to provide full access to Java from within Python. 

[Py4J](https://github.com/bartdag/py4j) enables Python programs running in a Python interpreter to dynamically access Java objects in a JVM.

This library is a wrapper to SikuliX that is exposing Java functions as Robot Framework keywords, and it can be enabled to use by 
choice any of the JPype or Py4J modules. This is done by creating SIKULI_PY4J environment variable and setting to 1. When not defined or
set to 0, JPype is used instead. Please note that on MacOS, only Py4J can be used, while on Windows or Ubuntu, any of them is working.

While in the past the only approach to use Sikuli functionality within Robot Framework was through Remote Server with XML RPC interface, the aim 
of this library is to replace that approach and make it a lot easier to use SikuliX within Robot Framework projects with a simple Library statement 
(i.e. no need to start remote server and so on).

Also with this implementation is very easy to extend the library with new custom keywords, for example with the purpose to
create migration classes to help migrate from current Sikuli libraries or other image recognition alternatives. For practical examples check migrate folder.

See [keyword documentation](https://adrian-evo.github.io/SikuliXLibrary.html).

# Installation instructions (Windows)

1. Python 3.5 or newer, as supported by JPype or Py4J
2. JPype 1.2 or newer and JPype project dependencies as explained on project page: https://github.com/jpype-project/jpype
	- Install Java 8 or newer
	- While not mentioned on JPype page, on a new Windows 10 machine also Visual C++ Redistributable 2015 and newer are needed (e.g. vc_redist.x64.exe)
3. or Py4J 0.10.9.2 or newer
4. SikuliX as a standalone jar from project page: https://raiman.github.io/SikuliX1/downloads.html
	- Put jar file in any local directory (e.g. C:\sikulix\sikulix.jar)
	- Recommended to use environment variable SIKULI_HOME that point to sikulix local directory
5. `pip install robotframework-sikulixlibrary`

While JPype JVM is always started automatically, Py4J JVM can be started manually or automatically. To start manually, use the command:
	> java -jar sikulix.jar -p (to start Py4J server)
	> java -jar -DsikuliDebug=3 sikulixide.jar -p (useful e.g. for checking sikulix debug info)
	

# Examples

### Testing with [Robot Framework](https://robotframework.org)
```RobotFramework
*** Settings ***
Library   SikuliXLibrary	sikuli_path=sikulixide-2.0.5.jar

*** Test Cases ***
Example Test
    imagePath add   ${my_path}
    settings set  	MinSimilarity  ${0.9}
    app open        C:/Windows/System32/notepad.exe
    region wait     iNotepad.PNG
    region paste    Welcome!
```

### Testing with [Python](https://python.org).
```python
from SikuliXLibrary import SikuliXLibrary
lib = SikuliXLibrary()
lib.imagePath_add('my_path')
lib.settings_set('MinSimilarity', float(0.9))
lib.app_open("C:\\Windows\\System32\\notepad.exe")
lib.region_wait('iNotepad')
lib.region_paste('Welcome!)
```

# Testing
Git clone and execute runtest.bat to run all *.robot files from within test directory, or run individual robot files.

Additionally, debugging with Robot Editor - RED (https://github.com/nokia/RED) is also possible with this library, for both Robot Framework and Pyton code.

# Supported Operating Systems

1. Windows 10
	- supported, tested

2. OSX
	- SikuliX works under OSX, however currently there are issues with JPype generally working under OSX: https://github.com/jpype-project/jpype/issues/911

3. Linux
	- supported, tested with Ubuntu 20.04 and leafpad application
	- tested with: python3.8, default-jre (openjdk-11-jre), libopencv4.2-java as explained on SikuliX support page, gnome-panel, `pip install robotframework-sikulixlibrary`
	- obviously images from test/img directory needs to be regenerated for the application of choice, adjust SikuliX path in .robot file and use `app open  leafpad` instead.
	- start the tests with e.g. `python -m robot --outputdir results/ubuntu test_defaultlibrary.robot`
