import pygame as pg
import numpy as np
from typing import Optional, Union, Tuple


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
