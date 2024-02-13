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

DEPO = Point(0, 0)
MAX_DISTANCE = 12*60

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
    def __init__(self, id:int, pickup:Point, dropoff:Point):
        self.id = int(id)
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

def greedy_vrp_v1(problem):
    """greedy_vrp_v1() picks the loads with the closest pickup points and does a round trip to the depo
    """
    drivers = []

    # Sorting loads by their distance from the depot
    sorted_loads = sorted(problem.loads, key=lambda load: distanceBetweenPoints(DEPO, load.pickup))

    # Start at zero
    current_driver_loads = []
    current_driver_distance = 0

    for load in sorted_loads:
        # Calculate the additional distance required to pick up and drop off the load round trip from the DEPO
        additional_distance = distanceBetweenPoints(DEPO, load.pickup) + \
                              distanceBetweenPoints(load.pickup, load.dropoff) + \
                              distanceBetweenPoints(load.dropoff, DEPO)
        
        # If adding this load exceeds the maximum distance for the current driver, start a new driver
        if current_driver_distance + additional_distance > MAX_DISTANCE:
            drivers.append(current_driver_loads)
            current_driver_loads = []
            current_driver_distance = 0
        
        # Add the load to the current driver's schedule
        current_driver_loads.append(load.id)
        
        # Update the current driver's total distance
        current_driver_distance += additional_distance
    
    # Add the remaining loads to the last driver
    if current_driver_loads:
        drivers.append(current_driver_loads)

    return drivers

def solveVRP(problem: VRP):
    """solveVRP() contains logic for VRP solution

    Parameters
    ----------
    problem : VRP
        the current problem being worked on from single inputFile
    """
    drivers = []
    useMySolution = True

    if useMySolution:
        drivers = greedy_vrp_v1(problem)
    else:
        # Test output succeeds for evaluateShared.py
        drivers = [[idx+1] for idx, load in enumerate(problem.loads)]

    for loads in drivers:
        print(loads)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Path to file containing current problem")
    args=parser.parse_args()
    problem = loadProblemFromFile(args.inputFile)
    solveVRP(problem)