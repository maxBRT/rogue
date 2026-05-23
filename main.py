import tcod

from engine import Engine
import game_map
from input_handlers import EventHandler
from entity import Entity
from game_map import GameMap


def main() -> None:
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    tileset = tcod.tileset.load_tilesheet("ascii.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    event_handler = EventHandler()
    player = Entity(screen_width // 2, screen_height // 2, "@", (255, 255, 255))
    npc = Entity(screen_width // 2 - 5, screen_height // 2 - 5, "@", (255, 255, 0))
    entites = {npc, player}
    game_map = GameMap(map_width, map_height)
    engine = Engine(entites, event_handler, game_map, player)

    with tcod.context.new(
        width=screen_width,
        height=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            engine.handle_events(tcod.event.wait())


if __name__ == "__main__":
    main()
