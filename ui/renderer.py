<<<<<<< HEAD
# ui/renderer.py
=======
>>>>>>> master
import pygame
from .assets import Assets
from config import TRAFFIC_LIGHT_POS
from traffic.phases import ALL_RED, EW_GREEN, EW_YELLOW, NS_GREEN, NS_YELLOW
from dataclasses import dataclass

@dataclass(frozen=True)
<<<<<<< HEAD
=======
# This just keeps one light position and axis.
>>>>>>> master
class TrafficLightSprite:
    pos: tuple[int, int]
    axis: str

<<<<<<< HEAD
def default_traffic_lights():
    return [
        TrafficLightSprite(
            pos=tl["center"],
            axis=tl["axis"],
        )
        for tl in TRAFFIC_LIGHT_POS
    ]

def render_frame(
    screen,
    assets,
    font,
    world,
    phase,
    queue_ns=0,
    queue_ew=0,
    traffic_lights=None,
):
    # Queue args are kept for compatibility with the Game draw call.
    _ = (queue_ns, queue_ew)
    if traffic_lights is None: traffic_lights = default_traffic_lights()
    screen.blit(assets.map_img, (0, 0))


    # Люди
    for p in getattr(world, "pedestrians", []):
        view = "ns" if p.direction in "NS" else ("we" if p.direction == "W" else "ew")
        sprite = assets.pedestrian_sprites.get(f"{p.variant}_{view}")
        if sprite: screen.blit(sprite, sprite.get_rect(center=(int(p.position[0]), int(p.position[1]))))

    # Машины
    for v in sorted(getattr(world, "vehicles", []), key=lambda x: x.get("y", 0)):
=======
# Turn config light data into sprite objects.
def default_traffic_lights():
    # Turn config data into tiny render-friendly objects.
    return [TrafficLightSprite(pos=tl["center"], axis=tl["axis"]) for tl in TRAFFIC_LIGHT_POS]

# Draw one full simulation frame.
def render_frame(screen, assets, font, world, phase, queue_ns=0, queue_ew=0, traffic_lights=None):
    if traffic_lights is None:
        traffic_lights = default_traffic_lights()
        
    # Draw in layers so objects stack the right way.
    screen.blit(assets.map_img, (0, 0))

    for p in world.pedestrians:
        view = "ns" if p.direction in "NS" else ("we" if p.direction == "W" else "ew")
        sprite = assets.pedestrian_sprites.get(f"{p.variant}_{view}")
        if sprite: 
            screen.blit(sprite, sprite.get_rect(center=(int(p.position[0]), int(p.position[1]))))

    for v in sorted(world.vehicles, key=lambda x: x.get("y", 0)):
>>>>>>> master
        sprite = assets.car_sprites.get(v["variant"], assets.car_sprites["grey_car"])
        angle = {"N": 180, "S": 0, "E": 90, "W": -90}.get(v["direction"], 0)
        rot = pygame.transform.rotate(sprite, angle)
        screen.blit(rot, rot.get_rect(center=(int(v["x"]), int(v["y"]))))

<<<<<<< HEAD
   # Светофоры
    for tl in traffic_lights:
        color = "red"
        if phase != ALL_RED:
            if tl.axis == "NS": color = "green" if phase == NS_GREEN else ("yellow" if phase == NS_YELLOW else "red")
            else: color = "green" if phase == EW_GREEN else ("yellow" if phase == EW_YELLOW else "red")
        img = getattr(assets, f"{'ns' if tl.axis == 'NS' else 'ew'}_traffic_light_{color}")
        screen.blit(img, tl.pos)
=======
    for tl in traffic_lights:
        color = "red"
        if phase != ALL_RED:
            if tl.axis == "NS": 
                color = "green" if phase == NS_GREEN else ("yellow" if phase == NS_YELLOW else "red")
            else: 
                color = "green" if phase == EW_GREEN else ("yellow" if phase == EW_YELLOW else "red")
                
        img = getattr(assets, f"{'ns' if tl.axis == 'NS' else 'ew'}_traffic_light_{color}")
        screen.blit(img, tl.pos)
>>>>>>> master
