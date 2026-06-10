"""Command-line interface for Tic Tac Toe."""

from tictactoe.game import Game
from tictactoe.ai import AI


def main() -> None:
    """Run the game loop."""
    print("Welcome to Tic Tac Toe!")
    print("You are X, the computer is O.")
    print("Enter the number of the cell you want to play (1-9).")

    game = Game()
    ai = AI(mark=game.computer_mark, opponent_mark=game.human_mark)

    while not game.is_over():
        print("\n" + game.board.display())

        if game.current_turn == game.human_mark:
            # Human move
            try:
                move = int(input("Your move (1-9): "))
            except ValueError:
                print("Invalid input. Please enter a number 1-9.")
                continue
            if not game.board.is_valid_move(move):
                print("That cell is already taken or out of range. Try again.")
                continue
            game.make_move(move)
        else:
            # Computer move
            print("Computer is thinking...")
            move = ai.get_move(game.board)
            game.make_move(move)
            print(f"Computer plays {move}")

    # Game over
    print("\n" + game.board.display())
    winner = game.board.get_winner()
    if winner == game.human_mark:
        print("Congratulations! You win!")
    elif winner == game.computer_mark:
        print("Computer wins. Try again!")
    else:
        print("It's a draw!")
