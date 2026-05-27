from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )
    return names.capitalize()


def render_bar(
    console: Console,
    current_value: int,
    maximum_value: int,
    total_width: int,
    bar_bg: Tuple[int, int, int],
    bar_fg: Tuple[int, int, int],
    text_color: Tuple[int, int, int],
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=bar_bg)

    if bar_width > 0:
        console.draw_rect(x=0, y=45, width=bar_width, height=1, ch=1, bg=bar_fg)

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=text_color
    )


def render_names_at_mouse_location(console: Console, engine: Engine) -> None:
    mouse_x, mouse_y = engine.mouse_location
    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )
    console.print(x=mouse_x + 1, y=mouse_y - 1, string=names_at_mouse_location)
