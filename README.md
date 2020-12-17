# robotframework-sikulixlibrary
The all new, modern, SikuliX Robot Framework library for Python 3.x, based on JPype Python module.

[JPype](https://github.com/jpype-project/jpype) is a Python module to provide full access to Java from within Python, and this library is 
a wrapper to SikuliX that is exposing Java functions as Robot Framework keywords. While in the past the only approach to use Sikuli functionality 
within Robot Framework was through Remote Server with XML RPC interface, the aim of this library is to replace that approach and
make it a lot easier to use SikuliX within Robot Framework projects with a simple Library statement (i.e. no need to start remote server and so on).

Also with this implementation is very easy to extend the library with new custom keywords, for example with the purpose to
create migration classes to help migrate from current Sikuli libraries or other image recognition alternatives. For practical examples check migrate folder.

See [keyword documentation](https://adrian-evo.github.io/SikuliXLibrary.html).

# Installation instructions

1. Python 3.5 or newer, as supported by JPype
2. JPype 1.2 or newer and JPype project dependencies as explained on project page: https://github.com/jpype-project/jpype
	- Install Java 8 or newer
	- While not mentioned on JPype page, on a new Windows 10 machine also Visual C++ Redistributable 2015 and newer are needed (e.g. vc_redist.x64.exe)
3. SikuliX as a standalone jar from project page: https://raiman.github.io/SikuliX1/downloads.html
	- Put jar file in any local directory (e.g. C:\sikulix\sikulix.jar)
	- Recommended to use environment variable SIKULI_HOME that point to sikulix local directory
4. `pip install robotframework-sikulixlibrary`

# Examples

### Testing with [Robot Framework](https://robotframework.org)
```RobotFramework
*** Settings ***
Library   SikuliXLibrary

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
from SikuliXLibrary import *
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
	- SikuliX works under OSX, however currently there are issues with JPype generally working under OSX: https://github.com/jpype-project/jpype/issues/906

3. Linux
	- untested
