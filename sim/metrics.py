# sim/metrics.py
# Метрики / утилиты для симуляции (без pygame, без MQTT)
from __future__ import annotations
from typing import Tuple

def count_queues(world) -> Tuple[int, int]:
    """Считает количество остановившихся машин в очередях по осям NS и EW.

    Ожидается, что у машины есть поля:
    - direction: 'N'/'S'/'E'/'W'
    - is_stopped: bool
    """
    ns_dirs = {"N", "S"}
    ew_dirs = {"E", "W"}
    queue_ns = 0
    queue_ew = 0

    for v in getattr(world, "vehicles", []):
        if not v.get("is_stopped"):
            continue
        d = v.get("direction")
        if d in ns_dirs:
            queue_ns += 1
        elif d in ew_dirs:
            queue_ew += 1

    return queue_ns, queue_ew
