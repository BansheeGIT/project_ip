<<<<<<< HEAD
# app/game.py
# Signed changes: Abdil_Super
=======
>>>>>>> master
from __future__ import annotations

import sys
import uuid
import pygame

from mqtt.client import LocalBroker, MqttClient
from mqtt.security import build_fernet_security_from_env
from mqtt.topics import TopicRegistry
from nodes.actuator_node import ActuatorNode
from nodes.controller_node import ControllerNode
from nodes.monitor_node import MonitorNode
from nodes.sensor_node import SensorNode
from sim.world import World
from sim.spawner import Spawner
from sim.metrics import EfficiencyLogger, count_queues
from traffic.controller_logic import TrafficController
from traffic.phases import ALL_RED, EW_GREEN, EW_YELLOW, NS_GREEN, NS_YELLOW

from ui.assets import load_assets
from ui.renderer import render_frame, default_traffic_lights
from ui.cursor_overlay import CursorOverlay
from ui.controls import (
    Button,
    Slider,
    SECTION_COLOR,
    TEXT_COLOR,
    draw_panel_background,
)

<<<<<<< HEAD

class Game:
    # Reserve a fixed side panel for GUI controls and live telemetry.
=======
# Main window and sim loop live here.
class Game:
    # Game ties the simulation, UI, and control mode together.
    # Sizes for the right panel and its small button.
>>>>>>> master
    PANEL_WIDTH = 360
    TOGGLE_W = 28
    TOGGLE_H = 56
    TARGET_FPS = 60
    START_WINDOW_WIDTH = 1280
    START_WINDOW_HEIGHT = 720
    MIN_VIEW_WIDTH = 200
    MIN_WINDOW_HEIGHT = 360

<<<<<<< HEAD
=======
    # Get the window, sim, and side panel ready.
>>>>>>> master
    def __init__(
        self,
        sim_width: int,
        sim_height: int,
        project_dir: str,
        mode: str = "fixed",
        window_width: int = START_WINDOW_WIDTH,
        window_height: int = START_WINDOW_HEIGHT,
    ) -> None:
        pygame.init()
        pygame.font.init()

        self.sim_width = sim_width
        self.sim_height = sim_height
        self.project_dir = project_dir
        self.mode = mode
        self.mqtt_transport = "local"

        self.window_width, self.window_height = self._normalize_window_size(
            window_width, window_height
        )
        self.panel_open = True
        open_x = self.window_width - self.PANEL_WIDTH
        self.panel_x = float(open_x)
        self.panel_target_x = float(open_x)
        self.panel_slide_speed = 900.0

        self.view_width = 0
        self.view_height = 0
        self._recompute_viewport()

        self.font = pygame.font.SysFont("Arial", 24, bold=True)  # In-map status text.
        self.panel_title_font = pygame.font.SysFont("Consolas", 28, bold=True)
        self.panel_font = pygame.font.SysFont("Consolas", 20)
        self.panel_small_font = pygame.font.SysFont("Consolas", 18)

        # Main OS window is always a normal resizable app window.
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.RESIZABLE
        )
        pygame.display.set_caption("Smart Traffic Light - Interactive GUI")

        # Simulation always renders at native map resolution.
        self.sim_surface = pygame.Surface((self.sim_width, self.sim_height)).convert()

        self.assets = load_assets(
            project_dir=project_dir,
            map_size=(self.sim_width, self.sim_height),
        )
        self.traffic_lights = default_traffic_lights()

        self.clock = pygame.time.Clock()
        self.running = True

        # Existing debug overlay remains available (F3).
        self.cursor_overlay = CursorOverlay(enabled=True)

<<<<<<< HEAD
        # Runtime stats shown in the GUI panel.
=======
        # These values are shown in the side panel.
