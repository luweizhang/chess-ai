"""chess game"""
import math
import itertools

from game import RulesEnforcer
from ai import ChessAi


class ChessGame(RulesEnforcer,ChessAi):
    def __init__(self, ai_depth):
        """
        Creates a chessboard with pieces
        
        params:
        ai_depth: max number of moves to search into the future
        
        Notation:
        ------------
        000 == empty space  
        
        "b-p"   == black pawn
        "b-r"   == black rook
        "b-r"   == black rook
        "b-n"   == black knight
        "b-b"   == black bishop
        "b-q"   == black queen
        "b-k"   == black king  
        
        "w-k"   == white king

        ... etc etc you get the idea
        
        
        As soon as the chess game is initialized, the chess computer will start calculating

        """
        
        ChessAi.__init__(self, ai_depth)
        RulesEnforcer.__init__(self)
        #super(ChessGame, self).__init__()

        self.ai_depth = ai_depth
        
        #initialize the chessboard
        self.chessboard = [["0-0"]*8 for i in range(8)]
        
        """Track aspects of the game"""
        #track which pieces have been taken
        self.white_taken = []
        self.black_taken = []
        
        #track which moves have been made in the game, key: move number, value: len 2 list of white and black move
        self.moves_made = {}
        
        #track the number of moves made
        self.move_count = 0
        
        #track whose turn it is (white always starts)
        self.current_turn = "w"
        
        #create pawns
        for i in range(8):
            self.chessboard[1][i] = 'b-p'
            self.chessboard[6][i] = 'w-p'
        
        #create rooks
        self.chessboard[0][0] = 'b-r'
        self.chessboard[0][7] = 'b-r'
        self.chessboard[7][0] = 'w-r'
        self.chessboard[7][7] = 'w-r'
        
        #create knights
        self.chessboard[0][1] = 'b-n'
        self.chessboard[0][6] = 'b-n'
        self.chessboard[7][1] = 'w-n'
        self.chessboard[7][6] = 'w-n'
        
        #create bishops
        self.chessboard[0][2] = 'b-b'
        self.chessboard[0][5] = 'b-b'
        self.chessboard[7][2] = 'w-b'
        self.chessboard[7][5] = 'w-b'
        
        #create queen and king
        self.chessboard[0][3] = 'b-q'
        self.chessboard[0][4] = 'b-k'
        self.chessboard[7][3] = 'w-q'
        self.chessboard[7][4] = 'w-k'

        self.game_over = False
            
    def see_board(self):
        """see the current state of the chessboard"""
        for i in self.chessboard:
            print(i)

    
    def whose_turn(self):
        #print(self.current_turn + " to move")
        return self.current_turn

    
    def recommend_move(self, depth_override = None):
        """
        Use the AI to recommend a move (will not actually make the move)
        """
        if not depth_override:
            depth_override = self.ai_depth

        self.tree_generator(depth_override)
        return self.minimax(self.current_game_state, 0)

    def make_move_ai(self, depth_override = None):
        """
        Let the AI make the move
        """
        if not depth_override:
            depth_override = self.ai_depth

        myoutput = self.recommend_move(depth_override)
        start  = myoutput[2]
        finish = myoutput[3]

        self.make_move(start, finish)
        print(start)
        print(finish)

        return self.chessboard


    def make_move(self, start, finish):
        """
        Make a move
        
        input:
        starting coordinate: example "e4"
        ending coordinate: example "e5"
        
        output:
        "Move success" or "Move invalid", self.chessboard is updated with the move made
        
        Uses the RulesEnforcer() to make sure that the move is valid
        
        """
        
        #map start and finish to gameboard coordinates
        start  = RulesEnforcer.coordinate_mapper(start)
        finish = RulesEnforcer.coordinate_mapper(finish)
        
        #need to move alot of this logic to the rules enforcer
        start_cor0  = start[0]
        start_cor1  = start[1]
        
        finish_cor0 = finish[0]
        finish_cor1 = finish[1]
        
        #check if destination is white, black or empty
        start_color = self.chessboard[start_cor0][start_cor1].split('-')[0]
        start_piece = self.chessboard[start_cor0][start_cor1].split('-')[1]
        
        #check if destination is white, black or empty
        destination_color = self.chessboard[finish_cor0][finish_cor1].split('-')[0]
        destination_piece = self.chessboard[finish_cor0][finish_cor1].split('-')[1]
        
        #cannot move if starting square is empty
        if start_color == '0':
            return "Starting square is empty!"
        
        #cannot move the other person's piece
        if self.current_turn != start_color:
            return "Cannot move the other person's piece!"
        
        #cannot take your own piece 
        if self.current_turn == destination_color:
            return "invalid move, cannot take your own piece!"
        elif self.current_turn != destination_color and destination_color != '0':
            if destination_piece == 'k':
                self.game_over = True
                return "game over, " + self.current_turn + " has won"
            elif self.current_turn == 'w':
                self.black_taken.append(destination_piece)
            elif self.current_turn == 'b':
                self.white_taken.append(destination_piece)     
        else:
            pass
        
        mypiece = self.chessboard[start_cor0][start_cor1]
        self.chessboard[start_cor0][start_cor1] = '0-0'
        self.chessboard[finish_cor0][finish_cor1] = mypiece
        
        #if the move is a success, change the turn state
        if self.current_turn == "w":
            self.current_turn = "b"
        elif self.current_turn == "b":
            self.current_turn = "w"
        
        return self.chessboard


    
    def current_position_score(self):
        """
        Get the position score of the current game being played
        """
        return self.position_evaluator(self.chessboard)


