"""Main entry point into the game"""

from chessgame import ChessGame

if __name__ == '__main__':

    current_game = ChessGame(3)
    print("Lets play chess!!! Here is the board:\n")
    current_game.see_board()
    print('\n')

    while not current_game.game_over:
        print("Your turn: ")
        start_point = raw_input("Enter starting point coordinate: ")
        end_point = raw_input("Enter ending point coordinate: ")
        current_game.make_move(start_point,end_point)
        print("You have made a move!\n")
        current_game.see_board()
        print('\n')
        
        if current_game.current_turn == 'b':
            print("AI is thinking...")
            current_game.make_move_ai(3)
            print('AI has made a move!\n\n')
            current_game.see_board()
            print('\n')