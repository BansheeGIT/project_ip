from __future__ import annotations
import os
from dataclasses import dataclass, field
import pygame

@dataclass(frozen=True)
# Keep all loaded images in one bundle.
class Assets:
    map_img: pygame.Surface
    ns_traffic_light_red: pygame.Surface
    ns_traffic_light_yellow: pygame.Surface
    ns_traffic_light_green: pygame.Surface
    ew_traffic_light_red: pygame.Surface
    ew_traffic_light_yellow: pygame.Surface
    ew_traffic_light_green: pygame.Surface
    car_sprites: dict[str, pygame.Surface] = field(default_factory=dict)
    pedestrian_sprites: dict[str, pygame.Surface] = field(default_factory=dict)

# Try to load one image without knowing if it is png or jpg.
def _load_img(path_without_ext: str) -> pygame.Surface | None:
    # Try png first, then jpg.
    if os.path.exists(path_without_ext + ".png"):
        return pygame.image.load(path_without_ext + ".png").convert_alpha()
    if os.path.exists(path_without_ext + ".jpg"):
        return pygame.image.load(path_without_ext + ".jpg").convert_alpha()
    return None

# Resize one surface to the needed size.
def _scale(img: pygame.Surface, size: tuple[int, int]) -> pygame.Surface:
    return pygame.transform.scale(img, size)

# Load every image the renderer needs.
def load_assets(project_dir: str, map_size: tuple[int, int]) -> Assets:
    assets_dir = os.path.join(project_dir, "sim", "assets")
    width, height = map_size

    car_variants = ["grey_car", "red_car", "blue_car", "green_car", "light_blue car", "pink_car", "purple_car", "ambulance"]
    car_sprites = {}

    # If a sprite is missing, fall back to a simple safe default.
    default_car = _load_img(os.path.join(assets_dir, "grey_car"))
    if not default_car:
        default_car = pygame.Surface((50, 95))
        default_car.fill((150, 150, 150))

    for var in car_variants:
        size = (75, 95) if var == "ambulance" else (50, 95)
        img = _load_img(os.path.join(assets_dir, var))
        car_sprites[var] = _scale(img if img else default_car, size)

    ped_size = (90, 135)
    ped_variants = ["ped1", "ped2", "ped3", "ped4"]
    ped_views = ["ns", "ew", "we"]
    pedestrian_sprites = {}

    # Build one default pedestrian view for each direction.
    default_peds = {}
    for view in ped_views:
        img = _load_img(os.path.join(assets_dir, f"ped1_{view}"))
        if not img:
            img = pygame.Surface(ped_size)
            img.fill((200, 200, 200))
        default_peds[view] = img

    for var in ped_variants:
        for view in ped_views:
            img = _load_img(os.path.join(assets_dir, f"{var}_{view}"))
            pedestrian_sprites[f"{var}_{view}"] = _scale(img if img else default_peds[view], ped_size)

    # Load one map or light image, with a plain fallback block.
    def load_base(name, size):
        # Use a plain block if the image file is missing.
        img = _load_img(os.path.join(assets_dir, name))
        if img: return _scale(img, size)
        s = pygame.Surface(size)
        s.fill((50, 50, 50))
        return s

    return Assets(
        map_img=load_base("map", (width, height)),
        ns_traffic_light_red=load_base("ns_traffic_red", (450, 300)),
        ns_traffic_light_yellow=load_base("ns_traffic_yellow", (450, 300)),
        ns_traffic_light_green=load_base("ns_traffic_green", (450, 300)),
        ew_traffic_light_red=load_base("ew_traffic_base_red", (450, 300)),
        ew_traffic_light_yellow=load_base("ew_traffic_base_yellow", (450, 300)),
        ew_traffic_light_green=load_base("ew_traffic_base_green", (450, 300)),
        car_sprites=car_sprites,
        pedestrian_sprites=pedestrian_sprites
    )
