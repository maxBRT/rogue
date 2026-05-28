from typing import TYPE_CHECKING, Tuple

import tcod
from tcod.console import Console
from tcod.map import compute_fov
from input_handlers import MainGameEventHandler
import colors
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location
import exceptions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler


class Engine:
    gamemap: GameMap

    def __init__(
        self,
        player: Actor,
    ):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.player = player
        self.mouse_location: Tuple[int, int] = (0, 0)

    def handle_enemy_turns(self) -> None:
        for entity in set(self.gamemap.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self):
        """Recompute the visible area based on the players point of view."""
        self.gamemap.visible[:] = compute_fov(
            self.gamemap.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
            algorithm=tcod.FOV_SHADOW,
        )

        # If a tile is "visible" it should be added to "explored".
        self.gamemap.explored |= self.gamemap.visible

    def render(self, console: Console) -> None:
        self.gamemap.render(console=console)
        render_bar(
            console,
            self.player.fighter.hp,
            self.player.fighter.max_hp,
            20,
            colors.bar_empty,
            colors.bar_filled,
            colors.bar_text,
        )  # Player HP bar
        self.message_log.render(console=console, x=21, y=45, width=40, height=5)
        render_names_at_mouse_location(console=console, engine=self)
