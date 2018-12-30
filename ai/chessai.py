"""chess ai"""
import math
import itertools
import copy

#import from parent directory
from game import RulesEnforcer

"""
Contains the method necessary for the Chess AI to work
"""

class TreeNode(object):
    """Tree data structure for storing possible chess positions

    self.data:
        len 2 array that contains the chess position and the evaluation score.
    """
    def __init__(self, data, parent=None):
        self.data = data
        self.children = []
        
    def add_child(self, data):
        self.children.append(TreeNode(data))

    def see_children(self):
        for i in self.children:
            print i.data

class ChessAi(object):
    #set the value of each of the pieces to be used in the hard coded heuristic algorithm
    piece_values = {'p':1,'r':5,'n':3,'b':3,'q':9,'k':99}
    
    def __init__(self, ai_depth = 3):
        """
        input: ai_depth is amount of moves to search into the future.

        in the future, we can try to add different parameter constrains 
        # such as time limit, cpu compute speed.
        """
        self.depth = ai_depth
        self.current_game_state = None
    
    @staticmethod
    def position_evaluator(chess_position):
        """
        Heuristic algorithm that evaluates a chess position
        
        First version of this will most likely be a hard coded heuristic algorithm, 
        But will try to use convolutional neural network trained off of millions of chess games...
        
        input: a chess_position (8 x 8 2d array), such as self.chessboard
        output: a float representing how good the position is 
        (positive score means white is winning, negative score means that black is winning)
        
        Example of a possible heuristic algorithm:
        position_score = sum_of_pieces + king_castled? + pawn_islands? + free_bishops? + forward_knights?
        
        developed pieces:
        forward knights
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
                    final_position_score += (8 - x - 2)*.02 
                if piece == 'p' and color == 'b':
                    final_position_score -= (x - 1)*.02
                    
                #score adjustment for developed knights (plus .1 for each square that the knight is advanced)
                if piece == 'n' and color == 'w':
                    final_position_score += math.pow(1 + (8 - x - 1)*.05, 2)
                    #penalize for knights on the sides of the board
                    if j == 0 or j == 7:
                        final_position_score -= .1

                if piece == 'n' and color == 'b':
                    final_position_score -= math.pow(1 + (x)*.05, 2)
                    #penalize for knights on the sides of the board
                    if j == 0 or j == 7:
                        final_position_score -= .1

                #score adjustment for bishops with open diagonals
                if piece == 'b' and color == 'w':
                    #check for open diagonals
                    new_row = x - 1
                    new_col = y + 1
                    while new_row >= 0 and new_col <= 7:
                        square = chess_position[x][y]
                        #add points for open diagonals
                        if square == '0-0':
                            final_position_score += .05
                            new_row -= 1
                            new_col += 1
                            continue
                        elif piece.split('-')[0] == 'b':
                            final_position_score += .25
                            break
                        elif piece.split('-')[0] == 'w':
                            break

                if piece == 'b' and color == 'w':
                    #check for open diagonals
                    new_row = x - 1
                    new_col = y - 1
                    while new_row >= 0 and new_col >= 0:
                        square = chess_position[x][y]
                        #add points for open diagonals
                        if square == '0-0':
                            final_position_score += .05
                            new_row -= 1
                            new_col -= 1
                            continue
                        elif piece.split('-')[0] == 'b':
                            final_position_score += .25
                            break
                        elif piece.split('-')[0] == 'w':
                            break

                #score adjustment for bishops with open diagonals
                if piece == 'b' and color == 'b':
                    #check for open diagonals
                    new_row = x + 1
                    new_col = y + 1
                    while new_row <= 7 and new_col <= 7:
                        square = chess_position[x][y]
                        #add points for open diagonals
                        if square == '0-0':
                            final_position_score += .05
                            new_row -= 1
                            new_col += 1
                            continue
                        elif piece.split('-')[0] == 'w':
                            final_position_score += .25
                            break
                        elif piece.split('-')[0] == 'b':
                            break

                if piece == 'b' and color == 'b':
                    #check for open diagonals
                    new_row = x + 1
                    new_col = y - 1
                    while new_row <= 7 and new_col >= 0:
                        square = chess_position[x][y]
                        #add points for open diagonals
                        if square == '0-0':
                            final_position_score += .05
                            new_row -= 1
                            new_col -= 1
                            continue
                        elif piece.split('-')[0] == 'w':
                            final_position_score += .25
                            break
                        elif piece.split('-')[0] == 'b':
                            break

                #ideas for more heuristics / features    
                #score adjustment for castled king, protected king in early and mid game, 
                #developed king in late game
                #score adjustment for open lane for rook
                #score adjustment for queen with open lanes
                #score adjustment for strong pawn structure


        return round(final_position_score, 4)
       

    def tree_generator(self, depth_override = None):
        """
        Brute force tree generation.  Generates all possible moves (will probably need to add pruning later) 
        
        input: current chess position (8 x 8 2d array)
        output: returns nothing but sets the current game state at self.current_game_state
        
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
        
        For the first iteration, just calculate three moves into the future

        """

        #first, lets try to look one move into the future.  Then we will expand the AI to look more moves into the future 

        #initialize the tree by putting the current state into the parent node of the chessboard. 
        self.current_game_state = TreeNode([copy.deepcopy(self.chessboard),0])
        current_positions = [self.current_game_state]

        #track the number of moves into the future you are calculating.
        current_depth = 1

        #override the target depth if depth is explicitly defined
        target_depth = depth_override or self.depth

        #get the current turn
        current_turn = copy.copy(self.current_turn)

        #keep searching until the desired AI depth has been reached. 
        while current_depth <= target_depth:
            for position in current_positions:
                #returns a dictionary of possible chess moves
                pos_moves = RulesEnforcer.all_possible_moves(position.data[0], current_turn)

                #now we need to generate all possible moves in the future...
                #we will do this by iterating through the pos moves dictionary
                for start, moves in pos_moves.items():
                    for move in moves:
                        current_pos = position.data[0]
                        new_pos = ChessAi.make_hypothetical_move(start, move, current_pos)

                        if current_turn == 'w':
                            score = ChessAi.position_evaluator(new_pos)
                        else:
                            #if black, store the negative score because black wants to play the best move
                            score = -ChessAi.position_evaluator(new_pos)

                        if current_depth > 1:
                            position.add_child([new_pos, score])
                        else:
                            position.add_child([new_pos, score, start, move])

            current_depth += 1

            #now, populate the new current positions list
            new_positions = []
            for position in current_positions:
                new_positions += position.children
            current_positions = new_positions

            #now, switch the turn
            if current_turn == 'w':
                current_turn = 'b' 
            else:
                current_turn = 'w' 



        #run the heuristic algorithm on the list of possible moves you can make to narrow down your search space.  
        #hmm...the problem with this is that unless the heuristic algorithm is very good
        #you might miss out on really good moves such as a queen sacrifice...I'm not sure what to do here...
        #pos_evaluated is an array of ints representing the quality of the moves e.g. [3,4,5,6,4]
        
        """
        pos_evaluated = []
        for i in pos_moves:
            pos_evaluated.append(position_evaluator(i))
        num_iter = min(8, len(pos_evaluated))
        
        #add top 8 possible moves as children of the tree.
        for i in range(num_iter):
            pos_score = pos_evaluated[i]
            move = pos_moves[i] 
            mytree.add_child([pos_score, move])
        """       
        

    def minimax(self, node, depth = 0):
        """Minimax algorithm to find the best moves at each layer of the tree
        
        Takes as input a tree of moves and uses minimax to find the best within in that tree.  
        Will use the heuristic algorithm to evaluate the chess moves.   
        
        Basically, use recursion to get to the leaf note of th tree
        Then use the minimax algorithm to backwards compute back to the original value.
        
        input: root/starting node of the possible move tree (created by the tree generator function)
        output: the best move to make at the current state (str)
        """

        #current player wants to maximize the score.
        #opponent wants to minimize the score.

        #current_turn = copy.copy(self.current_turn)
        scores = []

        #if children of children exist, that means you need to go one level deeper
        if node.children[0].children:
            for child in node.children:
                scores.append(self.minimax(child, depth + 1))
            #if its your turn, do max
            if depth % 2 == 0:
                #finally, when you get back to the root node, output the optimal move
                if depth == 0:
                    if self.current_turn == 'w':
                        return node.children[scores.index(max(scores))].data + [max(scores)]
                    elif self.current_turn == 'b':
                        #show the negative score for black to avoid confusion
                        myresult = node.children[scores.index(max(scores))].data
                        myresult[1] = -myresult[1]
                        return myresult + [-max(scores)]

                else:
                    return max(scores)          
            #if its the opponents turn, do min
            else:
                return min(scores)

        else:
            #if no children of children exist, then it is time to apply the minimax algorithm
            for child in node.children:
                scores.append(child.data[1])

            #if its your turn, do max
            if depth % 2 == 0:
                max_scores = max(scores)
                #store in the max or min score so you know how the chess engine evaluates the position
                self.future_position_score = max(scores)
                return max_scores
            #if its the opponents turn, do min
            else:
                min_scores = min(scores)
                #store in the max or min score so you know how the chess engine evaluates the position
                self.future_position_score = min(scores)
                return min_scores

    @staticmethod
    def make_hypothetical_move(start, finish, chessboard):
        """
        Make a hypothetical move, this will be used to generate the possibilities to be
        stored in the chess tree

        This method has a ton of redundant code with the make_move() method 
        so I should probably 
        
        input:
        starting coordinate: example "e4"
        ending coordinate: example "e5"
        chessboard: chessboard that you want to move
        
        output:
        "Move success" or "Move invalid"
        
        Uses the RulesEnforcer() to make sure that the move is valid
        
        """
        #deepcopy the chessboard so that it does not affect the original
        mychessboard = copy.deepcopy(chessboard[:])
        
        #map start and finish to gameboard coordinates
        start  = RulesEnforcer.coordinate_mapper(start)
        finish = RulesEnforcer.coordinate_mapper(finish)
        
        #need to move alot of this logic to the rules enforcer
        start_cor0  = start[0]
        start_cor1  = start[1]
        
        finish_cor0 = finish[0]
        finish_cor1 = finish[1]
        
        #check if destination is white, black or empty
        start_color = mychessboard[start_cor0][start_cor1].split('-')[0]
        start_piece = mychessboard[start_cor0][start_cor1].split('-')[1]
        
        #check if destination is white, black or empty
        destination_color = mychessboard[finish_cor0][finish_cor1].split('-')[0]
        destination_piece = mychessboard[finish_cor0][finish_cor1].split('-')[1]
        
        #cannot move if starting square is empty
        if start_color == '0':
            return "Starting square is empty!"
        
        mypiece = mychessboard[start_cor0][start_cor1]
        mychessboard[start_cor0][start_cor1] = '0-0'
        mychessboard[finish_cor0][finish_cor1] = mypiece
        
        return mychessboard


   