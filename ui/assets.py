# ui/assets.py
from __future__ import annotations
import os
from dataclasses import dataclass, field
import pygame

@dataclass(frozen=True)
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

def _load_and_scale(path: str, size: tuple[int, int]) -> pygame.Surface:
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except Exception:
        s = pygame.Surface(size)
        s.fill((255, 0, 255)) 
        return s

def load_assets(project_dir: str, map_size: tuple[int, int]) -> Assets:
    assets_dir = os.path.join(project_dir, "sim", "assets")
    width, height = map_size

    car_variants = ["grey_car", "red_car", "blue_car", "green_car", "light_blue car", "pink_car", "purple_car", "ambulance"]
    car_sprites = {var: _load_and_scale(os.path.join(assets_dir, f"{var}.png"), 
                   (75, 95) if var == "ambulance" else (50, 95)) for var in car_variants}

    # Увеличенный размер для пешеходов
    ped_size = (90, 135)
    ped_variants = ["ped1", "ped2", "ped3", "ped4"]
    ped_views = ["ns", "ew", "we"]
    pedestrian_sprites = {}

    for var in ped_variants:
        for view in ped_views:
            base_path = os.path.join(assets_dir, f"{var}_{view}")
            
            if os.path.exists(base_path + ".png"):
                path = base_path + ".png"
            elif os.path.exists(base_path + ".jpg"):
                path = base_path + ".jpg"
            else:
                # Защита от розовых квадратов (берем ped1 как запасной)
                fallback_path = os.path.join(assets_dir, f"ped1_{view}")
                if os.path.exists(fallback_path + ".png"):
                    path = fallback_path + ".png"
                elif os.path.exists(fallback_path + ".jpg"):
                    path = fallback_path + ".jpg"
                else:
                    path = base_path + ".png"

            pedestrian_sprites[f"{var}_{view}"] = _load_and_scale(path, ped_size)

    return Assets(
        map_img=_load_and_scale(os.path.join(assets_dir, "map.png"), (width, height)),
        ns_traffic_light_red=_load_and_scale(os.path.join(assets_dir, "ns_traffic_red.png"), (450, 300)),
        ns_traffic_light_yellow=_load_and_scale(os.path.join(assets_dir, "ns_traffic_yellow.png"), (450, 300)),
        ns_traffic_light_green=_load_and_scale(os.path.join(assets_dir, "ns_traffic_green.png"), (450, 300)),
        ew_traffic_light_red=_load_and_scale(os.path.join(assets_dir, "ew_traffic_base_red.png"), (450, 300)),
        ew_traffic_light_yellow=_load_and_scale(os.path.join(assets_dir, "ew_traffic_base_yellow.png"), (450, 300)),
        ew_traffic_light_green=_load_and_scale(os.path.join(assets_dir, "ew_traffic_base_green.png"), (450, 300)),
        car_sprites=car_sprites,
        pedestrian_sprites=pedestrian_sprites
    )
