# Smart Traffic Light Simulation

Interactive traffic simulation with two control modes:

- `fixed`: classic phase switching with fixed timing.
- `mqtt-smart`: smart control over MQTT with lane camera telemetry, emergency siren priority, and live metrics logging.

## Features

- Pygame-based city intersection simulation.
- Vehicles, pedestrians, emergency vehicles (`sirens_on` supported).
- MQTT smart-controller pipeline:
  - camera sensor node
  - controller node
  - actuator node
  - monitor node
- Transport options for MQTT smart mode:
  - `hivemq` (real broker, default: `broker.hivemq.com`)
  - `local` (in-process transport)
- Optional Fernet encryption for MQTT payloads (`cryptography`).
- Efficiency logging to:
  - CSV files in `logs/`
  - SQLite DB `logs/efficiency.sqlite3`
- SQL/report helpers for comparing `fixed` vs `mqtt-smart` runs.

## Requirements

- Python 3.10+
- See `requirements.txt`

## Installation

```bash
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install -U pip
py -m pip install -r requirements.txt
```

## Run

### 1) Fixed mode

```bash
py main.py --mode fixed
```

### 2) MQTT smart mode over HiveMQ

```bash
py main.py --mode mqtt-smart --mqtt-transport hivemq
```

Optional broker override:

```bash
py main.py --mode mqtt-smart --mqtt-transport hivemq --mqtt-host broker.hivemq.com --mqtt-port 1883
```

### 3) MQTT smart mode with local transport

```bash
py main.py --mode mqtt-smart --mqtt-transport local
```

## MQTT Security (Fernet)

If `cryptography` is installed, MQTT payload encryption is enabled in smart mode.

Optional explicit key:

```bash
set MQTT_FERNET_KEY=<your_fernet_key>
```

If key is not set, a process-local Fernet key is auto-generated.

## Tests

```bash
py -m pytest -q -p no:cacheprovider
```

## Metrics and Comparison

During simulation, efficiency samples are written to:

- `logs/efficiency_<mode>_<timestamp>.csv`
- `logs/efficiency.sqlite3` table `efficiency_samples`

Run quick comparison report:

```bash
py -m db.report_cli --db logs/efficiency.sqlite3
```

If you see `No runs found`, run the simulation first in at least one mode.

## Project Structure

- `app/` - application runtime and game loop
- `sim/` - world, entities, spawner, metrics
- `traffic/` - fixed controller logic and phases
- `mqtt/` - client, transport, topics, schemas, security
- `nodes/` - sensor/controller/actuator/monitor nodes
- `db/` - SQLite persistence and report queries
- `tests/` - unit/integration tests

## Notes

- Public broker topics are namespaced per run to avoid collisions.
- Smart mode falls back to local transport if remote broker connection fails.
