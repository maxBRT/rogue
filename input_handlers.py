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

    def ev_quit(self):
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.K:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.J:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.H:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.L:
            action = BumpAction(dx=1, dy=0)
        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        return action
