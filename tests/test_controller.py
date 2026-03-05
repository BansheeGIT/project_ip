from traffic.controller_logic import TrafficController
from traffic.phases import ALL_RED, EW_GREEN, NS_GREEN, NS_YELLOW
from sim.pedestrians import Pedestrian
from sim.world import World


def test_controller_keeps_green_before_20_seconds():
    controller = TrafficController()
    phase = controller.decide(19.9, queue_ns=999, queue_ew=999)
    assert phase == NS_GREEN


def test_controller_switches_after_20_seconds():
    controller = TrafficController()
    phase = controller.decide(20.1, queue_ns=0, queue_ew=0)
    assert phase == NS_YELLOW


def test_controller_emergency_preemption_forces_axis_green():
    controller = TrafficController()
    controller.set_preemption(True, "EW")
    phase = controller.decide(1.0, queue_ns=100, queue_ew=0)
    assert phase == "EW_GREEN"


def test_world_preemption_detects_approaching_emergency():
    world = World()
    world.vehicles = []
    world.next_id = 1
    world.spawn_emergency(direction="N", x=1000, y=180, speed=200, sirens_on=True)

    active, axis = world.compute_preemption_state()
    assert active is True
    assert axis == "NS"


def test_controller_yellow_to_all_red_transition():
    controller = TrafficController()
    controller.current_phase = NS_YELLOW
    controller.timer = 1.99
    phase = controller.decide(0.02, queue_ns=0, queue_ew=0)
    assert phase == ALL_RED


def test_vehicle_after_stop_line_does_not_stop_on_red():
    world = World()
    world.vehicles = []
    world.green_axis = "EW"  # NS cars see red.
    world.spawn_vehicle(direction="N", x=1000, y=350, speed=200)
    car = world.vehicles[0]

    world.step(0.2)
    assert car["current_speed"] > 0.0


def test_vehicle_stops_for_pedestrian_in_same_lane():
    world = World()
    world.vehicles = []
    world.pedestrians = []
    world.green_axis = "NS"
    world.spawn_vehicle(direction="N", x=1000, y=250, speed=200)
    car = world.vehicles[0]

    ped = type("PedStub", (), {})()
    ped.position = [1000.0, 420.0]
    ped.active = True
    world.pedestrians = [ped]

    world.step(0.2)
    assert car["current_speed"] < 200.0


def test_pedestrian_waits_at_curb_on_red():
    pedestrian = Pedestrian(740, 430, "EW")
    pedestrian.velocity = [100.0, 0.0]
    pedestrian.active = False
    for _ in range(20):
        pedestrian.update(0.1)
    assert pedestrian.position[0] <= pedestrian.WAIT_X_LEFT


def test_pedestrian_signal_axis_mapping():
    world = World()
    world.pedestrians = []
    ped = Pedestrian(740, 430, "EW")
    ped.velocity = [100.0, 0.0]
    world.pedestrians.append(ped)

    world.update_pedestrians(0.01, phase=EW_GREEN)
    assert ped.active is True

    world.update_pedestrians(0.01, phase=NS_GREEN)
    assert ped.active is False


def test_vehicle_gap_enforced_after_step():
    world = World()
    world.vehicles = []
    world.green_axis = "NS"
    world.spawn_vehicle("N", 920, 300, 200)
    world.spawn_vehicle("N", 920, 255, 200)

    world.step(0.1)
    cars = sorted(world.vehicles, key=lambda v: v["y"], reverse=True)
    lead, trail = cars[0], cars[1]
    assert (lead["y"] - trail["y"]) >= 100.0


def test_vehicle_does_not_overshoot_stop_line_on_red():
    world = World()
    world.vehicles = []
    world.green_axis = "EW"  # NS sees red.
    world.spawn_vehicle("N", 920, 260, 200)
    car = world.vehicles[0]

    world.step(0.2)
    assert car["y"] <= world.STOP_LINES["N"]