>>>>>>> master
        self.phase = NS_GREEN
        self.queue_ns = 0
        self.queue_ew = 0
        self.paused = False
        self.sim_speed = 1.00
        self.traffic_load = 1.00
        self.sim_time = 0.0

        # Simulation core objects.
        self.world = World()
        self.spawner = Spawner(self.world)
        self.controller = TrafficController()
        self.broker = None
        self.mqtt_client = None
        self.mqtt_security = None
        self.topic_registry = None
        self.sensor_node = None
        self.smart_controller = None
        self.actuator_node = None
        self.monitor_node = None
        self.last_smart_reason = ""
        # Keep baseline spawn rates so "traffic load" can scale from known defaults.
        self.base_spawn_rates = self.spawner.RATES.copy()
        self._setup_control_mode()
        self.logger = EfficiencyLogger(mode=self.mode, project_dir=self.project_dir)

        # Interactive widgets in the side panel.
        self.buttons: list[Button] = []
        self.speed_slider: Slider | None = None
        self.load_slider: Slider | None = None
        self._build_controls()
        self._apply_spawn_rates()

<<<<<<< HEAD
=======
    # Do not let the window get too small.
>>>>>>> master
    def _normalize_window_size(self, width: int, height: int) -> tuple[int, int]:
        min_window_width = self.PANEL_WIDTH + self.MIN_VIEW_WIDTH
        normalized_width = max(min_window_width, int(width))
        normalized_height = max(self.MIN_WINDOW_HEIGHT, int(height))
        return normalized_width, normalized_height

<<<<<<< HEAD
    def _panel_open_x(self) -> float:
        return float(self.window_width - self.PANEL_WIDTH)

    def _panel_closed_x(self) -> float:
        return float(self.window_width)

=======
    # Where the panel sits when it is open.
    def _panel_open_x(self) -> float:
        return float(self.window_width - self.PANEL_WIDTH)

    # Where the panel sits when it is hidden.
    def _panel_closed_x(self) -> float:
        return float(self.window_width)

    # Small hit box for the panel arrow.
>>>>>>> master
    def _toggle_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.window_width - self.TOGGLE_W,
            (self.window_height - self.TOGGLE_H) // 2,
            self.TOGGLE_W,
            self.TOGGLE_H,
        )

<<<<<<< HEAD
=======
    # Recalculate the visible sim area after a size change.
>>>>>>> master
    def _recompute_viewport(self) -> None:
        # Panel is an overlay; simulation viewport always matches full window.
        self.view_width = self.window_width
        self.view_height = self.window_height

<<<<<<< HEAD
=======
    # Resize the window and keep the panel in a sane place.
>>>>>>> master
    def _resize_window(self, width: int, height: int) -> None:
        old_visible_panel_w = max(0, self.window_width - int(self.panel_x))
        self.window_width, self.window_height = self._normalize_window_size(width, height)
        self.panel_target_x = self._panel_open_x() if self.panel_open else self._panel_closed_x()
        self.panel_x = float(self.window_width - old_visible_panel_w)
        self.panel_x = max(self._panel_open_x(), min(self._panel_closed_x(), self.panel_x))
        self._recompute_viewport()
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.RESIZABLE
        )
        self._position_controls(int(self.panel_x))

<<<<<<< HEAD
=======
    # Build all buttons and sliders in the side panel.
>>>>>>> master
    def _build_controls(self) -> None:
        """Create side-panel buttons/sliders and assign callbacks."""
        left = int(self.panel_x) + 16
        full_w = self.PANEL_WIDTH - 32
        button_h = 42
        y = 250

<<<<<<< HEAD
        # Core runtime actions.
=======
        # Main buttons.
