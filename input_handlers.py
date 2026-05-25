from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, BumpAction, EscapeAction

if TYPE_CHECKING:
    from engine import Engine


class EventHandler:
    def __init__(self, engine: Engine):
        self.engine = engine

    def dispatch(self, event: tcod.event.Event) -> Optional[Action]:
        """
        Takes the raw event and routes it to the correct method.
        This replaces the functionality of the deprecated base class.
        """
        match event:
            case tcod.event.Quit():
                return self.ev_quit()
            case tcod.event.KeyDown():
                return self.ev_keydown(event)
            case _:
                return None

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

    def ev_quit(self):
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        player = self.engine.player

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.K:
            action = BumpAction(player, dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.J:
            action = BumpAction(player, dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.H:
            action = BumpAction(player, dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.L:
            action = BumpAction(player, dx=1, dy=0)
        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(player)

        return action
