import argparse
import chess.pgn
import time

# Function to convert game result to WDL (Win/Draw/Loss) in terms of white
def result_to_wdl(result):
    if result == "1-0":
        return 1.0  # White wins
    elif result == "0-1":
        return 0.0  # White loses
    else:
        return 0.5  # Draw

# Function to play through a game and save FENs and WDLs
def process_pgn(pgn_path, output_file_path):
    games = 0
    startTime = time.time()
    with open(pgn_path) as f:
        with open(output_file_path, "w") as output_file:
            while True:
                games += 1
                if (games % 100 == 0):
                    print(f"Elapsed: \033[91m{int(1000*(time.time() - startTime))}\033[0m Game: \033[94m{games}\033[0m G/s: \033[92m{float(games/(time.time()-startTime))}\033[0m ETA: \033[96m{int(((35918-games)/(games/(time.time()-startTime)))/60)} min\033[0m")
                game = chess.pgn.read_game(f)
                if game is None:
                    break  # No more games in the PGN file

                board = game.board()
                result = game.headers["Result"]
                wdl = result_to_wdl(result)

                moves = list(game.mainline_moves())
                for i, move in enumerate(moves):
                    fen = board.fen()
                    output_file.write(f"{fen} [{wdl}]\n")

                    board.push(move)

                # Save the final position after all moves are played
                final_fen = board.fen()
                output_file.write(f"{final_fen} [{wdl}]\n")

# Main function
def main():
    parser = argparse.ArgumentParser(description='Convert PGN file to FEN format with results.')
    parser.add_argument('--input', '-i', type=str, help='Input PGN file path', required=True)
    parser.add_argument('--output', '-o', type=str, help='Output FEN file path', required=True)
    args = parser.parse_args()

    pgn_path = args.input
    output_file_path = args.output

    process_pgn(pgn_path, output_file_path)

if __name__ == "__main__":
    main()
