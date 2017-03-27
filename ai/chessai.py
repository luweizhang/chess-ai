"""chess ai"""
import math
import itertools

class TreeNode(object):
    """Tree data structure for storing possible chess positions"""
    def __init__(self, data, parent=None):
        self.data = data
        self.children = []
        
    def add_child(self, data):
        self.children.append(child)

class ChessAi(object):
    #set the value of each of the pieces to be used in the hard coded heuristic algorithm
    piece_values = {'p':1,'r':5,'n':3,'b':3,'q':9,'k':99}
    
    def __init__(self, ai_depth = 1):
        """
        input: ai_diff is the difficulty level of the ai (integer from 1 to 10)
        """
        self.depth = ai_depth
    
    @staticmethod
    def position_evaluator(chess_position):
        """
        Heuristic algorithm that evaluates a chess position
        
        First version of this will most likely be a hard coded heuristic algorithm, 
        But will try to use convolutional neural network trained off of millions of chess games...
        
        input: a chess_position (8 x 8 2d array), such as self.chessboard
        output: a float representing how good the position is 
        (positive score means white is winning, negative score means that black is winning)
        
        Heuristic algorithm example:
        position_score = sum_of_pieces + king_castled? + pawn_islands? + free_bishops? + forward_knights?
        
        developed pieces:
        forward kxnights
        forward pawn (more likely to castle)
        pawn islands (these are bad)
        bishops with open diagonals

        iterate through the entire chessboard and calculate the optimum value.
        """

        #sum up all material by iterating through the entire chessboard
        final_position_score = 0
        
        #iterate through every row on the chessboard and calculate heuristics adjustment 
        #for the first iteration of this, I will look for developed pieces
        for x, row in enumerate(chess_position):
            for y, j in enumerate(row):
                color = j.split('-')[0]
                piece = j.split('-')[1]
                
                #sum up the value of all the pieces
                if color == 'w':
                    final_position_score += ChessAi.piece_values[piece]
                elif color == 'b':
                    final_position_score -= ChessAi.piece_values[piece]

                #score adjustment for forward pawn (plus .1 for each square that the pawn is advanced)
                if piece == 'p' and color == 'w':
                    final_position_score += (8 - y - 2)*.1 
                if piece == 'p' and color == 'b':
                    final_position_score -= (y - 1)*.1 
                    
                #score adjustment for developed knights (plus .1 for each square that the knight is advanced)
                if piece == 'n' and color == 'w':
                    final_position_score += math.pow(1 + (8 - y - 1)*.1, 2)
                if piece == 'n' and color == 'b':
                    final_position_score -= math.pow(1 + (y)*.1, 2)
                    
                #score adjustment for bishops with open diagonals
                #score adjustment for castled king                
        return round(final_position_score, 4)
       

    def tree_generator(self):
        """
        Brute force tree generation.  Generates all possible moves (will probably need to add pruning later) 
        
        input: current chess position (8 x 8 2d array)
        output: a large tree of chess position
        
        My Notes:
        We should be able to use the position_evaluator to prune and make the tree generation smarter...
        
        Tree generation needs to be done carefully, if we just generate trees based on all possible moves, 
        the size of the tree can easily explode.
        
        For example, just assuming that we have around 20 possible moves at each turn, after around 6 moves the size
        of the tree explodes to 64 million moves (20^6).  This is crazy!
        
        If I can somehow narrow down the tree search to about 5 moves per tree, 
        then the size of the tree can be drastically reduced, 
        and I could possible compute 10 moves into the future without running out of memory 
        or taking up too much CPU power.
        I guess after the second move, I don't really need to store the position in the tree, I can just store the score...
        
        For the first iteration, just calculate three moves into the fiture

        """
        
        self.gametree = TreeNode(self.chessboard)

        #returns a list of possible chess positions, and the actual move itself
        pos_moves = possible_moves(gametree.data)
        
        #run the heuristic algorithm on the list of possible moves you can make to narrow down your search space.  
        #hmm...the problem with this is that unless the heuristic algorithm is very good
        #you might miss out on really good moves such as a queen sacrifice...I'm not sure what to do here...
        #pos_evaluated is an array of ints representing the quality of the moves e.g. [3,4,5,6,4]
        pos_evaluated = []
        for i in pos_moves:
            pos_evaluated.append(position_evaluator(i))
        num_iter = min(8, len(pos_evaluated))
        
        #add top 8 possible moves as children of the tree.
        for i in range(num_iter):
            pos_score = pos_evaluated[i]
            move = pos_moves[i] 
            mytree.add_child([pos_score, move])        
        
    
    def minimax(self):
        """Minimax algorithm to find the best moves at each layer of the tree
        
        Takes as input a tree of moves and uses minimax to find the best within in that tree.  
        Will use the heuristic algorithm to evaluate the chess moves.   
        
        Basically start at the leaf nodes of the tree and backwards compute back to the original
        
        input: a tree of possible moves (created by the tree generator function)
        output: the best move to make at the current state (str)
        
        """
        pass


   