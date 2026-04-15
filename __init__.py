from homeassistant.core import HomeAssistant
from .coordinator import EMSCoordinator

DOMAIN = "ems_v1"

async def async_setup(hass: HomeAssistant, config: dict):
    coordinator = EMSCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN] = coordinator
    return True