>>>>>>> master
        self.run_button = Button(
            rect=(left, y, full_w, button_h),
            label="Pause [Space]",
            font=self.panel_font,
            on_click=self._toggle_pause,
        )
        y += 52
        self.reset_button = Button(
            rect=(left, y, full_w, button_h),
            label="Reset Simulation [R]",
            font=self.panel_font,
            on_click=self._reset_simulation,
        )
        y += 52
        self.phase_button = Button(
            rect=(left, y, full_w, button_h),
            label="Switch Phase [T]",
            font=self.panel_font,
            on_click=self._toggle_phase,
        )
        y += 64

        # Manual spawn controls per inbound direction.
        half = (full_w - 12) // 2
        self.spawn_n = Button(
            rect=(left, y, half, button_h),
            label="Spawn N",
            font=self.panel_small_font,
            on_click=lambda: self._spawn_vehicle("N"),
        )
        self.spawn_s = Button(
            rect=(left + half + 12, y, half, button_h),
            label="Spawn S",
            font=self.panel_small_font,
            on_click=lambda: self._spawn_vehicle("S"),
        )
        y += 52
        self.spawn_w = Button(
            rect=(left, y, half, button_h),
            label="Spawn W",
            font=self.panel_small_font,
            on_click=lambda: self._spawn_vehicle("W"),
        )
        self.spawn_e = Button(
            rect=(left + half + 12, y, half, button_h),
            label="Spawn E",
            font=self.panel_small_font,
            on_click=lambda: self._spawn_vehicle("E"),
        )
        y += 76

        # Real-time simulation tuning.
        self.speed_slider = Slider(
            rect=(left, y, full_w, 8),
            label="Simulation speed",
            min_value=0.25,
            max_value=3.0,
            value=self.sim_speed,
            font=self.panel_small_font,
            precision=2,
            suffix="x",
        )
        y += 78

        # Higher load -> shorter spawn interval -> denser traffic.
        self.load_slider = Slider(
            rect=(left, y, full_w, 8),
            label="Traffic load",
            min_value=0.40,
            max_value=2.50,
            value=self.traffic_load,
            font=self.panel_small_font,
            precision=2,
            suffix="x",
        )

<<<<<<< HEAD
        # Keep a flat list for generic event dispatch and drawing.
=======
        # One list makes event handling easier.
>>>>>>> master
        self.buttons = [
            self.run_button,
            self.reset_button,
            self.phase_button,
            self.spawn_n,
            self.spawn_s,
            self.spawn_w,
            self.spawn_e,
        ]
        self._position_controls(int(self.panel_x))

<<<<<<< HEAD
=======
    # Move controls when the panel slides left or right.
>>>>>>> master
    def _position_controls(self, panel_left_x: int) -> None:
        """Keep panel controls aligned while the panel slides horizontally."""
        if not self.buttons:
            return

        left = panel_left_x + 16
        full_w = self.PANEL_WIDTH - 32
        half = (full_w - 12) // 2

        self.run_button.rect.x = left
        self.reset_button.rect.x = left
        self.phase_button.rect.x = left
        self.spawn_n.rect.x = left
        self.spawn_s.rect.x = left + half + 12
        self.spawn_w.rect.x = left
        self.spawn_e.rect.x = left + half + 12

        if self.speed_slider is not None:
            self.speed_slider.track_rect.x = left
        if self.load_slider is not None:
            self.load_slider.track_rect.x = left

<<<<<<< HEAD
=======
    # Sync the UI phase with the world phase.
>>>>>>> master
    def _set_phase_state(self, phase: str) -> None:
        """Apply chosen phase to both UI state and world light axis."""
        self.phase = phase
        self.world.current_phase = phase
        if phase in (NS_GREEN, NS_YELLOW):
            self.world.green_axis = "NS"
        elif phase in (EW_GREEN, EW_YELLOW):
            self.world.green_axis = "EW"
        else:
            self.world.green_axis = ""

<<<<<<< HEAD
    def _setup_control_mode(self) -> None:
=======
    # Choose smart mode or fixed mode.
    def _setup_control_mode(self) -> None:
        # Smart mode connects MQTT parts. Fixed mode stays local.
>>>>>>> master
        if self.mode == "mqtt-smart":
            run_topic_prefix = f"traffic/sim/{uuid.uuid4().hex[:8]}"
            self.topic_registry = TopicRegistry(prefix=run_topic_prefix)
            self.broker = LocalBroker()
            self.broker.start()

            self.mqtt_security = build_fernet_security_from_env()
            self.mqtt_client = MqttClient(
                self.broker,
                "game-main",
                security=self.mqtt_security,
            )
            self.sensor_node = SensorNode(self.mqtt_client, self.topic_registry)
            self.smart_controller = ControllerNode(self.mqtt_client, self.topic_registry)
            self.actuator_node = ActuatorNode(self.mqtt_client, self.topic_registry)
            self.monitor_node = MonitorNode(self.mqtt_client, self.topic_registry)
            self._set_phase_state(self.smart_controller.current_phase)
        else:
            self.broker = None
            self.mqtt_client = None
            self.mqtt_security = None
            self.topic_registry = None
            self.sensor_node = None
            self.smart_controller = None
            self.actuator_node = None
            self.monitor_node = None
            self._set_phase_state(self.controller.current_phase)

