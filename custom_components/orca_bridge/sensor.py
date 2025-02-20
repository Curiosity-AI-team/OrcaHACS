from homeassistant.components.sensor import SensorEntity

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([MyCustomSensor()])

class MyCustomSensor(SensorEntity):
    def __init__(self):
        self._state = None

    @property
    def name(self):
        return "My Custom Sensor"

    @property
    def state(self):
        return self._state