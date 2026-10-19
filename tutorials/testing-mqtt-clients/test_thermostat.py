import json
from unittest.mock import Mock

from thermostat import Thermostat

PREFIX = "home/test"


def make():
    pub = Mock()
    return Thermostat(prefix=PREFIX, publish=pub), pub


def msg(value):
    return json.dumps({"value": value}).encode()


def test_turns_heater_on_below_band():
    t, pub = make()
    t.on_temperature(f"{PREFIX}/kitchen/temperature", msg(20.0))
    pub.assert_called_once_with(f"{PREFIX}/kitchen/heater/set", "ON", 1, True)


def test_no_publish_inside_hysteresis_band():
    t, pub = make()
    t.on_temperature(f"{PREFIX}/kitchen/temperature", msg(21.2))
    pub.assert_not_called()


def test_turns_heater_off_above_band():
    t, pub = make()
    t.on_temperature(f"{PREFIX}/kitchen/temperature", msg(20.0))
    t.on_temperature(f"{PREFIX}/kitchen/temperature", msg(21.6))
    assert pub.call_args.args[1] == "OFF"


def test_ignores_garbage():
    t, pub = make()
    for bad in [b"", b"not json", b'{"temp": 3}', b'{"value": "hot"}']:
        t.on_temperature(f"{PREFIX}/kitchen/temperature", bad)
    pub.assert_not_called()
