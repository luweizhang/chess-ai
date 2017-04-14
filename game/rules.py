from collections import defaultdict
import pieces

class RulesEnforcer(object):
    """
    Enforces the rules of the game
    Examines the move, and determines whether its a valid move or not.
    """

    letter_dict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    pos_letters = letter_dict.keys()
    pos_nums = [1,2,3,4,5,6,7,8]
    letter_dict_rev = dict((v,k) for k,v in letter_dict.iteritems())
    possible_pieces = ['p','r','n','b','q','k']
    
    def __init__(self):
        pass

    

    @staticmethod
    def check_square(chessboard, coordinate):
        """
        Takes as input a chess board and coordinate and outputs
        what is inside that space

        This is useful for a variable of purposes
        """
        mycord = RulesEnforcer.coordinate_mapper(coordinate)

        first = mycord[0]
        second = mycord[1]

        return chessboard[first][second]


    @staticmethod
    def possible_moves(chessboard, color, piece, coordinate):
        """return possible moves of a piece
        
        a number of things need to be taken into a count
        1. whether we are allowed to move the piece
        
        input:  piece, color, and coordinate of piece
        output: all possible moves of the piece (lists of lists)
        
        Example of a cooridinate: a2
        """

        #if the coordinate is an array 
        if type(coordinate) == list:
            coordinate = RulesEnforcer.coordinate_mapper_reverse(coordinate)

        #break out coordinate into a list of len(2)
        cords = list(coordinate)
        cords[1] = int(cords[1])

        #pawns
        if piece == 'p':
            pos_moves = pieces.Pawn.moves(cords, color, chessboard)  

        #rook
        elif piece == 'r':
            pos_moves = pieces.Rook.moves(cords, color, chessboard)
        
        #knight
        elif piece == 'n':
            pos_moves = pieces.Knight.moves(cords, color, chessboard)
        
        #bishop
        elif piece == 'b':
            pos_moves = pieces.Bishop.moves(cords, color, chessboard)
        
        #queen
        elif piece == "q":
            pos_moves = pieces.Queen.moves(cords, color, chessboard)
        
        #king
        elif piece == "k":
            pos_moves = pieces.King.moves(cords, color, chessboard)
            
        else:                 
            return "invalid inputs!"
            

        return pos_moves

    @staticmethod
    def all_possible_moves(chessboard, color):
        """takes as input a chessboard and generates all possible moves

        input: 
            color: color that you want to generate moves for, 'w' or 'b'
            chessboard: 8x8 chessboard
        output: dict of all possible moves 
            key: piece and position
            value: list of list of possible moves
        """

        #dict for storing all the moves
        all_moves = defaultdict()

        for cor1, row in enumerate(chessboard):
            for cor2, square in enumerate(row):
                if square.split('-')[0] == color:
                    piece = square.split('-')[1]
                    coordinate = [cor1, cor2]
                    
                    moves = RulesEnforcer.possible_moves(chessboard, color, piece, coordinate)

                    if moves:
                        all_moves[RulesEnforcer.coordinate_mapper_reverse(coordinate)] = moves

        return all_moves

    @staticmethod
    def remove_outofbound_moves(pos_moves):
        """remove moves that are out of range of the board
        input: list of list of moves
        output: list of list of moves, with out of bound moves removed
        """

        to_remove = []
        for i in range(len(pos_moves)):
            if pos_moves[i][0] not in RulesEnforcer.pos_letters or pos_moves[i][1] not in RulesEnforcer.pos_nums:
                to_remove.append(pos_moves[i])                                          
        for i in to_remove:
            pos_moves.remove(i)
            
        return pos_moves
        
    @staticmethod
    def collision_detection(move, color, chessboard):
        """
        Collision detection for the chess game.  
        
        input:
            move: the move i.e ['a',7]
            color: white ('w') or black ('b')
            chessboard: chessboard object
        output: "friend" or "enemy" depending on what color you are and what the enemy color is
        
        """ 
        try:
            move = RulesEnforcer.coordinate_mapper(move)
        except:
            return False

        x = move[0]
        y = move[1]

        try:
            piece = chessboard[x][y]
        except:
            return False

        if color == 'w' and piece.split('-')[0] == 'w':
            return "friend"
        elif color == 'b' and piece.split('-')[0] == 'b':
            return "friend"
        if color == 'w' and piece.split('-')[0] == 'b':
            return "enemy"
        elif color == 'b' and piece.split('-')[0] == 'w':
            return "enemy"
        else:
            return "empty"


    @staticmethod            
    def move_allowed(move, chessboard):
        """
        Determine if the move is allowed
        
        input: 
            move: the move
            chessboard: chessboard object
        output: boolean, whether the move is allowed or not
        
        """
        pass
        
    
    @staticmethod
    def coordinate_mapper(mycoordinate):
        """takes as input a chess coordinate and maps it to the coordinate in the array
        
        input: chess coordinate (ie a5)
        output: coordinate of the array to be used in the chessboard 
                for example: [0,2]
        
        """
        mycoordinate  = list(mycoordinate)

        starthor  = RulesEnforcer.letter_dict[mycoordinate[0]]
        startver  = 7 - (int(mycoordinate[1]) - 1)
        
        return [startver, starthor]

    @staticmethod
    def coordinate_mapper_reverse(myarray):
        """
        Does the opposite of coordinate_mapper().  Takes as input array coordinates (ie. [0,5])

        This method is useful if you 
        
        input: a length 2 list of array coordinates
        output: chess coordinate (str)

        example:
        [7,0] -> a1
        """

        #letter of cor
        first_cor  = RulesEnforcer.letter_dict_rev[myarray[1]]
        #number of cor
        second_cor = 8 - myarray[0] 
        
        return str(first_cor) + str(second_cor)
        
    
    @staticmethod
    def legal_move_checker(start, finish):
        """checks if a move is legal or not based on the type of piece"""
        pass