

import pygame as pg
from typing import Dict, List, Union, Tuple, Callable, Optional


from utils.ui_utils import HEADER_FONT, STANDARD_FONT, THIN_FONT
from utils.ui_utils import render_text, sprite_transform
from utils.chess_types import Position, Vector, Loyalty

from utils.ui_utils import UIClickable, UIRegion

from utils.asset_loader import asset_loader as al

class ButtonsUI(UIRegion):
    """
    UI for buttons at the bottom of the sidebar.
    """
    ui: object
    scale: int # TODO: Remove?

    # [Normal, Hover/Click]
    pause_sprites: Tuple[pg.Surface, pg.Surface]
    play_sprites: Tuple[pg.Surface, pg.Surface]

    undo_sprites: Tuple[pg.Surface, pg.Surface]
    settings_sprites: Tuple[pg.Surface, pg.Surface]
    
    # map_sprites: Tuple[pg.Surface, pg.Surface]
    # quit_sprites: Tuple[pg.Surface, pg.Surface]
    
    def __init__(self,
                 ui,
                 origin: Position = (0, 0),
                 size: Vector = (0, 0),
                 scale: int = 2, # TODO: Remove?
                 ):
        # Determine size based on scaled button dimensions?
        super().__init__(origin, size)
        self.ui = ui
        self.scale: int = scale

        # Sprites
        ui_icons = al.icon_sprites['ui']
        self.pause_sprites: Tuple[pg.Surface, pg.Surface] = tuple(sprite_transform(s, size=self.size[1]) for s in ui_icons['pause'])
        self.play_sprites: Tuple[pg.Surface, pg.Surface] = tuple(sprite_transform(s, size=self.size[1]) for s in ui_icons['play'])
        self.undo_sprites: Tuple[pg.Surface, pg.Surface] = tuple(sprite_transform(s, size=self.size[1]) for s in ui_icons['undo'])
        self.settings_sprites: Tuple[pg.Surface, pg.Surface] = tuple(sprite_transform(s, size=self.size[1]) for s in ui_icons['settings'])
        # self.map_sprites: Tuple[pg.Surface, pg.Surface] = al.icon_sprites['map']
        # self.quit_sprites: Tuple[pg.Surface, pg.Surface] = al.icon_sprites['quit']
        
        #        
        padding = 8
        self.pauseB, x = self.make_button(sprite=(self.pause_sprites[0], self.play_sprites[0]),
                                          hsprite=(self.pause_sprites[1], self.play_sprites[1]),
                                          callback=self.pause_callback,
                                          x=self.origin[0] + padding)
        
        self.undoB, x = self.make_button(sprite=self.undo_sprites[0],
                                         hsprite=self.undo_sprites[1],
                                         callback=self.undo_callback,
                                         x=x + padding)
        
        self.settingsB, x = self.make_button(sprite=self.settings_sprites[0],
                                         hsprite=self.settings_sprites[1],
                                         callback=self.settings_callback,
                                         x=x + padding)
        
        # self.mapB, x = self.make_button(self.map_sprites[0],
        #                                     self.map_callback,
        #                                     x=x + padding)
        # self.quitB, x = self.make_button(self.quit_sprites[0],
        #                                     self.quit_callback,
        #                                     x=x + padding)
        
        
    # TODO:
    #       Map button
    #       Quit button
    def make_button(self,
                    sprite: Union[pg.Surface, Tuple[pg.Surface, ...]],
                    hsprite: Union[None, pg.Surface, Tuple[pg.Surface, ...]],
                    callback: Callable,
                    x: int,
                    y: Optional[int] = None,
                    add_clickable: bool = True) -> Tuple[UIClickable, int]:
        size = sprite.get_size() if isinstance(sprite, pg.Surface) else sprite[0].get_size()
        btn = UIClickable(origin=self.origin + (x, y if y is not None else 0),
                          size=size,
                          sprite=sprite,
                          hsprite=hsprite,
                          callback=callback)
        x = btn.origin[0] + btn.size[0]
        if add_clickable:
            self.add_clickable(btn)
        return btn, x
    
    def pause_callback(self, btn: UIClickable): # Remove?
        print('Pause button clicked')
        btn._callback = self.play_callback
        btn._sprite_idx = 1
        # Switch to play?
    
    def play_callback(self, btn: UIClickable): # TODO: Remove? Play button may be in menu.
        print('Play button clicked')
        btn._callback = self.pause_callback
        btn._sprite_idx = 0
        # Switch to pause?
    
    def settings_callback(self, btn: UIClickable):
        print('Settings button clicked')
        # btn._sprite_idx = (btn._sprite_idx + 1) % len(btn.sprites)
        # Open settings menu?
    
    # TODO: CREATE SPRITE
    def quit_callback(self, btn: UIClickable):
        print('Quit button clicked')
        # Quit game?
    
    def undo_callback(self, btn: UIClickable):
        print('Undo button clicked')
        # btn._sprite_idx = (btn._sprite_idx + 1) % len(btn.sprites)
        # Undo last move?


