from abc import ABCMeta, abstractmethod
import sys

class Heuristic(metaclass=ABCMeta):
    Goals = {}
    heur=0
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
        Heuristic.heur=0
        CopyGoals = {}
        for key in Heuristic.Goals :
            vList = []
            for v in Heuristic.Goals[key] :
                if state.boxes[v[0]][v[1]] == None or state.goals[v[0]][v[1]] != state.boxes[v[0]][v[1]].casefold() :
                    vList.append(v)
            CopyGoals[key] = vList
        
        for ro in range(state.MAX_ROW) :
            for co in range(state.MAX_COL) :
                #distance of agent to boxes 
                if state.boxes[ro][co] is not None and state.boxes[ro][co] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and state.goals[ro][co] != state.boxes[ro][co].casefold() :
                    calcdist = abs(ro-state.agent_row)+abs(co-state.agent_col)
                    Heuristic.heur+=(calcdist)
                    dist = abs(co-state.agent_col)
                    if dist > 1 :
                        Heuristic.heur+=dist
                #distance of agent to goals
                if state.goals[ro][co] is not None and state.goals[ro][co] in "abcdefghijklmnopqrstuvwqyz" and state.boxes[ro][co] != state.goals[ro][co].capitalize() :
                    calcdist = abs(ro-state.agent_row)+abs(co-state.agent_col)
                    Heuristic.heur+=(calcdist)
                if state.goals[ro][co] is not None and state.goals[ro][co] in "abcdefghijklmnopqrstuvwqyz" :
                    if ro == state.agent_row and co == state.agent_col :
                        Heuristic.heur+=3    
                                    
        for ro in range(state.MAX_ROW) :
            for co in range(state.MAX_COL) :
                if state.boxes[ro][co] is not None and state.boxes[ro][co] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and state.goals[ro][co] != state.boxes[ro][co].casefold() :
                    value = state.boxes[ro][co].casefold()
                    for index,x in enumerate(CopyGoals[value]) :
                        if state.boxes[x[0]][x[1]] is None or state.boxes[x[0]][x[1]].casefold() != state.goals[x[0]][x[1]] :
                            calcdist = abs(x[0]-ro)+abs(x[1]-co)
                            Heuristic.heur+=calcdist
        return Heuristic.heur
    
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


    