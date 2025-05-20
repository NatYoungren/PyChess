
from chess.tiles.tile import Tile
from utils.chess_types import TileType

from chess.tiles.floor import FloorTile
from chess.tiles.void import VoidTile
from chess.tiles.wall import WallTile
from chess.tiles.chasm import ChasmTile

piece_classes = {
    TileType.VOID: VoidTile,
    TileType.FLOOR: FloorTile,
    TileType.WALL: WallTile,
    TileType.CHASM: ChasmTile,
    
    TileType.DEFAULT: Tile,

}

def get_tile_class(tile_type: TileType):
    tc = piece_classes.get(tile_type, None)
    if tc is None:
        print(f"Tile type {tile_type} not found in tile_classes.")
        print(f"Defaulting to Tile.")
        tc = Tile
    return tc
