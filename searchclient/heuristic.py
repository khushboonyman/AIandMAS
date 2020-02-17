from abc import ABCMeta, abstractmethod
import sys

class Heuristic(metaclass=ABCMeta):
    Goals = {}
    def __init__(self, initial_state: 'State'):
        # Here's a chance to pre-process the static parts of the level.
        for ro in range(initial_state.MAX_ROW) :
            for co in range(initial_state.MAX_COL) :
                if initial_state.goals[ro][co] is not None and initial_state.boxes[ro][co] is not None and initial_state.goals[ro][co] == initial_state.boxes[ro][co].casefold() :
                    initial_state.goals[ro][co] = None
                    initial_state.boxes[ro][co] = None
                koal = initial_state.goals[ro][co]
                if koal is not None and koal in "abcdefghijklmnopqrstuvwxyz":
                    if koal in Heuristic.Goals.keys() :
                        Heuristic.Goals[koal].append([ro,co])
                    else :
                        Heuristic.Goals[koal] = [[ro,co]]
                    
    def h(self, state: 'State') -> 'int':
        heur=0
        CopyGoals = {}
        for key in Heuristic.Goals :
            vList = []
            for v in Heuristic.Goals[key] :
                if state.boxes[v[0]][v[1]] == None or state.goals[v[0]][v[1]] != state.boxes[v[0]][v[1]].casefold() :
                    vList.append(v)
            CopyGoals[key] = vList
            
        Boxes = {}
        for ro in range(state.MAX_ROW) :
            for co in range(state.MAX_COL) :
                if state.boxes[ro][co] is not None and state.boxes[ro][co] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and state.goals[ro][co] != state.boxes[ro][co].casefold() :
                    bo = state.boxes[ro][co]
                    if bo in Boxes.keys() :
                        Boxes[bo].append([ro,co])
                    else :
                        Boxes[bo] = [[ro,co]]        
        #agent to goal
        for key in CopyGoals :
            for cr in CopyGoals[key] :
                if state.boxes[cr[0]][cr[1]]!=key.capitalize():
                    calcdist=(abs(cr[0]-state.agent_row)+abs(cr[1]-state.agent_col))
                    if calcdist==0:
                        calcdist+=3
                    heur+=calcdist
        
        for key in Boxes :
            for index,cr in enumerate(Boxes[key]) :
                #agent to boxes
                if state.goals[cr[0]][cr[1]]!=key.casefold():
                    calcdist=(abs(cr[0]-state.agent_row)+abs(cr[1]-state.agent_col))
                    heur+=calcdist
                    calcdist=abs(state.agent_col-cr[1])
                    if calcdist > 1 :
                        heur+=calcdist
                #goals to boxes
                value = key.casefold()
                for x in CopyGoals[value] :
                    if not (x[0]==cr[0] and x[1]==cr[1]) :
                        calcdist=abs(cr[0]-x[0])+abs(cr[1]-x[1])
                        heur+=calcdist
                
                  
        #boxes to goals                            
        """for ro in range(state.MAX_ROW) :
            for co in range(state.MAX_COL) :
                if state.boxes[ro][co] is not None and state.boxes[ro][co] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    value = state.boxes[ro][co].casefold()
                    for x in CopyGoals[value] :
                        if state.boxes[x[0]][x[1]] is None or state.boxes[x[0]][x[1]].casefold() != state.goals[x[0]][x[1]] :
                            calcdist = abs(x[0]-ro)+abs(x[1]-co)
                            heur+=calcdist"""
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


    