<<<<<<< HEAD
=======
    # Scale car spawn timing from the current traffic load.
>>>>>>> master
    def _apply_spawn_rates(self) -> None:
        """Scale per-direction spawn intervals by the current traffic load."""
        for direction, base_rate in self.base_spawn_rates.items():
            self.spawner.RATES[direction] = base_rate / self.traffic_load

<<<<<<< HEAD
=======
    # Pause or resume the simulation.
>>>>>>> master
    def _toggle_pause(self) -> None:
        """Pause or resume simulation updates."""
        self.paused = not self.paused

<<<<<<< HEAD
=======
    # Reset the world but keep the current UI settings.
>>>>>>> master
    def _reset_simulation(self) -> None:
        """Recreate world/controller state and keep current GUI tuning values."""
        self.logger.close()
        if self.mqtt_client is not None:
            self.mqtt_client.close()
        self.world = World()
        self.spawner = Spawner(self.world)
        self.controller = TrafficController()
        self._apply_spawn_rates()
        self.sim_time = 0.0
        self.queue_ns = 0
        self.queue_ew = 0
        self.last_smart_reason = ""
        self._setup_control_mode()
        self.logger = EfficiencyLogger(mode=self.mode, project_dir=self.project_dir)

<<<<<<< HEAD
=======
    # Manual phase switch for fixed mode.
>>>>>>> master
    def _toggle_phase(self) -> None:
        """Manual override: force the controller to switch traffic phase."""
        if self.mode == "mqtt-smart":
            return
        self.controller.switch_phase()
        self._set_phase_state(self.controller.current_phase)

<<<<<<< HEAD
=======
    # Spawn one car from a chosen direction.
>>>>>>> master
    def _spawn_vehicle(self, direction: str) -> None:
        """Manual vehicle injection for quick scenario testing."""
        self.spawner.spawn_car(direction)

<<<<<<< HEAD
=======
    # Read input events and send them to the right place.
>>>>>>> master
    def handle_events(self) -> None:
        """Route input to widgets, keyboard shortcuts, then optional debug overlay."""
        self._position_controls(int(self.panel_x))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type == pygame.VIDEORESIZE:
                self._resize_window(event.w, event.h)
                continue

            consumed = False

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self._toggle_rect().collidepoint(event.pos)
            ):
                self._toggle_panel()
                consumed = True

            panel_left_x = int(self.panel_x)
            panel_visible = panel_left_x < self.window_width
            panel_rect = pygame.Rect(
                panel_left_x,
                0,
                self.PANEL_WIDTH,
                self.window_height,
            )
            mouse_pos = getattr(event, "pos", None)
            if not consumed and panel_visible and mouse_pos is not None and panel_rect.collidepoint(mouse_pos):
                for button in self.buttons:
                    consumed = button.handle_event(event) or consumed

                if self.speed_slider is not None:
                    consumed = self.speed_slider.handle_event(event) or consumed

                if self.load_slider is not None:
                    consumed = self.load_slider.handle_event(event) or consumed

            if event.type == pygame.KEYDOWN:
                # Keyboard shortcuts mirror primary panel actions.
                if event.key == pygame.K_SPACE:
                    self._toggle_pause()
                    consumed = True
                elif event.key == pygame.K_r:
                    self._reset_simulation()
                    consumed = True
                elif event.key == pygame.K_t:
                    self._toggle_phase()
                    consumed = True

            if not consumed:
                self.cursor_overlay.handle_event(event)

<<<<<<< HEAD
=======
    # Advance one frame of simulation time.
