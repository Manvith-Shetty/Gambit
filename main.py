import chess
from fastapi import FastAPI
from chess import Board

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Robert James Fisher is the Greatest of All Time"}


@app.post("/fen-to-board")
async def fen_to_board(fen: str):
    """
    Converts a FEN string to a chess board representation. Args: fen (str): The FEN string representing the
    chessboard position. Returns: dict: A dictionary containing the board representation as a 2D list, or an error
    message if the FEN string is invalid.
    """
    try:
        board = chess.Board(fen)
        board_representation = []
        for rank in range(8, 0, -1):
            row = []
            for file in range(ord('a'), ord('h') + 1):
                square = chess.parse_square(chr(file) + str(rank))
                piece = board.piece_at(square)
                row.append(piece.symbol() if piece else "-")
            board_representation.append(row)
        return {"board": board_representation}
    except ValueError:
        return {"error": "Invalid FEN string"}
