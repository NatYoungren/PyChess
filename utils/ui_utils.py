import pygame as pg
import numpy as np
from typing import Optional, Union, Tuple, Dict, List, Callable, Self

from utils.chess_types import Position, Vector


pg.font.init()
MHEADER_FONT = pg.font.Font("assets/fonts/merlin-16x16-monospaced.ttf", 16)
MSTANDARD_FONT = pg.font.Font("assets/fonts/merlin-8x8-monospaced.ttf", 8)
MTHIN_FONT = pg.font.Font("assets/fonts/merlin-light-8x8-monospaced.ttf", 8)

HEADER_FONT = pg.font.Font("assets/fonts/merlin-16x16.ttf", 16)
STANDARD_FONT = pg.font.Font("assets/fonts/merlin-8x8.ttf", 8)
THIN_FONT = pg.font.Font("assets/fonts/merlin-light-8x8.ttf", 8)



def sprite_transform(img: pg.Surface,
                     randomflip: bool = False,
                     randomrotate: bool = False,
                     rotate_by: Optional[int] = None,
                     size: Union[None, int, Tuple[int, int]] = None) -> pg.Surface:
    """
    Transform a sprite to the given size (optionally flipped or rotated).
    """
    if randomflip: img = pg.transform.flip(img, *np.random.randint(0, 2, 2))
    if randomrotate:
        img = pg.transform.rotate(img, np.random.randint(0, 4)*90)
    
    elif isinstance(rotate_by, (int, np.int64)):
        img = pg.transform.rotate(img, rotate_by*90)
        
    if size is not None:
        if isinstance(size, (int, np.int64)):
            size = (size, size)
        img = pg.transform.scale(img, size)
    
    return img