>>>>>>> master
    def update(self, dt: float) -> None:
        """Advance simulation using current panel settings."""
        dx = self.panel_target_x - self.panel_x
        step = self.panel_slide_speed * dt
        if abs(dx) <= step:
            self.panel_x = self.panel_target_x
        elif dx > 0:
            self.panel_x += step
        elif dx < 0:
            self.panel_x -= step

        # Pull current slider values every frame for smooth interaction.
        if self.speed_slider is not None:
            self.sim_speed = self.speed_slider.value
        if self.load_slider is not None and abs(self.load_slider.value - self.traffic_load) > 1e-6:
            self.traffic_load = self.load_slider.value
            self._apply_spawn_rates()

        # Keep displayed queues fresh while paused, but skip world updates.
        if self.paused:
            self.queue_ns, self.queue_ew = count_queues(self.world)
            return

<<<<<<< HEAD
        # Speed slider scales effective simulation time.
        scaled_dt = dt * self.sim_speed
        self.sim_time += scaled_dt

        # Standard simulation pipeline.
        self.spawner.step(scaled_dt)
        self.queue_ns, self.queue_ew = count_queues(self.world)
=======
        # Speed slider makes time go faster or slower.
        scaled_dt = dt * self.sim_speed
        self.sim_time += scaled_dt

        # Usual update order.
        self.spawner.step(scaled_dt)
        self.queue_ns, self.queue_ew = count_queues(self.world)
        # Both modes use the same world. They pick lights in different ways.
>>>>>>> master
        if self.mode == "mqtt-smart":
            self.sensor_node.publish_snapshots(self.world, self.sim_time)
            self.smart_controller.decide(scaled_dt, self.sim_time)
            next_phase = self.actuator_node.current_phase or self.smart_controller.current_phase
            self.last_smart_reason = self.monitor_node.latest_reason()
        else:
            emergency_active, emergency_axis = self.world.compute_preemption_state()
            self.controller.set_preemption(emergency_active, emergency_axis)
            next_phase = self.controller.decide(scaled_dt, self.queue_ns, self.queue_ew)
        self._set_phase_state(next_phase)
        self.world.update_pedestrians(scaled_dt, phase=next_phase)
        self.world.step(scaled_dt)
        self.logger.step(self.world, scaled_dt, self.sim_time)

<<<<<<< HEAD
=======
    # Paint stats, controls, and help text on the right.
>>>>>>> master
    def _draw_panel(self, panel_left_x: int) -> None:
        """Draw side-panel shell, status telemetry, controls, and help text."""
        panel_rect = pygame.Rect(
            panel_left_x,
            0,
            self.PANEL_WIDTH,
            self.window_height,
        )
        draw_panel_background(self.screen, panel_rect)

        title = self.panel_title_font.render("Simulation GUI", True, TEXT_COLOR)
        self.screen.blit(title, (panel_left_x + 20, 18))

        pygame.draw.line(
            self.screen,
            (67, 88, 110),
            (panel_left_x + 20, 56),
            (panel_left_x + self.PANEL_WIDTH - 20, 56),
            2,
        )

        status_header = self.panel_small_font.render("Runtime Status", True, SECTION_COLOR)
        self.screen.blit(status_header, (panel_left_x + 20, 72))

        phase_name = self.phase if self.phase in (
            NS_GREEN,
            NS_YELLOW,
            EW_GREEN,
            EW_YELLOW,
            ALL_RED,
        ) else str(self.phase)
        state_name = "Paused" if self.paused else "Running"
        vehicles = len(self.world.vehicles)
        pedestrians = len(self.world.pedestrians)
        fps = self.clock.get_fps()

        status_lines = [
            f"State: {state_name}",
            f"Mode: {self.mode}",
            "MQTT: local" if self.mode == "mqtt-smart" else "MQTT: off",
            f"Phase: {phase_name}",
            f"Vehicles: {vehicles}",
            f"Pedestrians: {pedestrians}",
            f"Queue NS: {self.queue_ns}",
            f"Queue EW: {self.queue_ew}",
            f"FPS: {fps:.1f}",
            f"Sim Time: {self.sim_time:.1f}s",
        ]
        if self.mode == "mqtt-smart" and self.last_smart_reason:
            status_lines.append(f"Smart reason: {self.last_smart_reason}")
        y = 102
        for line in status_lines:
            text = self.panel_small_font.render(line, True, TEXT_COLOR)
            self.screen.blit(text, (panel_left_x + 22, y))
            y += 22

        controls_header = self.panel_small_font.render("Controls", True, SECTION_COLOR)
        self.screen.blit(controls_header, (panel_left_x + 20, 220))

