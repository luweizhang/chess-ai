import itertools
from rules import RulesEnforcer

"""
Movement behavior for each of the different pieces.
"""

class Pawn(object):
    """
    Movement behavior for this piece
    Note that the pawn is able to take pieces that are across from it, so we will need to scan 
    the board for diagonally adjacent pieces to identify piece taking opportunities
    """
    @staticmethod
    def moves(cords, color, chessboard = None):
        """
        takes as input the coordinate and color of the piece, outputs the possible moves
        Pawns can attack adjacent diagonals
        """
        
        if not chessboard:
            if color == 'w':
                if int(cords[1]) == 2:
                    #if the pawn is at the starting position then it can move either one or two squares
                    pos_moves = [[cords[0], int(cords[1]) + 1], [cords[0], int(cords[1]) + 2]]
                else:
                    pos_moves = [[cords[0], int(cords[1]) + 1]]
            if color == 'b':
                if int(cords[1]) == 7:
                    pos_moves = [[cords[0], int(cords[1]) - 1], [cords[0], int(cords[1]) - 2]]
                else:
                    pos_moves = [[cords[0], int(cords[1]) - 1]]

        
        obstructed = False
        if chessboard:
            pos_moves = []
            if color == 'w':
                move1 = [cords[0], int(cords[1]) + 1]
                if RulesEnforcer.collision_detection(move1, color, chessboard) not in ["friend","enemy"]:
                    pos_moves.append(move1)
                else:
                    obstructed = True

                if int(cords[1]) == 2 and obstructed == False:
                    move2 = [cords[0], int(cords[1]) + 2]
                    if RulesEnforcer.collision_detection(move2, color, chessboard) not in ["friend","enemy"]:
                        pos_moves.append(move2)
            if color == 'b':
                move1 = [cords[0], int(cords[1]) - 1]
                if RulesEnforcer.collision_detection(move1, color, chessboard) not in ["friend","enemy"]:
                    pos_moves.append(move1)
                else:
                    obstructed = True

                if int(cords[1]) == 7 and obstructed == False:
                    move2 = [cords[0], int(cords[1]) - 2]
                    if RulesEnforcer.collision_detection(move2, color, chessboard) not in ["friend","enemy"]:
                        pos_moves.append(move2)

        #check adjacent diagonals for piece taking opportunities
        if chessboard:
            board_cords = RulesEnforcer.coordinate_mapper(cords)
            if color == 'w':
                #check diagonal left
                if board_cords[0] > 0 and board_cords[1] > 0:
                    row    = board_cords[0] - 1
                    column = board_cords[1] - 1
                    square = chessboard[row][column]
                    if square.split('-')[0] == 'b':
                        final_cord = RulesEnforcer.coordinate_mapper_reverse([row,column])
                        pos_moves.append([final_cord[0],int(final_cord[1])])

                #check diagonal right
                if board_cords[0] > 0 and board_cords[1] < 7:
                    row    = board_cords[0] - 1
                    column = board_cords[1] + 1
                    square = chessboard[row][column]
                    if square.split('-')[0] == 'b':
                        final_cord = RulesEnforcer.coordinate_mapper_reverse([row,column])
                        pos_moves.append([final_cord[0],int(final_cord[1])])
                
            if color == 'b':
                #check diagonal left
                if board_cords[0] < 7 and board_cords[1] > 0:
                    row    = board_cords[0] + 1
                    column = board_cords[1] - 1
                    square = chessboard[row][column] 
                    if square.split('-')[0] == 'w':
                        final_cord = RulesEnforcer.coordinate_mapper_reverse([row,column])
                        pos_moves.append([final_cord[0],int(final_cord[1])])

                #check diagonal right
                if board_cords[0] < 7 and board_cords[1] < 7:
                    row    = board_cords[0] + 1
                    column = board_cords[1] + 1
                    square = chessboard[row][column]
                    if square.split('-')[0] == 'w':
                        final_cord = RulesEnforcer.coordinate_mapper_reverse([row,column])
                        pos_moves.append([final_cord[0],int(final_cord[1])])

        pos_moves = RulesEnforcer.remove_outofbound_moves(pos_moves)
        return pos_moves
        
        
