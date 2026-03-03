from __future__ import annotations

import os
import sys

import pygame

try:
    from .map import MAP_HEIGHT, MAP_WIDTH
    from .world import World
except ImportError:
    # Allow running this file directly as a script.
    from map import MAP_HEIGHT, MAP_WIDTH
    from world import World


def _load_assets(assets_dir: str):
    bg_path = os.path.join(assets_dir, "map.png")
    map_img = pygame.image.load(bg_path).convert()
    ns_traffic_light = pygame.image.load(
        os.path.join(assets_dir, "ns_traffic_base.png")
    ).convert_alpha()
    ew_traffic_light = pygame.image.load(
        os.path.join(assets_dir, "ew_traffic_base.png")
    ).convert_alpha()
    ns_light_mini = pygame.transform.scale(ns_traffic_light, (450, 300))
    ew_light_mini = pygame.transform.scale(ew_traffic_light, (450, 300))
    return map_img, ns_light_mini, ew_light_mini


def main() -> int:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")

    pygame.init()
    screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
    pygame.display.set_caption("Smart Traffic Light Simulation")

    try:
        map_img, ns_light_mini, ew_light_mini = _load_assets(assets_dir)
    except FileNotFoundError as exc:
        print(f"Missing asset: {exc}")
        pygame.quit()
        return 1

    traffic_lights_pos = [
        (600, 450),
        (870, 150),
    ]

    world = World()
    world.spawn_vehicle(direction="N", x=920, y=0, speed=200)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                world.spawn_vehicle(direction="N", x=920, y=0, speed=300)

        world.step(dt)

        screen.blit(map_img, (0, 0))
        for pos in traffic_lights_pos:
            if pos == (600, 450):
                screen.blit(ns_light_mini, pos)
            else:
                screen.blit(ew_light_mini, pos)

        for v in world.vehicles:
            rect = pygame.Rect(v["x"], v["y"], 20, 40)
            pygame.draw.rect(screen, (0, 0, 255), rect)

        pygame.display.update()

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
