from .sikulixjclass import useJpype, SikuliXJClass

if not useJpype:
    def JBoolean(x):
        return bool(x) 
    def JInt(x):
        return int(x)        
    def JFloat(x):
        return SikuliXJClass.JavaGW.jvm.java.lang.Double(float(x)).floatValue() 
    def JDouble(x):
        return float(x) 