import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval

# Set up logging
_LOGGER = logging.getLogger(__name__)

# Interval to print hello (every 5 seconds)
PRINT_INTERVAL = timedelta(seconds=5)

# Define a simple sensor class
class HelloSensor(Entity):
    """Representation of a Hello sensor."""

    def __init__(self):
        self._state = "Hello from Home Assistant!"
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return "Hello Sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Update the state of the sensor."""
        self._state = "Hello from Home Assistant!"
        _LOGGER.info("Hello sensor updated!")

async def async_setup(hass, config):
    """Set up the Hello integration."""

    # Register the HelloSensor entity
    async def register_hello_sensor():
        hass.data["hello_integration"] = HelloSensor()
        hass.async_add_job(hass.helpers.entity_component.async_add_entities, [hass.data["hello_integration"]])

    # Callback function to print hello every 5 seconds
    async def print_hello(now):
        _LOGGER.info("Hello from custom integration!")
        print("Hello from Home Assistant!")  # This will print to your terminal

        # Update the state of the Hello sensor
        await hass.data["hello_integration"].async_update()

    # Register the hello sensor after setup
    await register_hello_sensor()

    # Schedule the callback function to run every 5 seconds
    async_track_time_interval(hass, print_hello, PRINT_INTERVAL)

    # Log the setup feedback
    _LOGGER.info("Hello Integration has been set up successfully.")

    return True
