from typing import Optional

import tcod.event

from actions import Action, BumpAction, EscapeAction


class EventHandler:
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

        if key == tcod.event.KeySym.UP:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT:
            action = BumpAction(dx=1, dy=0)
        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        return action
