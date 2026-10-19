import json
from dataclasses import dataclass
from typing import Callable

Publish = Callable[[str, str, int, bool], None]


@dataclass
class Thermostat:
    prefix: str
    publish: Publish
    setpoint: float = 21.0
    hysteresis: float = 0.5
    heating: bool = False

    def on_temperature(self, topic: str, payload: bytes) -> None:
        try:
            value = float(json.loads(payload)["value"])
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            return  # ignore malformed messages

        room = topic.split("/")[-2]
        if not self.heating and value < self.setpoint - self.hysteresis:
            self.heating = True
        elif self.heating and value > self.setpoint + self.hysteresis:
            self.heating = False
        else:
            return

        self.publish(f"{self.prefix}/{room}/heater/set",
                     "ON" if self.heating else "OFF", 1, True)
