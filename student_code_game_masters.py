from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        ask = parse_input("fact: (inst ?x peg)")
        answers = self.kb.kb_ask(ask)
        peglist = list()
        for answer in answers:
            peglist.append(str(answer).split()[-1])
        finalList = list()
        for peg in peglist:
            ask = parse_input("fact: (on ?x " + peg + ")")
            answers = self.kb.kb_ask(ask)
            pegDisklist = list()
            if not answers:
                finalList.append(tuple(pegDisklist))
                continue
            for answer in answers:
                pegDisklist.append(int(str(answer)[-1:]))
            pegDisklist.sort()
            finalList.append(tuple(pegDisklist))
        return(tuple(finalList))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        sl = movable_statement.terms
        diskToMove = str(sl[0])
        oldPeg = str(sl[1])
        newPeg = str(sl[2])
        # Get disk under disk to be moved
        ask = parse_input("fact: (ontop " + diskToMove + " ?x)")
        answers = self.kb.kb_ask(ask)
        oldPegEmpty = False
        if answers:
            diskUnder = str(answers[0]).split()[-1]
        else:
            oldPegEmpty = True
        # Check if destination peg empty
        ask = parse_input("fact: (topOfPeg ?x " + newPeg + ")")
        topOfNewPeg = self.kb.kb_ask(ask)
        newPegEmpty = True
        # Find old top of destination peg
        if topOfNewPeg:
            oldTopNewPeg = str(topOfNewPeg[0]).split()[-1]
            newPegEmpty = False
        # Remove disk from old peg
        statement = parse_input("fact: (on " + diskToMove + " " + oldPeg + ")")
        self.kb.kb_retract(statement)
        # Remove relationship between disk and disk under it
        if not oldPegEmpty:
            statement2 = parse_input("fact: (ontop " + diskToMove + " " + diskUnder + ")")
            self.kb.kb_retract(statement2)
            statement5 = parse_input("fact: (TopofStack " + diskUnder + ")")
            self.kb.kb_assert(statement5)
        else:
            statement7 = parse_input("fact: (empty " + oldPeg + ")")
            self.kb.kb_assert(statement7)
        # Remove old top of stack
        statement3 = parse_input("fact: (TopofStack " + diskToMove + ")")
        self.kb.kb_retract(statement3)
        # Add disk to newPeg
        statement8 = parse_input("fact: (on " + diskToMove + " " + newPeg + ")")
        self.kb.kb_assert(statement8)
        statement9 = parse_input("fact: (TopofStack " + diskToMove + ")")
        self.kb.kb_assert(statement9)
        if not newPegEmpty:
            statement10 = parse_input("fact: (ontop " + diskToMove + " " + oldTopNewPeg + ")")
            self.kb.kb_assert(statement10)
            statement11 = parse_input("fact: (TopofStack " + oldTopNewPeg + ")")
            self.kb.kb_retract(statement11)
        else:
            statement12 = parse_input("fact: (empty " + newPeg + ")")
            self.kb.kb_retract(statement12)





    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        topRow = list()
        middleRow = list()
        bottomRow = list()
        ask = parse_input("fact: (position ?a pos1 pos1)")
        answers = self.kb.kb_ask(ask)
        tile = str(answers[0]).split()[-1]
        if tile == "empty":
            topRow.append(-1)
        else:
            topRow.append((int(str(answers[0])[-1:])))
        ask = parse_input("fact: (position ?a pos2 pos1)")
        answers = self.kb.kb_ask(ask)
        tile = str(answers[0]).split()[-1]
        if tile == "empty":
            topRow.append(-1)
        else:
            topRow.append((int(str(answers[0])[-1:])))
        ask = parse_input("fact: (position ?a pos3 pos1)")
        answers = self.kb.kb_ask(ask)
        tile = str(answers[0]).split()[-1]
        if tile == "empty":
            topRow.append(-1)
        else:
            topRow.append((int(str(answers[0])[-1:])))
        ask = parse_input("fact: (position ?a pos1 pos2)")
        answers = self.kb.kb_ask(ask)
        tile = str(answers[0]).split()[-1]
        if tile == "empty":
            middleRow.append(-1)
        else:
            middleRow.append((int(str(answers[0])[-1:])))
        ask = parse_input("fact: (position ?a pos2 pos2)")
        answers = self.kb.kb_ask(ask)
        tile = str(answers[0]).split()[-1]
        if tile == "empty":
            middleRow.append(-1)
        else:
            middleRow.append((int(str(answers[0])[-1:])))
        ask = parse_input("fact: (position ?a pos3 pos2)")
        answers = self.kb.kb_ask(ask)
        tile = str(answers[0]).split()[-1]
        if tile == "empty":
            middleRow.append(-1)
        else:
            middleRow.append((int(str(answers[0])[-1:])))
        ask = parse_input("fact: (position ?a pos1 pos3)")
        answers = self.kb.kb_ask(ask)
        tile = str(answers[0]).split()[-1]
        if tile == "empty":
            bottomRow.append(-1)
        else:
            bottomRow.append((int(str(answers[0])[-1:])))
        ask = parse_input("fact: (position ?a pos2 pos3)")
        answers = self.kb.kb_ask(ask)
        tile = str(answers[0]).split()[-1]
        if tile == "empty":
            bottomRow.append(-1)
        else:
            bottomRow.append((int(str(answers[0])[-1:])))
        ask = parse_input("fact: (position ?a pos3 pos3)")
        answers = self.kb.kb_ask(ask)
        tile = str(answers[0]).split()[-1]
        if tile == "empty":
            bottomRow.append(-1)
        else:
            bottomRow.append((int(str(answers[0])[-1:])))
        finalTuple = (tuple(topRow), tuple(middleRow), tuple(bottomRow))
        return(finalTuple)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        sl = movable_statement.terms
        tile = str(sl[0])
        oldx = str(sl[1])
        oldy = str(sl[2])
        newx = str(sl[3])
        newy = str(sl[4])
        # Get adjacents of tile
        ask = parse_input("fact: (adjacent " + tile + " ?x)")
        answers = self.kb.kb_ask(ask)
        tileAdjacents = list()
        for answer in answers:
            adjacentTile = str(answer).split()[-1]
            if adjacentTile != tile:
                tileAdjacents.append(adjacentTile)
        ask = parse_input("fact: (adjacent empty ?x)")
        answers = self.kb.kb_ask(ask)
        emptyAdjacents = list()
        for answer in answers:
            adjacentTile = str(answer).split()[-1]
            if adjacentTile != "empty":
                emptyAdjacents.append(adjacentTile)
        # Switch adjacents of tiles
        for adjacent in tileAdjacents:
            statement = parse_input("fact: (adjacent " + adjacent + " " + tile + ")")

            self.kb.kb_retract(statement)
            if adjacent == "empty":
                statement3 = parse_input("fact: (adjacent " + tile + " empty)")
            else:
                statement3 = parse_input("fact: (adjacent " + adjacent + " empty)")
            self.kb.kb_assert(statement3)
        for adjacent in emptyAdjacents:
            statement2 = parse_input("fact: (adjacent " + adjacent + " empty)")
            self.kb.kb_retract(statement2)
            if adjacent == tile:
                statement4 = parse_input("fact: (adjacent " + tile + " empty)")
            else:
                statement4 = parse_input("fact: (adjacent " + adjacent + " " + tile + ")")
            self.kb.kb_assert(statement4)
        # Change positions of tiles
        statement5 = parse_input("fact: (position " + tile + " " + newx + " " + newy + ")")
        self.kb.kb_assert(statement5)
        statement6 = parse_input("fact: (position empty " + oldx + " " + oldy + ")")
        self.kb.kb_assert(statement6)
        statement7 = parse_input("fact: (position " + tile + " " + oldx + " " + oldy + ")")
        self.kb.kb_retract(statement7)
        statement8 = parse_input("fact: (position empty " + newx + " " + newy + ")")
        self.kb.kb_retract(statement8)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
