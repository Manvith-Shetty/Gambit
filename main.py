import chess
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from chess import Board
import chess.pgn
import chess.svg

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def documentation(request: Request):
    return templates.TemplateResponse(
        request=request, name="doc.html"
    )


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


@app.get("/pgn-to-board")
async def pgn_to_board():
    """
        Analyzes a Chess game in Portable Game Notation (PGN) format and returns final position along with outcome.
        Returns:
            dict: A dictionary containing the board representation as a 2D list of the game along with the result.
        """
    try:

        pgn = open("./data/pgn/fisher.pgn")
        game = chess.pgn.read_game(pgn)
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
        fen = board.fen()
        return {await fen_to_board(fen), game.headers["Result"]}
    except ValueError:
        return {"error": "Invalid pgn"}
