import copy
import tcod
import colors

from engine import Engine
import entities_factories
from procgen import generate_dungeon
import traceback

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50


def main() -> None:

    map_width = 80
    map_height = 45
    room_max_size = 10
    room_min_size = 6
    max_monster_per_room = 2
    max_item_per_room = 2
    max_rooms = 30

    tileset = tcod.tileset.load_tilesheet("ascii.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    player = copy.deepcopy(entities_factories.player)
    engine = Engine(player)
    engine.gamemap = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        max_monster_per_room=max_monster_per_room,
        max_item_per_room=max_item_per_room,
        map_width=map_width,
        map_height=map_height,
        engine=engine,
    )
    engine.update_fov()
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!",
        colors.welcome_text,
    )

    with tcod.context.new(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            try:
                for event in tcod.event.wait():
                    event = context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:  # Handle exceptions in game.
                traceback.print_exc()  # Print error to stderr.
                # Then print the error to the message log.
                engine.message_log.add_message(traceback.format_exc(), colors.error)


if __name__ == "__main__":
    main()
