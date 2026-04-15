from homeassistant.core import HomeAssistant

DOMAIN = "ems_v1"

async def async_setup(hass: HomeAssistant, config: dict):
    return True


async def async_setup_entry(hass: HomeAssistant, entry):
    from .coordinator import EMSCoordinator

    coordinator = EMSCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    return True