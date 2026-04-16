"""EMS V1.2 Home Assistant integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import EMSCoordinator

_LOGGER = logging.getLogger(__name__)


PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EMS V1.2 from config entry."""

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    coordinator = EMSCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("EMS V1.2 setup complete entry_id=%s", entry.entry_id)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload EMS V1.2."""

    coordinators = hass.data.get(DOMAIN)
    if not coordinators:
        return True

    coordinator = coordinators.pop(entry.entry_id, None)

    if coordinator and hasattr(coordinator, "async_shutdown"):
        await coordinator.async_shutdown()

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )

    if not coordinators:
        hass.data.pop(DOMAIN)

    _LOGGER.info("EMS V1.2 unloaded entry_id=%s", entry.entry_id)

    return unload_ok
