<<<<<<< HEAD
# ui/cursor_overlay.py - Abdil
# Signed changes: Abdil
=======
>>>>>>> master
from __future__ import annotations
import pygame


<<<<<<< HEAD
class CursorOverlay:
    """
    Debug overlay inside main simulation window:
    - F3 toggles on/off
    - LMB stores last click
    - shows cursor coords + last click label near cursor
    """

=======
# Show mouse and click positions on top of the screen.
class CursorOverlay:
    # Remember the overlay state and font.
>>>>>>> master
    def __init__(self, enabled: bool = True, font_size: int = 18) -> None:
        self.enabled = enabled
        self.last_click: tuple[int, int] | None = None
        self._font = pygame.font.SysFont("consolas", font_size)

<<<<<<< HEAD
    def handle_event(self, event: pygame.event.Event) -> None:
=======
    # Handle F3 and left clicks.
    def handle_event(self, event: pygame.event.Event) -> None:
        # F3 turns this helper on and off.
>>>>>>> master
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
            self.enabled = not self.enabled
            return

        if not self.enabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
<<<<<<< HEAD
            self.last_click = event.pos
            print(f"[CURSOR] click={self.last_click}")

=======
            # Remember the last click so map coords are easy to read.
            self.last_click = event.pos

    # Draw the live cursor text and the last click mark.
>>>>>>> master
    def draw(self, screen: pygame.Surface, mouse_pos: tuple[int, int] | None = None) -> None:
        if not self.enabled:
            return

        w, h = screen.get_size()
<<<<<<< HEAD
        # Optional mouse_pos lets caller pass logical coordinates when rendering is scaled. - Abdil
        mx, my = mouse_pos if mouse_pos is not None else pygame.mouse.get_pos()

        # Top-left cursor label - Abdil
=======
        mx, my = mouse_pos if mouse_pos is not None else pygame.mouse.get_pos()

>>>>>>> master
        cursor_text = f"cursor=({mx}, {my})  [F3 toggle]"
        label = self._font.render(cursor_text, True, (255, 255, 255))
        bg = pygame.Surface((label.get_width() + 10, label.get_height() + 8))
        bg.set_alpha(160)
        bg.fill((0, 0, 0))
        screen.blit(bg, (8, 8))
        screen.blit(label, (13, 12))

        if self.last_click is None:
            return

        x, y = self.last_click

<<<<<<< HEAD
        # Marker - Abdil
=======
>>>>>>> master
        pygame.draw.circle(screen, (255, 60, 60), (x, y), 6, 2)
        pygame.draw.line(screen, (255, 60, 60), (x - 8, y), (x + 8, y), 2)
        pygame.draw.line(screen, (255, 60, 60), (x, y - 8), (x, y + 8), 2)

<<<<<<< HEAD
        # Label near cursor (not at click, so it's always readable) - Abdil
=======
>>>>>>> master
        text = f"click=({x}, {y})"
        t = self._font.render(text, True, (255, 255, 0))

        lx, ly = mx + 14, my + 14
<<<<<<< HEAD
        if lx + t.get_width() > w:
            lx = mx - 14 - t.get_width()
        if ly + t.get_height() > h:
            ly = my - 14 - t.get_height()
=======
        if lx + t.get_width() > w: lx = mx - 14 - t.get_width()
        if ly + t.get_height() > h: ly = my - 14 - t.get_height()
>>>>>>> master

        bg2 = pygame.Surface((t.get_width() + 10, t.get_height() + 8))
        bg2.set_alpha(160)
        bg2.fill((0, 0, 0))
        screen.blit(bg2, (lx - 5, ly - 4))
        screen.blit(t, (lx, ly))
