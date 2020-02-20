from abc import ABCMeta, abstractmethod
import sys

class Heuristic(metaclass=ABCMeta):
    Goals = {}
    numOfGoals = 0
    def __init__(self, initial_state: 'State'):
        # Here's a chance to pre-process the static parts of the level.
        #dictionary of goals
        for ro in range(1,initial_state.MAX_ROW-1) :
            for co in range(1,initial_state.MAX_COL-1) :
                koal = initial_state.goals[ro][co]
                if koal is not None and koal in "abcdefghijklmnopqrstuvwxyz":
                    Heuristic.numOfGoals+=1
                    if koal in Heuristic.Goals.keys() :
                        Heuristic.Goals[koal].append([ro,co])
                    else :
                        Heuristic.Goals[koal] = [[ro,co]]
                    
    def h(self, state: 'State') -> 'int':
        heur=0            
        #dictionary of boxes
        Boxes = {}
        numOfBoxes=0
        for ro in range(1,state.MAX_ROW-1) :
            for co in range(1,state.MAX_COL-1) :
                boal = state.boxes[ro][co]
                if boal is not None and boal in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    boal = boal.casefold()
                    numOfBoxes+=1
                    if boal in Boxes.keys() :
                        Boxes[boal].append([ro,co])
                    else :
                        Boxes[boal] = [[ro,co]]  
                         
        #minimum box and goal distances
        for key in Boxes :
            BoxToGoal = []
            agentBox = []
            if key in Heuristic.Goals :
                for bCR in Boxes[key] :
                    dist=[]
                    for gCR in Heuristic.Goals[key] :
                        dist.append(abs(bCR[0]-gCR[0])+abs(bCR[1]-gCR[1]))
                    agentBox.append(bCR)
                    BoxToGoal.append(dist)
                   
                for x in range(numOfBoxes):
                    minimum = -1
                    minBoxToGoal = -1
                    minBoxToGoalIn = -1
                    for index,btg in enumerate(BoxToGoal) :
                        if len(btg) > 0 :
                            minValue = min(btg)
                            if minimum == -1 or minValue < minimum :
                                minimum = minValue
                                minBoxToGoal = index
                                minBoxToGoalIn = btg.index(minValue)
                    if minBoxToGoal != -1 :
                        #agent to box distance of the boxes that are closest to goal
                        agentB = agentBox.pop(minBoxToGoal)
                        if state.goals[agentB[0]][agentB[1]] is None or state.goals[agentB[0]][agentB[1]]!=state.boxes[agentB[0]][agentB[1]].casefold():
                            calcdist=abs(state.agent_col-agentB[1])
                            heur+=calcdist
                            if calcdist==0:
                                heur+=1
                            if state.agent_col > agentB[1]:
                                heur+=2                              
                        BoxToGoal.pop(minBoxToGoal)
                        heur+=minimum
                        for btg in BoxToGoal :
                            btg.pop(minBoxToGoalIn)
       
        
        return heur
    
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


    