class Rook(object):
    """
    Movement behavior for this piece
    
    The rook can move horizontally and vertically
    """
    @staticmethod
    def moves(cords, color, chessboard = None):
        pos_moves = []
        
        x = cords[0] #g
        y = int(cords[1]) #5
        
        x_new = ord(cords[0]) #g
        y_new = int(cords[1]) #5
        #while x is between 'a' and 'h' and..
        while x_new >= 97 and x_new <= 104 and y_new >= 1 and y_new <= 8:
            x_new = x_new + 1
            

            move = [chr(x_new), y_new]

            if chessboard:
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    break
                elif RulesEnforcer.collision_detection(move, color, chessboard) == "enemy":
                    pos_moves.append(move)
                    break
                else:
                    pass

            pos_moves.append(move)
        
        x_new = ord(cords[0]) #g
        y_new = int(cords[1]) #5   
        while x_new >= 97 and x_new <= 104 and y_new >= 1 and y_new <= 8:
            x_new = x_new - 1
            

            move = [chr(x_new), y_new]

            if chessboard:
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    break
                elif RulesEnforcer.collision_detection(move, color, chessboard) == "enemy":
                    pos_moves.append(move)
                    break
                else:
                    pass

            pos_moves.append(move)
            
        x_new = ord(cords[0]) #g
        y_new = int(cords[1]) #5     
        while x_new >= 97 and x_new <= 104 and y_new >= 1 and y_new <= 8:
            y_new = y_new - 1

            move = [chr(x_new), y_new]

            if chessboard:
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    break
                elif RulesEnforcer.collision_detection(move, color, chessboard) == "enemy":
                    pos_moves.append(move)
                    break
                else:
                    pass

            pos_moves.append(move)
            
        x_new = ord(cords[0]) #g
        y_new = int(cords[1]) #5       
        while x_new >= 97 and x_new <= 104 and y_new >= 1 and y_new <= 8:
            y_new = y_new + 1

            move = [chr(x_new), y_new]

            if chessboard:
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    break
                elif RulesEnforcer.collision_detection(move, color, chessboard) == "enemy":
                    pos_moves.append(move)
                    break
                else:
                    pass

            pos_moves.append(move)
        
        pos_moves = RulesEnforcer.remove_outofbound_moves(pos_moves)
        return pos_moves

    
class Knight(object):
    """
    Movement behavior for this piece
    
    The knight moves in an L shape
    """
    @staticmethod
    def moves(cords, color, chessboard = None):
        """
        takes as input the coordinate and color of the piece, outputs the possible moves
        
        """
        pos_hor1 = [chr(ord(cords[0]) + 1), chr(ord(cords[0]) - 1)]
        pos_hor2 = [chr(ord(cords[0]) + 2), chr(ord(cords[0]) - 2)]

        pos_ver1 = [int(cords[1]) + 1, int(cords[1]) - 1]
        pos_ver2 = [int(cords[1]) + 2, int(cords[1]) - 2]

        pos_moves1 = list(itertools.product(pos_hor1, pos_ver2))  
        pos_moves2 = list(itertools.product(pos_hor2, pos_ver1))  

        pos_moves = pos_moves1 + pos_moves2        
        pos_moves = [list(i) for i in pos_moves]
        
        pos_moves = RulesEnforcer.remove_outofbound_moves(pos_moves)
        
        #If chessboard exists, then run collision detection
        if chessboard:
            for i in range(len(pos_moves)):
                move = pos_moves[i]
                
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    pos_moves[i] = 'remove'

            while 'remove' in pos_moves:
                pos_moves.remove('remove')

        return pos_moves
    
