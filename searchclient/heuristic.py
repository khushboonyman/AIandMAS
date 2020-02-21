from abc import ABCMeta, abstractmethod
import sys


class Heuristic(metaclass=ABCMeta):
    Goals = {} #dictionary for goals
    numOfGoals = 0
    def __init__(self, initial_state: 'State'):
        # Here's a chance to pre-process the static parts of the level. x will always be the row and y will always be the column
        #create a dictionary of goals, where key is the goal letter and value is the list of row,column combination
        for x in range(1,initial_state.MAX_ROW-1) :   #dont need to read the walls, so range is 1 to MAX_ROW-1 same for column
            for y in range(1,initial_state.MAX_COL-1) :
                goalAtXY = initial_state.goals[x][y]
                if goalAtXY is not None and goalAtXY in "abcdefghijklmnopqrstuvwxyz":
                    Heuristic.numOfGoals+=1
                    if goalAtXY in Heuristic.Goals.keys() :
                        Heuristic.Goals[goalAtXY].append([x,y])
                    else :
                        Heuristic.Goals[goalAtXY] = [[x,y]]
                    
    def h(self, state: 'State') -> 'int':
        sumOfDistances=0            
        Boxes = {}  #dictionary of boxes
        numOfBoxes=0
        for x in range(1,state.MAX_ROW-1) : #here we are doing the same for boxes as we did for goals
            for y in range(1,state.MAX_COL-1) :
                boxAtXY = state.boxes[x][y]
                if boxAtXY is not None and boxAtXY in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    boxAtXY = boxAtXY.casefold() #convert to lower case, so it is easier to process later
                    numOfBoxes+=1
                    if boxAtXY in Boxes.keys() :
                        Boxes[boxAtXY].append([x,y])
                    else :
                        Boxes[boxAtXY] = [[x,y]]  
                         
        #find the distances between the closest box goal pairs 
        for letter in Boxes :
            AllBoxesToAllGoals = []
            agentToBoxes = []
            if letter in Heuristic.Goals :
                for boxXY in Boxes[letter] :
                    ABoxToAllGoals=[]
                    for goalXY in Heuristic.Goals[letter] :
                        ABoxToAllGoals.append(abs(boxXY[0]-goalXY[0])+abs(boxXY[1]-goalXY[1]))
                    agentToBoxes.append(boxXY)
                    AllBoxesToAllGoals.append(ABoxToAllGoals)
                    
                #process the matrix AllBoxesToAllGoals until we have found all minimum distances   
                for counter in range(numOfBoxes):
                    minDistPerBox = -1
                    BoxIndex = -1
                    GoalIndex = -1
                    for BoxIndexTemp,BoxToAllGoals in enumerate(AllBoxesToAllGoals) :
                        if len(BoxToAllGoals) > 0 :
                            minDistPerBoxTemp = min(BoxToAllGoals)
                            if minDistPerBox == -1 or minDistPerBoxTemp < minDistPerBox :
                                minDistPerBox = minDistPerBoxTemp
                                BoxIndex = BoxIndexTemp
                                GoalIndex = BoxToAllGoals.index(minDistPerBoxTemp)
                    
                    if BoxIndex != -1 :
                        #agent to box distance of the boxes that are closest to goal
                        agentXY = agentToBoxes.pop(BoxIndex)
                        if state.goals[agentXY[0]][agentXY[1]] is None or state.goals[agentXY[0]][agentXY[1]]!=state.boxes[agentXY[0]][agentXY[1]].casefold():
                            distance=abs(state.agent_col-agentXY[1])
                            sumOfDistances+=distance
                            if distance==0:
                                sumOfDistances+=1
                            if state.agent_col > agentXY[1]:
                                sumOfDistances+=2                              
                        AllBoxesToAllGoals.pop(BoxIndex)
                        #add box to goal distance to the heuristic
                        sumOfDistances+=minDistPerBox
                        for boxGoalPairs in AllBoxesToAllGoals :
                            boxGoalPairs.pop(GoalIndex)  #remove the goal that has been assigned to closest box, from rest of boxes
       
        
        return sumOfDistances
    
    @abstractmethod
    def f(self, state: 'State') -> 'int': pass
    
    @abstractmethod
    def __repr__(self): raise NotImplementedError


class AStar(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)
    
    def f(self, state: 'State') -> 'int':
        return state.g + self.h(state)
    
    def __repr__(self):
        return 'A* evaluation'


class WAStar(Heuristic):
    def __init__(self, initial_state: 'State', w: 'int'):
        super().__init__(initial_state)
        self.w = w
    
    def f(self, state: 'State') -> 'int':
        return state.g + self.w * self.h(state)
    
    def __repr__(self):
        return 'WA* ({}) evaluation'.format(self.w)


class Greedy(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)
    
    def f(self, state: 'State') -> 'int':
        return self.h(state)
    
    def __repr__(self):
        return 'Greedy evaluation'


    