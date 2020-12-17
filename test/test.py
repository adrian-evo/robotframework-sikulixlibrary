# Sample test file from JPype project to test library functionality under any OS

import jpype
import jpype.imports

jpype.startJVM()
import java
import javax
from javax.swing import *

def createAndShowGUI():
    frame = JFrame("HelloWorldSwing")
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
    label = JLabel("Hello World")
    frame.getContentPane().add(label)
    frame.pack()
    frame.setVisible(True)

# Start an event loop thread to handling gui events
@jpype.JImplements(java.lang.Runnable)
class Launch:
    @jpype.JOverride
    def run(self):
        createAndShowGUI()
javax.swing.SwingUtilities.invokeLater(Launch())
