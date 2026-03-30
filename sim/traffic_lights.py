import os
import pygame
from config import TRAFFIC_LIGHT_POS

from sim.map import MAP_HEIGHT, MAP_WIDTH
from sim.world import World


# Load the test map and light sprites.
def load_assets(assets_dir):
    # Tiny script for checking the map and lights.
    bg_path = os.path.join(assets_dir, "map.png")
    map_img = pygame.image.load(bg_path).convert()
    
    ns_light = pygame.image.load(os.path.join(assets_dir, "ns_traffic_base.png")).convert_alpha()
    ew_light = pygame.image.load(os.path.join(assets_dir, "ew_traffic_base.png")).convert_alpha()
    
    ns_mini = pygame.transform.scale(ns_light, (450, 300))
    ew_mini = pygame.transform.scale(ew_light, (450, 300))
    
    return map_img, ns_mini, ew_mini


# Run a tiny visual test window.
def main():
    # Only a quick visual check, not the full app.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")

    pygame.init()
    screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
    pygame.display.set_caption("Traffic Light Test")

    map_img, ns_light_mini, ew_light_mini = load_assets(assets_dir)

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
        for tl in TRAFFIC_LIGHT_POS:
            pos = tl.get("pos", tl["center"])
            if tl["axis"] == "NS":
                screen.blit(ns_light_mini, pos)
            else:
                screen.blit(ew_light_mini, pos)

        for v in world.vehicles:
            rect = pygame.Rect(v["x"], v["y"], 20, 40)
            pygame.draw.rect(screen, (0, 0, 255), rect)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
