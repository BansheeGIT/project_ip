from __future__ import annotations

from collections.abc import Callable
import pygame

Color = tuple[int, int, int]

PANEL_BG_COLOR: Color = (17, 26, 36)
PANEL_BORDER_COLOR: Color = (70, 92, 114)
SECTION_COLOR: Color = (173, 204, 233)
TEXT_COLOR: Color = (241, 248, 255)

# Fill the panel background.
def draw_panel_background(surface: pygame.Surface, rect: pygame.Rect) -> None:
    # Simple panel shell behind the buttons and stats.
    pygame.draw.rect(surface, PANEL_BG_COLOR, rect)
    pygame.draw.line(surface, PANEL_BORDER_COLOR, rect.topleft, rect.bottomleft, 2)

# This class is one clickable button.
class Button:
    # Button only handles clicks and drawing. The callback does the real work.
    # Store button text, size, and click action.
    def __init__(
        self,
        rect: tuple[int, int, int, int],
        label: str,
        font: pygame.font.Font,
        on_click: Callable[[], None],
        base_color: Color = (54, 86, 116),
        hover_color: Color = (74, 112, 148),
        text_color: Color = TEXT_COLOR,
    ) -> None:
        self.rect = pygame.Rect(rect)
        self.label = label
        self.font = font
        self.on_click = on_click
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.enabled = True

    # Change the text shown on the button.
    def set_label(self, value: str) -> None:
            self.label = value
            
    # Handle one mouse click.
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()
                return True
        return False

    # Draw the button and its hover state.
    def draw(self, surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None) -> None:
        pointer = mouse_pos if mouse_pos is not None else pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(pointer)
        
        color = self.hover_color if mouse_over and self.enabled else self.base_color
        if not self.enabled:
            color = (95, 95, 95)

        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (22, 33, 45), self.rect, width=2, border_radius=8)

        label = self.font.render(self.label, True, self.text_color)
        text_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, text_rect)

# This class is one horizontal slider.
class Slider:
    # Slider maps mouse x-position into a value range.
    # Hold the range and the current value.
    def __init__(
        self,
        rect: tuple[int, int, int, int],
        label: str,
        min_value: float,
        max_value: float,
        value: float,
        font: pygame.font.Font,
        precision: int = 2,
        suffix: str = "",
    ) -> None:
        self.track_rect = pygame.Rect(rect)
        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.value = max(min_value, min(max_value, value))
        self.font = font
        self.precision = precision
        self.suffix = suffix
        self.dragging = False
        self.knob_radius = 10

    # Turn the current value into a 0..1 ratio.
    def _ratio(self) -> float:
        value_span = self.max_value - self.min_value
        return 0.0 if value_span <= 0 else (self.value - self.min_value) / value_span

    # Convert the current value into an x-position.
    def _x_from_value(self) -> int:
        return int(self.track_rect.left + self._ratio() * self.track_rect.width)

    # Update the slider value from one x-position.
    def _set_from_x(self, x_pos: int) -> None:
        # Clamp first so dragging outside the bar still feels okay.
        x_pos = max(self.track_rect.left, min(self.track_rect.right, x_pos))
        ratio = (x_pos - self.track_rect.left) / self.track_rect.width
        self.value = self.min_value + ratio * (self.max_value - self.min_value)

    # Small rect used for dragging the knob.
    def _knob_rect(self) -> pygame.Rect:
        x = self._x_from_value()
        y = self.track_rect.centery
        return pygame.Rect(x - self.knob_radius, y - self.knob_radius, self.knob_radius * 2, self.knob_radius * 2)

    # Handle click, drag, and release.
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.track_rect.collidepoint(event.pos) or self._knob_rect().collidepoint(event.pos):
                self.dragging = True
                self._set_from_x(event.pos[0])
                return True

        if event.type == pygame.MOUSEMOTION and self.dragging:
            self._set_from_x(event.pos[0])
            return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            return True

        return False

    # Render the bar, fill, and knob.
    def draw(self, surface: pygame.Surface) -> None:
        value_text = f"{self.value:.{self.precision}f}{self.suffix}"
        title = self.font.render(f"{self.label}: {value_text}", True, TEXT_COLOR)
        surface.blit(title, (self.track_rect.left, self.track_rect.top - 30))

        pygame.draw.line(
            surface, (85, 110, 138),
            (self.track_rect.left, self.track_rect.centery),
            (self.track_rect.right, self.track_rect.centery), 5
        )

        fill_end_x = self._x_from_value()
        pygame.draw.line(
            surface, (119, 178, 230),
            (self.track_rect.left, self.track_rect.centery),
            (fill_end_x, self.track_rect.centery), 5
        )

        knob_color = (220, 238, 255) if self.dragging else (187, 220, 252)
        pygame.draw.circle(surface, knob_color, (fill_end_x, self.track_rect.centery), self.knob_radius)
        pygame.draw.circle(surface, (34, 46, 60), (fill_end_x, self.track_rect.centery), self.knob_radius, 2)