<<<<<<< HEAD
        # Keep button label synchronized with pause state.
=======
        # Button text changes when pause changes.
>>>>>>> master
        self.run_button.set_label("Resume [Space]" if self.paused else "Pause [Space]")
        for button in self.buttons:
            button.draw(self.screen)

        if self.speed_slider is not None:
            self.speed_slider.draw(self.screen)
        if self.load_slider is not None:
            self.load_slider.draw(self.screen)

        tips = [
            "Tips:",
            "Space = pause/resume",
            "R = reset world",
            "T = force phase switch",
            "F3 = cursor overlay",
        ]
        y = self.window_height - 130
        for i, line in enumerate(tips):
            color = SECTION_COLOR if i == 0 else TEXT_COLOR
            text = self.panel_small_font.render(line, True, color)
            self.screen.blit(text, (panel_left_x + 20, y))
            y += 22

<<<<<<< HEAD
=======
    # Open or close the side panel.
>>>>>>> master
    def _toggle_panel(self) -> None:
        self.panel_open = not self.panel_open
        self.panel_target_x = self._panel_open_x() if self.panel_open else self._panel_closed_x()

<<<<<<< HEAD
=======
    # Draw the little arrow button for the panel.
>>>>>>> master
    def _draw_toggle_button(self) -> None:
        toggle_rect = self._toggle_rect()
        mouse_over = toggle_rect.collidepoint(pygame.mouse.get_pos())
        bg_color = (74, 112, 148) if mouse_over else (54, 86, 116)

        pygame.draw.rect(self.screen, bg_color, toggle_rect, border_radius=10)
        pygame.draw.rect(self.screen, (22, 33, 45), toggle_rect, width=2, border_radius=10)

        cx, cy = toggle_rect.center
        if self.panel_open:
            arrow_points = [(cx - 4, cy - 9), (cx - 4, cy + 9), (cx + 7, cy)]
        else:
            arrow_points = [(cx + 4, cy - 9), (cx + 4, cy + 9), (cx - 7, cy)]
        pygame.draw.polygon(self.screen, TEXT_COLOR, arrow_points)

<<<<<<< HEAD
    def draw(self) -> None:
        # Draw simulation at native resolution, then scale to the full window.
=======
    # Render one frame and show it on screen.
    def draw(self) -> None:
        # Draw on the sim surface first, then scale to the window.
>>>>>>> master
        render_frame(
            screen=self.sim_surface,
            assets=self.assets,
            font=self.font,
            world=self.world,
            phase=self.phase,
            queue_ns=self.queue_ns,
            queue_ew=self.queue_ew,
            traffic_lights=self.traffic_lights,
        )

        scaled_view = pygame.transform.smoothscale(
            self.sim_surface, (self.window_width, self.window_height)
        )
        self.screen.blit(scaled_view, (0, 0))

        panel_left_x = int(self.panel_x)
        self._position_controls(panel_left_x)
        if panel_left_x < self.window_width:
            self._draw_panel(panel_left_x)
        self._draw_toggle_button()
        self.cursor_overlay.draw(self.screen)
        pygame.display.update()

<<<<<<< HEAD
=======
    # Run the main loop until the window closes.
>>>>>>> master
    def run(self) -> None:
        """Main loop: input, update, draw at target FPS."""
        while self.running:
            dt = self.clock.tick(self.TARGET_FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        self.logger.close()
        if self.mqtt_client is not None:
            self.mqtt_client.close()
        pygame.quit()
        sys.exit()
