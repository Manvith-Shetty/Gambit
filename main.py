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
        board = Board(fen)
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


@app.post("/validate-move")
async def validate_move(fen: str, move: str):
    """
    Validates a chess move on a board represented by a FEN string.
    Args:
        fen (str): The FEN string representing the chessboard position.
        move (str): The chess move in Standard Algebraic Notation (SAN).
    Returns:
        dict: A dictionary containing a "valid" key with a boolean value indicating
               if the move is valid on the board.
    """
    try:
        board = Board(fen)
        move = chess.Move.from_uci(move)
        print(move)
        is_valid = move in board.legal_moves
        return {"valid": is_valid}
    except ValueError:
        return {"valid": False, "error": "Invalid FEN string or move notation"}
