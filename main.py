"""Main entry point into the game"""

from chessgame import ChessGame

if __name__ == '__main__':
	current_game = ChessGame(5)
	current_game.see_board()