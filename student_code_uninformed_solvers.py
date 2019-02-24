from solver import *
import queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def _getChildStates(self):
        # Get movables
        movables = self.gm.getMovables()
        for movable in movables:
            self.gm.makeMove(movable)
            childState = self.gm.getGameState()
            # Generate child game state
            childGS = GameState(childState, self.currentState.depth + 1, movable)
            # only add child state if it hasn't already been visited
            # so we don't get into infinite loops
            if childGS not in self.visited:
                childGS.parent = self.currentState
                self.currentState.children.append(childGS)
            # reverse the move
            self.gm.reverseMove(movable)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState not in self.visited:
            self.visited[self.currentState] = True
            #return self.currentState.state == self.victoryCondition
        if self.currentState.state == self.victoryCondition:
            return True

        # if this is the first time a state is being visited, generate all the
        # children nodes (game states) by making all the possible moves from the current state
        # We also reverse the moves because we don't want to process those states
        # before processing the current state
        if self.currentState.nextChildToVisit == 0:
            self._getChildStates()


        # Now process the next child to be processed
        numberOfChildren = len(self.currentState.children)
        if self.currentState.nextChildToVisit < numberOfChildren:
            # Visit next child
            childState = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            self.gm.makeMove(childState.requiredMovable)
            self.currentState = childState
            return False
        else:
            #All child nodes have been processed. Move back to parent
            self.currentState.nextChildToVisit += 1
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStep()


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = queue.Queue()

    def _getChildStates(self):
        # Get movables
        movables = self.gm.getMovables()
        for movable in movables:
            self.gm.makeMove(movable)
            childState = self.gm.getGameState()
            # Generate child game state
            childGS = GameState(childState, self.currentState.depth + 1, movable)
            # only add child state if it hasn't already been visited
            # so we don't get into infinite loops
            if childGS not in self.visited:
                childGS.parent = self.currentState
                self.currentState.children.append(childGS)
                self.queue.put(childGS)
            # reverse the move
            self.gm.reverseMove(movable)

    def _goToRoot(self):
        while self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

    def _getPathFromRootToState(self, state):
        pathToStateFromRoot = list()
        while state.requiredMovable:
            pathToStateFromRoot.append(state.requiredMovable)
            state = state.parent
        return pathToStateFromRoot

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState not in self.visited:
            self.visited[self.currentState] = True
        if self.currentState.state == self.victoryCondition:
            return True

        while True:
            if not self.currentState.children:
                # Get child states and append to current state
                # Also add child to queue
                self._getChildStates()

            nextState = self.queue.get()
            if nextState in self.visited:
                continue

            # Go back to root and traverse to next state to get the path
            # from root to next state
            self._goToRoot()
            pathToNextStateFromRoot = self._getPathFromRootToState(nextState)

            while pathToNextStateFromRoot:
                move = pathToNextStateFromRoot.pop(-1)
                self.gm.makeMove(move)
                newState = self.gm.getGameState()
                for child in self.currentState.children:
                    if child.state == newState:
                        self.currentState = child
                        self.visited[self.currentState] = True
                        break
            break
        return False

