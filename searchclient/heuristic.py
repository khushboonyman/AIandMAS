from abc import ABCMeta, abstractmethod

class Heuristic(metaclass=ABCMeta):
    Goals = {}
    heur=0
    def __init__(self, initial_state: 'State'):
        # Here's a chance to pre-process the static parts of the level.
        for ro in range(initial_state.MAX_ROW) :
            for co in range(initial_state.MAX_COL) :
                koal = initial_state.goals[ro][co]
                if koal is not None and koal in "abcdefghijklmnopqrstuvwxyz":
                    if koal in Heuristic.Goals.keys() :
                        Heuristic.Goals[koal].append([ro,co])
                    else :
                        Heuristic.Goals[koal] = [[ro,co]]
                    
    def h(self, state: 'State') -> 'int':
        Heuristic.heur=0
        agentdist=[]
        for ro in range(state.MAX_ROW) :
            for co in range(state.MAX_COL) :
                if state.boxes[ro][co] is not None and state.boxes[ro][co] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and state.goals[ro][co] != state.boxes[ro][co].casefold() :
                    dist=[]
                    calcdist = abs(ro-state.agent_row)+abs(co-state.agent_col)
                    if calcdist > 0 :
                        agentdist.append(calcdist)
                    value = state.boxes[ro][co].casefold()
                    for x in Heuristic.Goals[value] :
                        calcdist = abs(x[0]-ro)+abs(x[1]-co)
                        if calcdist > 0 :
                            dist.append(calcdist)
                    if len(dist) > 0 :
                        Heuristic.heur += min(dist)
                    #print('heuristic!!',Heuristic.heur)
        if len(agentdist) > 0 :
            Heuristic.heur+=min(agentdist)
        #print('heuristic!!',Heuristic.heur)
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


    