# class FactionIconClickable(UIClickable):
#     """
#     Clickable for a faction icon in the turn order.
#     """
#     turn_pointer_sprite: pg.Surface
    
#     def __init__(self, origin: Position, size: Vector,
#                  sprite: Union[pg.Surface, Tuple[pg.Surface, ...]],
#                  hsprite: Union[None, pg.Surface, Tuple[pg.Surface, ...]],
#                  faction: Loyalty,
#                  callback: Callable = lambda _: None):
#         super().__init__(origin, size, sprite=sprite, hsprite=hsprite, callback=callback)
#         self.faction = faction  # Faction this clickable represents
        

class TurnOrderUI(UIRegion):
    ui: object
    scale: int # TODO: Remove?

    _faction_clickables: Dict[Loyalty, UIClickable] # Faction name -> clickable
    _selected_faction: Loyalty = Loyalty.NONE  # Faction currently selected (for info display)

    turn_pointer_sprite: pg.Surface
    under_indicator: pg.Surface # TODO: Remove? Used for turn pointer?
    over_indicator: pg.Surface # TODO: Remove? Used for turn pointer?
    right_indicator: pg.Surface # TODO: Remove? Used for turn pointer?
    
    
    def __init__(self,
                 ui,
                 origin: Position,
                 size: Vector,
                 scale: int, # TODO: Remove?
                 ):
        
        # TODO: Use or remove size?
        super().__init__(origin, size)
        self.ui = ui
        self.scale: int = scale
        
        turn_order_text = render_text('Turn Order', THIN_FONT, scale=self.scale)
        to_clickable = UIClickable(self.origin+(0, 0), turn_order_text.get_size(), turn_order_text)
        self.add_clickable(to_clickable)
        
        self._faction_clickables: Dict[Loyalty, UIClickable] = {}
        self._selected_faction = Loyalty.NONE  # Faction currently selected (for info display)
        self.turn_pointer_sprite = sprite_transform(al.indicator_sprites['turn'], size=(32 * self.scale, 32 * self.scale))
        self.under_indicator = sprite_transform(al.indicator_sprites['under'], size=(32 * self.scale, 32 * self.scale))
        self.over_indicator = sprite_transform(al.indicator_sprites['over'], size=(32 * self.scale, 32 * self.scale))
        self.right_indicator = sprite_transform(al.indicator_sprites['right'], size=(32 * self.scale, 32 * self.scale))

    def draw(self, surf: pg.Surface, hovered: Optional[UIClickable] = None):
        """
        Draw the turn order UI region.
        """
        
        super().draw(surf, hovered=hovered)
        self.draw_indicators(surf, hovered=hovered)

        # TODO: Display faction info:
        # Show info for hovered faction, default to current faction?
        # OR allow click-to-select.
        #       - Faction name
        #       - Faction 'direction'
        #       - Pieces taken
        #       - Pieces remaining
        #       - Misc information / morale / leadership / objectives?
        #       - Information about bot priorities / decisionmaking?
        #           - (The kings nephew was recently knighted, he will be protected at all costs.)


    def draw_indicators(self, surf: pg.Surface, hovered: Optional[UIClickable] = None):
        """
        Draw indicators for factions in the turn order.
        """
        # hf = hovered in self._faction_clickables.values()
        for i, (l, cl) in enumerate(self._faction_clickables.items()):
            if l is self.ui.board.current_turn:
                cl._sprite_idx = 1  # Highlight current faction
                # Draw turn pointer for current faction
                over_pos = (cl.origin[0] + cl.size[0] // 2 - self.over_indicator.get_width() // 2,
                            cl.origin[1]-4*self.scale)# - self.over_indicator.get_height())
                under_pos = (cl.origin[0] + cl.size[0] // 2 - self.under_indicator.get_width() // 2,
                             cl.origin[1]+4*self.scale)# - self.under_indicator.get_height())
                surf.blit(self.under_indicator, under_pos)
                surf.blit(self.over_indicator, over_pos)
                # pointer_pos = (cl.origin[0] + cl.size[0] // 2 - self.turn_pointer_sprite.get_width() // 2,
                #                cl.origin[1] - self.turn_pointer_sprite.get_height())
                # surf.blit(self.turn_pointer_sprite, pointer_pos)
            else:
                pass
                cl._sprite_idx = 0
                
            if i != len(self._faction_clickables) - 1:
                right_pos = (cl.origin[0] + cl.size[0] // 2 - self.right_indicator.get_width() // 2 + 4*self.scale,
                        cl.origin[1] + cl.size[1] // 2 - self.right_indicator.get_height() // 2)
                surf.blit(self.right_indicator, right_pos)

        
    def reset_faction_icons(self):
        """
        Update the factions displayed in the turn order.
        """

        # TODO: Use faction UI regions?
        for _, cl in self._faction_clickables.items():
            if cl in self.clickables:
                self.clickables.remove(cl)
        self._faction_clickables.clear()
        # self._faction_backgrounds = al.icon_sprites['faction']['bg'] # Background sprites for factions
        
        # TODO: Display horizontally
        #       Evenly spaced
        #       Use icons.
        
        factions = self.ui.board.turn_order
        if not factions: return
        curr_faction = self.ui.board.current_turn
        
        w = self.size[0]
        px_per_faction = w // len(factions) if factions else 0
        
        x = self.origin[0]# + (w - px_per_faction * len(factions)) # Start at right edge of sidebar
        y = self.origin[1] + 32

        icon_size = 32 * self.scale # TODO: Use UI scale / resolution
        padding = (px_per_faction - icon_size) // 2
        
        # print(w, padding, px_per_faction, icon_size)

        faction_sprites = al.icon_sprites['faction']
        bg = faction_sprites['bg']
        bgselect = faction_sprites['bgselect']
        
        # TODO: Skip NONE faction?
        #       Shrink or skip 'auto' faction icons?
        # skip_factions = (Loyalty.NONE, Loyalty.WHITE_AUTO, Loyalty.BLACK_AUTO)
        
        x -= padding // 2
        for faction in factions:
            
            # Get sprite which represents faction
            faction_sprite = sprite_transform(faction_sprites[faction], size=icon_size)

            # Apply to unselected + hover backgrounds
            _unselected = sprite_transform(bg[0], size=icon_size)
            _unselected.blit(faction_sprite, (0, 0))
            _unselected_h = sprite_transform(bg[1], size=icon_size)
            _unselected_h.blit(faction_sprite, (0, 0))
            
            # Apply to selected + hover backgrounds
            _selected = sprite_transform(bgselect[0], size=icon_size)
            _selected.blit(faction_sprite, (0, 0))
            _selected_h = sprite_transform(bgselect[1], size=icon_size)
            _selected_h.blit(faction_sprite, (0, 0))
            
            # sprite = render_text(faction.name, THIN_FONT, scale=self.scale)
            
            x += padding
            f_clickable = UIClickable((x, y), faction_sprite.get_size(),
                                      sprite=(_unselected, _selected),
                                      hsprite=(_unselected_h, _selected_h),)
            x += faction_sprite.get_size()[0] + padding

            
            self.add_clickable(f_clickable)
            self._faction_clickables[faction] = f_clickable

class LeftSidebar(UIRegion):
    """
    Sidebar which displays summative game information.
    """
    ui: object
    scale: int # TODO: Remove?
        
    def __init__(self,
                 ui,
                 battle_name: str = 'Brinan Courtyard', # TODO: Rework, location name?
                 scale: int = 2, # TODO: Remove?
                 ):
        origin = (0, 0)
        size = (ui.b_origin[0], ui.height)
        
        super().__init__(origin, size)
        self.ui = ui
        self.scale: int = scale
        
        # TODO: Does this need to be a clickable? (Map link??)
        battle_title = render_text(battle_name, HEADER_FONT, scale=self.scale)
        bt_clickable = UIClickable(self.origin + (8, 8), battle_title.get_size(), battle_title)
        self.add_clickable(bt_clickable)
        
        # Buttons at bottom of sidebar
        # TODO: Anchor to bottom left corner
        buttonsui_origin = (0, self.size[1] - 64) # TODO: Padding?
        buttonsui_size = (self.size[0] - buttonsui_origin[0],
                          self.size[1] - buttonsui_origin[1]) # TODO: Padding?
        
        self.buttons_ui = ButtonsUI(ui,
                                   self.origin + buttonsui_origin,
                                   buttonsui_size,
                                   scale=self.scale)
        
        # Turn order between title and buttons
        # TODO: Anchor to center left side of board (or window?)
        turnorderui_origin = (8, 64)
        turnorder_ui_size = (self.size[0] - turnorderui_origin[0],
                             buttonsui_origin[1] - turnorderui_origin[1]) # Padding?
        
        self.turn_order_ui = TurnOrderUI(ui,
                                         self.origin + turnorderui_origin,
                                         turnorder_ui_size,
                                         scale=self.scale)
        
        self.add_clickable(self.turn_order_ui)
        self.add_clickable(self.buttons_ui)
        
        self.reset_turn_order_ui()  # Initialize faction clickables
    
    def update_turn(self):
        """
        Update indicator for current faction.
        """
        pass
        # self.turn_order_ui.update_factions()
    
    def reset_turn_order_ui(self):
        """
        Reset the turn order region.
        """
        self.turn_order_ui.reset_faction_icons()

    # def draw(self, surf):
    #     self.ui.surf.blit(self.text_surf, self.origin)
    
    # @property
    # def origin(self):
    #     return (0, 0)
    
    # @property
    # def size(self): # Extend to board edge and bottom of window
    #     # TODO: Use standard dimensions for simplicity?
    #     return (self.ui.b_origin[0], self.ui.height)
