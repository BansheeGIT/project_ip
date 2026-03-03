from __future__ import annotations
# Signed changes: Abdil

from collections.abc import Callable
import pygame


Color = tuple[int, int, int]

# Shared palette used by the right-side simulation control panel. - Abdil
PANEL_BG_COLOR: Color = (17, 26, 36)
PANEL_BORDER_COLOR: Color = (70, 92, 114)
SECTION_COLOR: Color = (173, 204, 233)
TEXT_COLOR: Color = (241, 248, 255)


def draw_panel_background(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draws the side panel shell."""
    pygame.draw.rect(surface, PANEL_BG_COLOR, rect)
    # Left border visually separates panel from map viewport. - Abdil
    pygame.draw.line(surface, PANEL_BORDER_COLOR, rect.topleft, rect.bottomleft, 2)


class Button:
    """Small clickable rectangular control for in-panel actions."""

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

    def set_label(self, value: str) -> None:
        self.label = value

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Returns True when this button consumed the event."""
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()
                return True
        return False

    def draw(self, surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None) -> None:
        """Render with hover and disabled states."""
        # Optional mouse_pos lets caller pass logical coordinates for scaled rendering. - Abdil
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


class Slider:
    """Horizontal drag slider with numeric readout."""

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

    def _ratio(self) -> float:
        """Normalize current value to 0..1 for rendering."""
        value_span = self.max_value - self.min_value
        if value_span <= 0:
            return 0.0
        return (self.value - self.min_value) / value_span

    def _x_from_value(self) -> int:
        return int(self.track_rect.left + self._ratio() * self.track_rect.width)

    def _value_from_x(self, x_pos: int) -> float:
        """Convert cursor x-position on the track into slider value."""
        x_pos = max(self.track_rect.left, min(self.track_rect.right, x_pos))
        ratio = (x_pos - self.track_rect.left) / self.track_rect.width
        return self.min_value + ratio * (self.max_value - self.min_value)

    def _set_from_x(self, x_pos: int) -> None:
        self.value = self._value_from_x(x_pos)

    def _knob_rect(self) -> pygame.Rect:
        x = self._x_from_value()
        y = self.track_rect.centery
        return pygame.Rect(
            x - self.knob_radius,
            y - self.knob_radius,
            self.knob_radius * 2,
            self.knob_radius * 2,
        )

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Returns True when slider consumed the event."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.track_rect.collidepoint(event.pos) or self._knob_rect().collidepoint(event.pos):
                self.dragging = True
                self._set_from_x(event.pos[0])
                return True
            return False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            self._set_from_x(event.pos[0])
            return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            return True

        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Render label, inactive/active track, and draggable knob."""
        value_text = f"{self.value:.{self.precision}f}{self.suffix}"
        title = self.font.render(f"{self.label}: {value_text}", True, TEXT_COLOR)
        surface.blit(title, (self.track_rect.left, self.track_rect.top - 30))

        pygame.draw.line(
            surface,
            (85, 110, 138),
            (self.track_rect.left, self.track_rect.centery),
            (self.track_rect.right, self.track_rect.centery),
            5,
        )

        fill_end_x = self._x_from_value()
        pygame.draw.line(
            surface,
            (119, 178, 230),
            (self.track_rect.left, self.track_rect.centery),
            (fill_end_x, self.track_rect.centery),
            5,
        )

        knob_color = (220, 238, 255) if self.dragging else (187, 220, 252)
        pygame.draw.circle(surface, knob_color, (fill_end_x, self.track_rect.centery), self.knob_radius)
        pygame.draw.circle(surface, (34, 46, 60), (fill_end_x, self.track_rect.centery), self.knob_radius, 2)
