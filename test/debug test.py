#!python

"""
Description: Utility that will allow to debug and break into e.g. custom python libraries. Add a configuration within Visual Studio Code
    to run Python file and then execute this file. Set a breakpoint in the Python library as needed.
"""

from pathlib import Path

import robot

if __name__ == "__main__":
    robot.run('test/test_defaultlibrary_win.robot', outputdir='test/results/default')
