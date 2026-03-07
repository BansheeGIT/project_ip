from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, Protocol

try:
    import paho.mqtt.client as paho
except ImportError:  # pragma: no cover - optional dependency in some envs
    paho = None  # type: ignore[assignment]


WireHandler = Callable[[str, Any], None]


class BrokerTransport(Protocol):
    def subscribe(self, topic: str, handler: WireHandler) -> None: ...
    def publish(self, topic: str, payload: Any) -> None: ...
    def start(self) -> None: ...
    def close(self) -> None: ...


class LocalBrokerTransport:
    """In-process pub/sub transport."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[WireHandler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: WireHandler) -> None:
        self._subscribers[topic].append(handler)

    def publish(self, topic: str, payload: Any) -> None:
        for handler in list(self._subscribers.get(topic, [])):
            handler(topic, payload)

    def start(self) -> None:
        return

    def close(self) -> None:
        return


class HiveMQBrokerTransport:
    """Network MQTT transport backed by broker.hivemq.com (or custom host)."""

    def __init__(
        self,
        client_id: str,
        host: str = "broker.hivemq.com",
        port: int = 1883,
        keepalive: int = 30,
        qos: int = 0,
    ) -> None:
        if paho is None:
            raise RuntimeError("paho-mqtt is not installed")
        self.host = host
        self.port = int(port)
        self.keepalive = int(keepalive)
        self.qos = int(qos)
        self._connected = False
        self._started = False
        self._subscribers: dict[str, list[WireHandler]] = defaultdict(list)

        self._client = paho.Client(client_id=client_id, protocol=paho.MQTTv311)
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

    def _on_connect(self, client, _userdata, _flags, rc):
        self._connected = rc == 0
        if not self._connected:
            return
        for topic in self._subscribers:
            client.subscribe(topic, qos=self.qos)

    def _on_disconnect(self, _client, _userdata, _rc):
        self._connected = False

    def _on_message(self, _client, _userdata, msg):
        handlers = list(self._subscribers.get(msg.topic, []))
        for handler in handlers:
            handler(msg.topic, msg.payload)

    def start(self) -> None:
        if self._started:
            return
        self._client.connect(self.host, self.port, self.keepalive)
        self._client.loop_start()
        self._started = True

    def subscribe(self, topic: str, handler: WireHandler) -> None:
        self._subscribers[topic].append(handler)
        if self._connected:
            self._client.subscribe(topic, qos=self.qos)

    def publish(self, topic: str, payload: Any) -> None:
        self._client.publish(topic, payload=payload, qos=self.qos)

    def close(self) -> None:
        if not self._started:
            return
        self._client.loop_stop()
        self._client.disconnect()
        self._started = False
        self._connected = False
