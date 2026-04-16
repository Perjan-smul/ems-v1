"""EMS V1.2 Integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import EMSCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    coordinator = EMSCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("EMS V1.2 setup complete")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    coordinators = hass.data.get(DOMAIN)

    if coordinators:
        coordinator = coordinators.pop(entry.entry_id, None)

        if coordinator and hasattr(coordinator, "async_shutdown"):
            await coordinator.async_shutdown()

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )

    if coordinators and not coordinators:
        hass.data.pop(DOMAIN)

    return unload_ok
