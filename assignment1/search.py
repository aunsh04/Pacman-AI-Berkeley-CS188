# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
	"""
    
    "*** YOUR CODE HERE ***"
    
    
    # s = util.Stack()
#     explored = []
#     solution = []
#     su = []
# 	s.push(problem.getStartState())
#     while not s.isEmpty():
#     	x = s.pop()
#     	if x not in explored:
#     		explored.append(x)
#     	solution.append(x)
#     	su = problem.getSuccessors(x)
#     	for st in su:
#     		if(st not in s) or (st not in explored):
#     			s.push(st)
#     return solution				
    	
    x=[]
    explored=[]
    temp=[]
    n=(problem.getStartState(), ' ',0,x)
    s=util.Stack()
    s.push(n)
    while not s.isEmpty():
    	i,j,k,l=s.pop()
    	explored.append(i)
    	if problem.isGoalState(i):
    		return l
    	s1=problem.getSuccessors(i)
    	for state in s1:
    		if state[0] not in explored:
    			temp = l + [state[1]]
    			t=(state[0],state[1],state[2],temp)
    			s.push(t)
    		
    			
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):

    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    x=[]
    explored=[]
    list=[]
    temp=[]
    n=(problem.getStartState(), ' ',0,x)
    q=util.Queue()
    q.push(n)
    list.append(n[0])
    while not q.isEmpty():
    	i,j,k,l=q.pop()
    	explored.append(i)
    	list.remove(i)
    	if problem.isGoalState(i):
    		return l
    	s=problem.getSuccessors(i)
    	for state in s:
    		if state[0] not in explored and state[0] not in list:
    			temp = l + [state[1]]
    			t=(state[0],state[1],state[2],temp)
    			q.push(t)
    			list.append(state[0])						 	
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
 	
    totalcost={}
    temp1=[]
    x=[]
    explored=set()
    n=(problem.getStartState(),' ',0,x)
    p=util.PriorityQueue()
    p.push(n,0)
    totalcost[n[0]]=0
    while not p.isEmpty():
    	i,j,k,l=p.pop()
    	if problem.isGoalState(i):
    		return l
    	s=problem.getSuccessors(i)	
    	for state in s:
    		temp=totalcost[i]+state[2]
    		if state[0] not in totalcost or temp<totalcost[state[0]]:
    			totalcost[state[0]]=temp
    			temp1=l+[state[1]]
    			t=(state[0],state[1],state[2],temp1)
    			p.push(t,temp)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    totalcost={}
    temp1=[]
    x=[]
    explored=set()
    n=(problem.getStartState(),' ',0,x)
    p=util.PriorityQueue()
    p.push(n,0)
    totalcost[n[0]]=0
    while not p.isEmpty():
    	i,j,k,l=p.pop()
    	explored.add(i)
    	if problem.isGoalState(i):
    		return l
    	s=problem.getSuccessors(i)		
    	for state in s:
    		temp=totalcost[i]+state[2]
    		if state[0] not in totalcost or temp<totalcost[state[0]]:
    			totalcost[state[0]]=temp
    			temp1=l+[state[1]]
    			t=(state[0],state[1],state[2],temp1)
    			priority=temp+heuristic(t[0],problem)
    			p.push(t,priority)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

