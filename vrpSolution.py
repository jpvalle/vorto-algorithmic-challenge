import io
import math
import argparse

class Point:
    """
    Provided by evaluateShared.py
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

def distanceBetweenPoints(p1, p2):
    """
    Provided by evaluateShared.py
    """
    xDiff = p1.x - p2.x
    yDiff = p1.y - p2.y
    return math.sqrt(xDiff*xDiff + yDiff*yDiff)
    
class Load:
    """
    Provided by evaluateShared.py
    """
    def __init__(self, id, pickup, dropoff):
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        
class VRP:
    """
    Provided by evaluateShared.py
    """
    def __init__(self, loads):
        self.loads = loads
    def toProblemString(self):
        s = "loadNumber pickup dropoff\n"
        for idx, load in enumerate(self.loads):
            s += str(idx+1) + " " + load.pickup.toString() + " " + load.dropoff.toString() + "\n"
        return s
        
def loadProblemFromFile(filePath):
    """
    Provided by evaluateShared.py
    """
    f = open(filePath, "r")
    problemStr = f.read()
    f.close()
    return loadProblemFromProblemStr(problemStr)

def getPointFromPointStr(pointStr):
    """
    Provided by evaluateShared.py
    """
    pointStr = pointStr.replace("(","").replace(")","")
    splits = pointStr.split(",")
    return Point(float(splits[0]), float(splits[1]))

def loadProblemFromProblemStr(problemStr):
    """
    Provided by evaluateShared.py
    """
    loads = []
    buf = io.StringIO(problemStr)
    gotHeader = False
    while True:
        line = buf.readline()
        if not gotHeader:
            gotHeader = True
            continue
        if len(line) == 0:
            break
        line = line.replace("\n", "")
        splits = line.split()
        id = splits[0]
        pickup = getPointFromPointStr(splits[1])
        dropoff = getPointFromPointStr(splits[2])
        loads.append(Load(id, pickup, dropoff))
    return VRP(loads)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Path to file containing current problem")
    args=parser.parse_args()

    print(args.inputFile)
    problem = loadProblemFromFile(args.inputFile)
    print(problem.toProblemString())