class Bishop(object):
    """Movement behavior for this piece"""
    @staticmethod
    def moves(cords, color, chessboard = None):
        pos_moves = []
        
        x = cords[0] #g
        y = int(cords[1]) #5
        
        x_new = ord(cords[0]) #g
        y_new = int(cords[1]) #5
        #while x is between 'a' and 'h' and..
        while x_new >= 97 and x_new <= 104 and y_new >= 1 and y_new <= 8:
            x_new = x_new + 1
            y_new = y_new + 1

            move = [chr(x_new), y_new]

            if chessboard:
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    break
                elif RulesEnforcer.collision_detection(move, color, chessboard) == "enemy":
                    pos_moves.append(move)
                    break
                else:
                    pass

            pos_moves.append(move)
        
        x_new = ord(cords[0]) #g
        y_new = int(cords[1]) #5   
        while x_new >= 97 and x_new <= 104 and y_new >= 1 and y_new <= 8:
            x_new = x_new - 1
            y_new = y_new - 1

            move = [chr(x_new), y_new]

            if chessboard:
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    break
                elif RulesEnforcer.collision_detection(move, color, chessboard) == "enemy":
                    pos_moves.append(move)
                    break
                else:
                    pass

            pos_moves.append(move)
            
        x_new = ord(cords[0]) #g
        y_new = int(cords[1]) #5     
        while x_new >= 97 and x_new <= 104 and y_new >= 1 and y_new <= 8:
            x_new = x_new + 1
            y_new = y_new - 1

            move = [chr(x_new), y_new]

            if chessboard:
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    break
                elif RulesEnforcer.collision_detection(move, color, chessboard) == "enemy":
                    pos_moves.append(move)
                    break
                else:
                    pass

            pos_moves.append(move)
            
        x_new = ord(cords[0]) #g
        y_new = int(cords[1]) #5       
        while x_new >= 97 and x_new <= 104 and y_new >= 1 and y_new <= 8:
            x_new = x_new - 1
            y_new = y_new + 1

            move = [chr(x_new), y_new]

            if chessboard:
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    break
                elif RulesEnforcer.collision_detection(move, color, chessboard) == "enemy":
                    pos_moves.append(move)
                    break
                else:
                    pass

            pos_moves.append(move)
        
        pos_moves = RulesEnforcer.remove_outofbound_moves(pos_moves)
        return pos_moves
    
class Queen(object):
    """Movement behavior for this piece
    Should be a combination of the bishop and the rook, so we should be able to combine those two movements
    """
    @staticmethod
    def moves(cords, color, chessboard = None):
        pos_moves_verthor = Rook.moves(cords,color,chessboard)
        pos_moves_diag    = Bishop.moves(cords,color,chessboard)
        
        pos_moves = pos_moves_verthor + pos_moves_diag
        pos_moves = RulesEnforcer.remove_outofbound_moves(pos_moves)
        return pos_moves
        
class King(object):
    """Movement behavior for the King.
    The king is a special piece because there is the concept of "check."  
    If the king is under check, then something has to be done to move the king out of check. 
    The state of "check" will be stored here so that we can incorporate this logic.
    
    Also, another nuance is that the king cannot move somewhere where he can be attacked or in "check"
    So we need to incorporate logic to account for this as well

    """

    def __init__(self, color):
        self.color = color
        self.check = False
        
    @staticmethod
    def moves(cords, color, chessboard = None):
        x = cords[0] #g
        y = int(cords[1]) #5
        
        pos_moves = []
        
        x_new = ord(cords[0]) #g
        y_new = int(cords[1]) #5
        
        #8 possible locations where the king can move
        pos_moves.append([chr(x_new + 1), y_new])
        pos_moves.append([chr(x_new - 1), y_new])
        pos_moves.append([chr(x_new), y_new + 1])
        pos_moves.append([chr(x_new), y_new - 1])
        pos_moves.append([chr(x_new + 1), y_new + 1])
        pos_moves.append([chr(x_new + 1), y_new - 1])
        pos_moves.append([chr(x_new - 1), y_new + 1])
        pos_moves.append([chr(x_new - 1), y_new - 1])
                                    
        pos_moves = RulesEnforcer.remove_outofbound_moves(pos_moves)

        #If chessboard exists, then run collision detection
        if chessboard:
            for i in range(len(pos_moves)):
                move = pos_moves[i]
                
                if RulesEnforcer.collision_detection(move, color, chessboard) == "friend":
                    pos_moves[i] = 'remove'

            while 'remove' in pos_moves:
                pos_moves.remove('remove')

        return pos_moves