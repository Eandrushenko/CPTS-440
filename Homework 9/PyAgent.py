from random import randint
import Action
import Orientation


class WorldState:
    def __init__(self):
        self.agentlocation = [1, 1]
        self.agentOrientation = Orientation.RIGHT
        self.agentHasArrow = True
        self.agentHasGold = False
        self.goldlocation = [0, 0]
        self.worldSize = 5
        self.probabilities = {}
        self.known = {}
        self.breeze = {}
        self.frontier = []


class Agent:
    def __init__(self):
        self.worldState = WorldState()
        self.previousAction = Action.CLIMB
        self.actionStrList = []
        self.firstTry = True
        self.pathToGold = []
        self.potentialdanger = []
        self.vislocation = []
        self.safelocations = []
        self.stenchlocations = []
        self.clearlocations = []

    def Initialize(self):
        self.worldState.agentlocation = [1, 1]
        self.worldState.agentOrientation = Orientation.RIGHT
        self.worldState.agentHasArrow = True
        self.worldState.agentHasGold = False
        self.previousAction = Action.CLIMB
        self.actionStrList = []

        if (self.firstTry):
            self.worldState.worldSize = 5
            self.pathToGold.append([1, 1])
            self.worldState.frontier = [[1, 2], [2, 1]]
            self.worldState.known[(1, 1)] = False
            self.worldState.breeze[(1, 1)] = False
            self.Init_Probabilities()

        else:
            if (self.worldState.goldlocation == [0, 0]):
                self.pathToGold = []
                self.pathToGold.append([1, 1])
            else:
                self.AddActionsFromPath(True)

    def Process(self, percept):
        self.UpdateState(percept)
        if (not self.actionStrList):
            if (percept['Glitter']):
                self.actionStrList.append(Action.GRAB)
                self.AddActionsFromPath(False)
            elif (self.worldState.agentHasGold and (self.worldState.agentlocation == [1, 1])):
                self.actionStrList.append(Action.CLIMB)
            else:
                self.actionStrList.append(self.ChooseAction(percept))
        action = self.actionStrList.pop(0)
        self.previousAction = action

        print("Frontier: {0}".format(self.worldState.frontier))
        self.CalculateProb()

        self.showprobabilities()

        return action

    def CalculateProb(self):
        frontier = self.worldState.frontier
        breeze = self.worldState.breeze
        known = self.worldState.known
        location = self.worldState.agentlocation
        combinations = {}
        for location in frontier:
            C = 0
            trueprobability = 0.00
            falseprobability = 0.00
            temp = list(frontier)
            temp.remove(location)
            falselength = len(temp)
            print("Computing probPit({0}):".format(location))
            while C <= falselength:
                self.combinations(falselength, C, combinations, temp)
                T_calc = self.getcounts(combinations)
                F_calc = falselength - T_calc
                falseProbability = (0.2**T_calc) * (0.8**(F_calc))
                combinations[(location[0], location[1])] = True
                check = self.consists(breeze, combinations)
                if check == True:
                    trueprobability += falseProbability

                combinations[(location[0], location[1])] = False
                check = self.consists(breeze, combinations)
                if check == True:
                    falseprobability += falseProbability
                C += 1

            trueprobability *= 0.2
            falseprobability *= 0.8

            if falseprobability != 0 and trueprobability != 0:
                trueprobability = trueprobability / (trueprobability + falseprobability)

            print "\tFrontier: {0}".format(temp)
            print("\tProbability({0}) = {1}").format(location, trueprobability)

            if trueprobability == 0:
                known[(location[0], location[1])] = False

    def combinations(self, n, i, combinations, location):
        i = 0
        while i < n:
            xtemporary = location[i][0]
            ytemporary = location[i][1]
            if (i >> i) & 1:
                combinations[(xtemporary, ytemporary)] = True
            else:
                combinations[(xtemporary, ytemporary)] = False
            i += 1

    def getcounts(self, combinations):
        count = 0
        for C in combinations:
            if combinations.get(C) == True:
                count += 1
        return count


    def consists(self, B, combinations):
        Consistent = False
        worldSize = self.worldState.worldSize
        visit = self.vislocation        
        for location, y in B.items():
            location1 = (location[0], location[1] + 1)
            location2 = (location[0], location[1] - 1)
            location3 = (location[0] + 1, location[1])
            location4 = (location[0] - 1, location[1])
            
            
            if y == True:
                if (location[1] + 1) < worldSize:
                    if location1 in combinations:
                        if combinations.get(location1) == True:
                            Consistent = True
                if (location[1] - 1) >= 1:
                    if location2 in combinations:
                        if combinations.get(location2) == True:
                            Consistent = True
                if (location[0] + 1) < worldSize:
                    if location3 in combinations:
                        if combinations.get(location3) == True:
                            Consistent = True
                if (location[0] - 1) >= 1:
                    if location4 in combinations:
                        if combinations.get(location4) == True:
                            Consistent = True
            
        for location, x in combinations.items():
            location1 = (location[0], location[1] + 1)
            location2 = (location[0], location[1] - 1)
            location3 = (location[0] + 1, location[1])
            location4 = (location[0] - 1, location[1])
            
            if x == True:
                if (location[1] + 1) < worldSize and location1 in visit:
                    if location1 in B and B.get(location1) == True:
                        Consistent = True
                    else: return False
                if (location[1] - 1) >= 1 and location2 in visit:
                    if location1 in B and B.get(location1) == True:
                        Consistent = True
                    else: return False
                if (location[0] + 1) < worldSize and location3 in visit:
                    if location1 in B and B.get(location1) == True:
                        Consistent = True
                    else: return False
                if (location[0] - 1) >= 1 and location4 in visit:  
                    if location1 in B and B.get(location1) == True:
                        Consistent = True
                    else: return False
            else:
                if (location[1] + 1) < worldSize and location1 in visit:
                    if location1 in B and B.get(location1) == False:
                        Consistent = True
                    else: return False
                if (location[1] - 1) >= 1 and location2 in visit:
                    if location1 in B and B.get(location1) == False:
                        Consistent = True
                    else: return False
                if (location[0] + 1) < worldSize and location3 in visit:
                    if location1 in B and B.get(location1) == False:
                        Consistent = True
                    else: return False
                if (location[0] - 1) >= 1 and location4 in visit:  
                    if location1 in B and B.get(location1) == False:
                        Consistent = True
                    else: return False

        return Consistent

    def GameOver(self, score):
        self.firstTry = False

    def UpdateState(self, percept):
        currentOrientation = self.worldState.agentOrientation

        if (self.previousAction == Action.GOFORWARD):
            if (percept['Bump']):
                if (self.worldState.agentOrientation == Orientation.RIGHT):
                    self.worldState.worldSize = self.worldState.agentlocation[0]
                if (self.worldState.agentOrientation == Orientation.UP):
                    self.worldState.worldSize = self.worldState.agentlocation[1]
                if (self.worldState.worldSize > 0):
                    self.FilterSafelocations()
            else:
                self.worldState.agentlocation = self.GetGoForward()
                if (self.worldState.goldlocation == [0, 0]):
                    self.AddToPath(self.worldState.agentlocation)

        if (self.previousAction == Action.TURNLEFT):
            self.worldState.agentOrientation = (currentOrientation + 1) % 4

        if (self.previousAction == Action.TURNRIGHT):
            currentOrientation -= 1
            if (currentOrientation < 0):
                currentOrientation = 3
            self.worldState.agentOrientation = currentOrientation

        if (self.previousAction == Action.GRAB):
            self.worldState.agentHasGold = True 
            self.worldState.goldlocation = self.worldState.agentlocation

        if (self.previousAction == Action.SHOOT):
            self.worldState.agentHasArrow = False

            self.potentialdanger = []
            if (percept['Scream']):
                self.potentialdanger.append([2, 1])
            else:
                self.potentialdanger.append([1, 2])


        if self.worldState.agentlocation in self.worldState.frontier:
            self.worldState.frontier.remove(self.worldState.agentlocation)
        self.UpdateFrontier(self.safelocations, self.worldState.agentlocation)

        self.addnewlocation(self.vislocation,
                            self.worldState.agentlocation)
        self.addnewlocation(self.safelocations, self.worldState.agentlocation)
        if (percept['Stench']):
            self.addnewlocation(self.stenchlocations,
                                self.worldState.agentlocation)
        else:
            self.addnewlocation(self.clearlocations,
                                self.worldState.agentlocation)
            self.AddAdjacentlocations(
                self.safelocations, self.worldState.agentlocation)
        if (len(self.potentialdanger) != 1):
            self.Updatepotentialdanger()

        if percept['Breeze']:
            self.worldState.breeze[(
                self.worldState.agentlocation[0], self.worldState.agentlocation[1])] = True
        else:
            self.worldState.breeze[(
                self.worldState.agentlocation[0], self.worldState.agentlocation[1])] = False

        self.Output()

    def showprobabilities(self):
        print("")
        print("P(Pit):")
        x = 1
        y = 5
        while y > 0:
            print("\t"),
            while x < 5:
                print('{0:.2f}'.format(self.worldState.probabilities[(x, y)])),
                x += 1
            print("")
            x = 1
            y -= 1
        print("\n")

    def Updatepotentialdanger(self):
        self.potentialdanger = []
        for location1 in self.stenchlocations:
            adjacentlocations = []
            self.AddAdjacentlocations(adjacentlocations, location1)
            if (not self.potentialdanger):
                self.potentialdanger = adjacentlocations
            else:
                temporarylocation = self.potentialdanger
                self.potentialdanger = []
                for location2 in temporarylocation:
                    if (location2 in adjacentlocations):
                        self.potentialdanger.append(location2)
        for location1 in self.clearlocations:
            adjacentlocations = []
            self.AddAdjacentlocations(adjacentlocations, location1)
            temporarylocation = self.potentialdanger
            self.potentialdanger = []
            for location2 in temporarylocation:
                if (location2 not in adjacentlocations):
                    self.potentialdanger.append(location2)

    def GetGoForward(self):
        X = self.worldState.agentlocation[0]
        Y = self.worldState.agentlocation[1]
        if (self.worldState.agentOrientation == Orientation.RIGHT):
            X = X + 1
        if (self.worldState.agentOrientation == Orientation.UP):
            Y = Y + 1
        if (self.worldState.agentOrientation == Orientation.LEFT):
            X = X - 1
        if (self.worldState.agentOrientation == Orientation.DOWN):
            Y = Y - 1
        return [X, Y]

    def AddToPath(self, location):
        if (location in self.pathToGold):
            index = self.pathToGold.index(location)
            self.pathToGold = self.pathToGold[:index]
        self.pathToGold.append(location)

    def ChooseAction(self, percept):
        forwardlocation = self.GetGoForward()
        if (percept['Stench'] and (self.worldState.agentlocation == [1, 1]) and
                (len(self.potentialdanger) != 1)):
            action = Action.SHOOT
        elif ((forwardlocation in self.safelocations) and (forwardlocation not in self.vislocation)):
            action = Action.GOFORWARD
        else:
            if ((forwardlocation in self.potentialdanger) or
                    self.OutsideWorld(forwardlocation)):
                action = randint(1, 2)
            else:
                action = randint(0, 2)
        return action

    def AddActionsFromPath(self, forward):
        path = list(self.pathToGold)
        if (not forward):
            path = list(reversed(path))
        currentlocation = self.worldState.agentlocation
        currentOrientation = self.worldState.agentOrientation
        for nextlocation in path[1:]:
            if (nextlocation[0] > currentlocation[0]):
                nextOrientation = Orientation.RIGHT
            if (nextlocation[0] < currentlocation[0]):
                nextOrientation = Orientation.LEFT
            if (nextlocation[1] > currentlocation[1]):
                nextOrientation = Orientation.UP
            if (nextlocation[1] < currentlocation[1]):
                nextOrientation = Orientation.DOWN
            diff = (currentOrientation - nextOrientation)
            if ((diff == 1) or (diff == -3)):
                self.actionStrList.append(Action.TURNRIGHT)
            else:
                if (diff != 0):
                    self.actionStrList.append(Action.TURNLEFT)
                if ((diff == 2) or (diff == -2)):
                    self.actionStrList.append(Action.TURNLEFT)
            self.actionStrList.append(Action.GOFORWARD)
            currentlocation = nextlocation
            currentOrientation = nextOrientation

    def addnewlocation(self, locationList, location):
        if (location not in locationList):
            locationList.append(location)

    def AddAdjacentlocations(self, locationList, location):
        worldSize = self.worldState.worldSize
        if ((worldSize == 0) or (location[1] < worldSize)):
            self.addnewlocation(
                locationList, [location[0], location[1] + 1])  
        if ((worldSize == 0) or (location[0] < worldSize)):
            self.addnewlocation(
                locationList, [location[0] + 1, location[1]])  
        if (location[0] > 1):
            self.addnewlocation(
                locationList, [location[0] - 1, location[1]]) 
        if (location[1] > 1):
            self.addnewlocation(
                locationList, [location[0], location[1] - 1])  

    def UpdateFrontier(self, locationList, location):
        worldSize = self.worldState.worldSize
        if ((worldSize == 0) or (location[1] < worldSize)):
            if [location[0], location[1] + 1] not in self.worldState.frontier:
                self.worldState.frontier.append([location[0], location[1] + 1])
        if ((worldSize == 0) or (location[0] < worldSize)):
            if [location[0] + 1, location[1]] not in self.worldState.frontier:
                self.worldState.frontier.append(
                    [location[0] + 1, location[1]])  # right
        if (location[0] > 1):
            if [location[0] - 1, location[1]] not in self.worldState.frontier:
                self.worldState.frontier.append(
                    [location[0] - 1, location[1]])  # left
        if (location[1] > 1):
            if [location[0], location[1] - 1] not in self.worldState.frontier:
                self.worldState.frontier.append(
                    [location[0], location[1] - 1])  # down

        if [1, 1] in self.worldState.frontier:
            self.worldState.frontier.remove([1, 1])

    def OutsideWorld(self, location):
        worldSize = self.worldState.worldSize
        if ((location[0] < 1) or (location[0] < 1)):
            return True
        if ((worldSize > 0) and ((location[0] > worldSize) or (location[1] > worldSize))):
            return True
        return False

    def FilterSafelocations(self):
        worldSize = self.worldState.worldSize
        temporarylocation = list(self.safelocations)
        self.safelocations = []
        for location in temporarylocation:
            if ((location[0] < 1) or (location[1] < 1)):
                continue
            if ((worldSize > 0) and ((location[0] > worldSize) or (location[1] > worldSize))):
                continue
            self.safelocations.append(location)

    def Init_Probabilities(self):
        self.worldState.probabilities = {
            (1, 1): 0.00,
            (1, 2): 0.20,
            (1, 3): 0.20,
            (1, 4): 0.20,
            (1, 5): 0.20,
            (2, 1): 0.20,
            (2, 2): 0.20,
            (2, 3): 0.20,
            (2, 4): 0.20,
            (2, 5): 0.20,
            (3, 1): 0.20,
            (3, 2): 0.20,
            (3, 3): 0.20,
            (3, 4): 0.20,
            (3, 5): 0.20,
            (4, 1): 0.20,
            (4, 2): 0.20,
            (4, 3): 0.20,
            (4, 4): 0.20,
            (4, 5): 0.20,
            (5, 1): 0.20,
            (5, 2): 0.20,
            (5, 3): 0.20,
            (5, 4): 0.20,
            (5, 5): 0.20,
        }

    def Output(self):
        print("World Size: " + str(self.worldState.worldSize))
        print("visit locations: " + str(self.vislocation))
        print("Safe locations: " + str(self.safelocations))
        print("Potential Wumpus locations: " +
              str(self.potentialdanger))
        print("Gold location: " + str(self.worldState.goldlocation))
        print("Path To Gold: " + str(self.pathToGold))
        actionStrList = []
        for action in self.actionStrList:
            if action == Action.GOFORWARD:
                actionStrList.append('GOFORWARD')
            elif action == Action.TURNLEFT:
                actionStrList.append('TURNLEFT')
            elif action == Action.TURNRIGHT:
                actionStrList.append('TURNRIGHT')
            elif action == Action.GRAB:
                actionStrList.append('GRAB')
            elif action == Action.SHOOT:
                actionStrList.append('SHOOT')
            else:
                actionStrList.append('CLIMB')
        print("Action List: " + str(actionStrList))
        print("")


myAgent = 0


def PyAgent_Constructor():
    print "PyAgent_Constructor"
    global myAgent
    myAgent = Agent()


def PyAgent_Destructor():
    print "PyAgent_Destructor"


def PyAgent_Initialize():
    print "PyAgent_Initialize"
    global myAgent
    myAgent.Initialize()


def PyAgent_Process(stench, breeze, glitter, bump, scream):
    global myAgent
    percept = {'Stench': bool(stench), 'Breeze': bool(breeze), 'Glitter': bool(
        glitter), 'Bump': bool(bump), 'Scream': bool(scream)}
    return myAgent.Process(percept)


def PyAgent_GameOver(score):
    print "PyAgent_GameOver: score = " + str(score)
    myAgent.GameOver(score)
