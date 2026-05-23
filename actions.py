from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action(ABC):
    @abstractmethod
    def perform(self, engine: Engine, entity: Entity):
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

         This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity):
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is not in bounds

        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is not walkable

        entity.move(self.dx, self.dy)
