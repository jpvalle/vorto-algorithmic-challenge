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

def greedy_vrp_v2(problem):
    """greedy_vrp_v2() picks the loads with the closest pickup points and decides between a round trip or another load
    """
    ERROR = 10 # Used to address the bug for now; Drivers go over by at most 10 minutes in two cases
    drivers = []

    # Sorting loads by their distance from the depot
    sorted_loads = sorted(problem.loads, key=lambda load: distanceBetweenPoints(DEPO, load.pickup))

    # Start at zero
    current_driver_loads = []
    current_driver_distance = 0
    current_driver_point = DEPO

    # Pop the first load from the sorted list
    pop_next = True
    next_load = None

    while sorted_loads:
        if pop_next:
            load = sorted_loads.pop(0)
        else:
            sorted_loads.remove(next_load)
            current_driver_point = load.dropoff
            load = next_load
            pop_next = True

        # Calculate the additional time required to pick up and drop off the load
        additional_distance = distanceBetweenPoints(current_driver_point, load.pickup) + \
                              distanceBetweenPoints(load.pickup, load.dropoff)
        distance_to_depo = distanceBetweenPoints(load.dropoff, DEPO)

        # If adding this load exceeds the maximum drive time for the current driver, start a new driver
        if current_driver_distance + additional_distance + distance_to_depo > MAX_DISTANCE:
            drivers.append(current_driver_loads)
            current_driver_loads = []
            current_driver_distance = 0
            current_driver_point = DEPO
        elif sorted_loads:
            # Decide on whether the driver could go to the next pickup instead
            next_loads = sorted(sorted_loads, key=lambda next_load: distanceBetweenPoints(load.dropoff, next_load.pickup))
            next_load = next_loads[0]
            additional_distance_next_load = additional_distance + \
                                            distanceBetweenPoints(load.dropoff, next_load.pickup) + \
                                            distanceBetweenPoints(next_load.pickup, next_load.dropoff) + \
                                            distanceBetweenPoints(next_load.dropoff, DEPO)
            if current_driver_distance + additional_distance_next_load + ERROR < MAX_DISTANCE:
                # Driver should take on the load in the next loop iteration
                pop_next = False

        # Add the load to the current driver's schedule
        current_driver_loads.append(load.id)

        # Update the current driver's total distance
        current_driver_distance += additional_distance
        if pop_next:
            current_driver_distance += distance_to_depo

    # Add the remaining loads to the last driver
    if current_driver_loads:
        drivers.append(current_driver_loads)

    return drivers

def driver_per_load_vrp(problem):
    """driver_per_load_vrp will assign one driver per load
    """
    return [[load.id] for load in problem.loads]

def solveVRP(problem: VRP):
    """solveVRP() contains logic for VRP solution

    Parameters
    ----------
    problem : VRP
        the current problem being worked on from single inputFile
    """
    drivers = greedy_vrp_v2(problem)

    for loads in drivers:
        print(loads)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Path to file containing current problem")
    args=parser.parse_args()
    problem = loadProblemFromFile(args.inputFile)
    solveVRP(problem)