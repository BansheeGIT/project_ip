# ui/renderer.py
import pygame
from .assets import Assets
from traffic.phases import ALL_RED, EW_GREEN, EW_YELLOW, NS_GREEN, NS_YELLOW
from dataclasses import dataclass

@dataclass(frozen=True)
class TrafficLightSprite:
    pos: tuple[int, int]
    axis: str

def default_traffic_lights():
    return [TrafficLightSprite((820, 400), "EW"), TrafficLightSprite((1100, 680), "NS")]

def render_frame(screen, assets, font, world, phase, q_ns, q_ew, traffic_lights=None):
    if traffic_lights is None: traffic_lights = default_traffic_lights()
    screen.blit(assets.map_img, (0, 0))

    # Светофоры
    for tl in traffic_lights:
        color = "red"
        if phase != ALL_RED:
            if tl.axis == "NS": color = "green" if phase == NS_GREEN else ("yellow" if phase == NS_YELLOW else "red")
            else: color = "green" if phase == EW_GREEN else ("yellow" if phase == EW_YELLOW else "red")
        img = getattr(assets, f"{'ns' if tl.axis == 'NS' else 'ew'}_traffic_light_{color}")
        screen.blit(img, tl.pos)

    # Люди
    for p in getattr(world, "pedestrians", []):
        view = "ns" if p.direction in "NS" else ("we" if p.direction == "W" else "ew")
        sprite = assets.pedestrian_sprites.get(f"{p.variant}_{view}")
        if sprite: screen.blit(sprite, sprite.get_rect(center=(int(p.position[0]), int(p.position[1]))))

    # Машины
    for v in sorted(getattr(world, "vehicles", []), key=lambda x: x.get("y", 0)):
        sprite = assets.car_sprites.get(v["variant"], assets.car_sprites["grey_car"])
        angle = {"N": 180, "S": 0, "E": 90, "W": -90}.get(v["direction"], 0)
        rot = pygame.transform.rotate(sprite, angle)
        screen.blit(rot, rot.get_rect(center=(int(v["x"]), int(v["y"]))))