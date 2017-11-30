# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
       

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        
        t2 = 0
        # Distance to closest ghost
        mingdist = float("inf")
        for g in newGhostStates:
            gdist = util.manhattanDistance(newPos, g.getPosition())
            mingdist = min(mingdist, gdist)
            
        # Distance to closest food
        minfdist = float("inf")
        food = newFood.asList()
        l=len(food)             # number of food left
        for f in food:
            fdist = util.manhattanDistance(newPos, f)
            minfdist = min(minfdist,fdist)

        t2 = (mingdist/minfdist) + l*-5             # reciprocal of minimum distance to food
        return t2 + successorGameState.getScore()

        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        final = -float("inf")    
        action = ''
        prev=0
        for a in gameState.getLegalActions(0):
            final = max(final,self.MinValue(gameState.generateSuccessor(0,a),self.depth,1))
            if final!=prev:
                action=a
                prev=final
        return action

    # Maximizer 
        
    def MaxValue(self,gameState,dTree):
    	if self.TerminalTest(gameState,dTree):
        	return self.evaluationFunction(gameState)
        v = -float("inf")
        for a in gameState.getLegalActions(0):
        	v = max(v, self.MinValue(gameState.generateSuccessor(0,a),dTree,1))
        return v
        
    # Minimizer
        
    def MinValue(self,gameState,dTree,nGhost):
    	if self.TerminalTest(gameState,dTree):
        	return self.evaluationFunction(gameState)
        v= float("inf")
        for a in gameState.getLegalActions(nGhost):
        	if nGhost==gameState.getNumAgents()-1: #check if last ghost
        		v=min(v, self.MaxValue(gameState.generateSuccessor(nGhost,a),dTree-1))
        	else:
        		nGhost1=nGhost+1   # next ghost
        		v=min(v, self.MinValue(gameState.generateSuccessor(nGhost,a),dTree,nGhost1))
        return v

    def TerminalTest(self,gameState,dTree):
    	if dTree==0 or gameState.isWin() or gameState.isLose():
        	return True
        else:
        	return False
            
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float("inf")
        beta = float("inf")
        final = -float("inf")
        action = ''
        prev = 0
        for a in gameState.getLegalActions(0):
        	final = max(final,self.MinValue(gameState.generateSuccessor(0,a),self.depth,1,alpha,beta))
        	if final!=prev:
        		action=a
        		prev=final
        	alpha=max(alpha,final)
        return action
        
    def MaxValue(self,gameState,dTree,alpha,beta):
    	if self.TerminalTest(gameState,dTree):
        	return self.evaluationFunction(gameState)
        v = -float("inf")
        for a in gameState.getLegalActions(0):
        	v = max(v, self.MinValue(gameState.generateSuccessor(0,a),dTree,1,alpha,beta))
        	if v>beta:
        		return v
        	alpha=max(alpha,v)
        return v
        
        # Minimizer
        
    def MinValue(self,gameState,dTree,nGhost,alpha,beta):
    	if self.TerminalTest(gameState,dTree):
        	return self.evaluationFunction(gameState)
        v= float("inf")
        for a in gameState.getLegalActions(nGhost):
        	if nGhost==gameState.getNumAgents()-1:  #check if last ghost
        		v=min(v, self.MaxValue(gameState.generateSuccessor(nGhost,a),dTree-1,alpha,beta))
        	else:
        		nGhost1=nGhost+1                # next ghost
        		v=min(v, self.MinValue(gameState.generateSuccessor(nGhost,a),dTree,nGhost1,alpha,beta))
            	if v<alpha:
            		return v
            	beta=min(beta,v)                  
        return v

    def TerminalTest(self,gameState,dTree):
    	if dTree==0 or gameState.isWin() or gameState.isLose():
        	return True
        else:
        	return False
        
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
	
	
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        final = -float("inf")
    	action = ''
    	prev=0
    	for a in gameState.getLegalActions(0):
        	final = max(final,self.ExpectiValue(gameState.generateSuccessor(0,a),self.depth,1))
        	if final!=prev:
        		action=a
        		prev=final
        return action
        util.raiseNotDefined()
     
    def MaxValue(self,gameState,dTree):
    	if self.TerminalTest(gameState,dTree):
        	return self.evaluationFunction(gameState)
        v = -float("inf")
        for a in gameState.getLegalActions(0):
        	v = max(v, self.ExpectiValue(gameState.generateSuccessor(0,a),dTree,1))
        return v
        
        # Minimizer
        
    def ExpectiValue(self,gameState,dTree,nGhost):
    	if self.TerminalTest(gameState,dTree):
        	return self.evaluationFunction(gameState)
        v= 0.0
        for a in gameState.getLegalActions(nGhost):
        	l = len(gameState.getLegalActions(nGhost))
        	p = 1.0/l                                       # uniform probability
        	if nGhost==gameState.getNumAgents()-1: # if last ghost
        		v=v+p*(self.MaxValue(gameState.generateSuccessor(nGhost,a),dTree-1))                  
        	else:
        		nGhost1=nGhost+1 # next ghost
        		v=v+p*(self.ExpectiValue(gameState.generateSuccessor(nGhost,a),dTree,nGhost1))
        return v    

    def TerminalTest(self,gameState,dTree):
    	if dTree==0 or gameState.isWin() or gameState.isLose():
        	return True
        else:
            return False
        
    
	
	
        
    
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: I have designed this evaluation function using a linear combination of features by multiplying them
                   with weights according to their importance.

                   I have used reciprocal of the minimum distance from the present position of Pacman to food and multiplied
                   it with 2. This implies that closer the food is to Pacman, the score will increase.

                   Similarly, I have used reciprocal of the minimum distance from the present position of Pacman to a food pellet and
                   multiplied it by 2. I have also used the feature of the minimum ghost distance from this position and multiplied by the same factor
                   but negative. This makes the Pacman rush towards the closest ghost as soon as it eats a food pellet.

                   I have used the features of number of food left and number of capsules left too.I have given the feature of number of food left
                   a weight of -5, which makes Pacman rush towards all food, to avoid losing score. More the food is left, more is the score lost.
                   Similar case applies to food pellets. They fetch a higher score once eaten, so I have assigned a -10 as a weight to it.
                   
                   
    """
    "*** YOUR CODE HERE ***"
    
    GhostStates = currentGameState.getGhostStates()
    Pos = currentGameState.getPacmanPosition()
    score=0
    score1=0
    
    minfdist = float("inf")
    food = currentGameState.getFood()
    food1=food.asList()
    lfood=len(food1)
    for f in food1:
    	fdist = util.manhattanDistance(Pos, f)
    	minfdist = min(minfdist,fdist)
    
    mingdist = float("inf")
    for g in GhostStates:
    	gdist = util.manhattanDistance(Pos, g.getPosition())
    	mingdist = min(mingdist, gdist)
    
    mincdist = float("inf")
    capsule = currentGameState.getCapsules()
    ncapsules=len(capsule)
    for c in capsule:
    	cdist = util.manhattanDistance(Pos, c)
    	mincdist = min(mincdist,cdist)    

    score = ((1.0/minfdist)*2) + ((1.0/mincdist)*2) + (mingdist*-2) + lfood*-5 + ncapsules*-10
    score1 = currentGameState.getScore() + score 
    return score1
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

