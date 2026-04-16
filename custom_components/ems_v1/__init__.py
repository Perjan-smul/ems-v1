"""EMS V1 integration for Home Assistant."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import EMSCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EMS V1 from a config entry."""

    # 👇 ALWAYS ensure dict container exists
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    # Create coordinator per entry
    coordinator = EMSCoordinator(hass, entry)

    # Initial data load
    await coordinator.async_config_entry_first_refresh()

    # Store per entry (IMPORTANT: multi-entry safe)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward setup to platforms (sensors etc.)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    _LOGGER.info("EMS V1 loaded for entry_id=%s", entry.entry_id)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload EMS V1 config entry."""

    coordinators = hass.data.get(DOMAIN)

    if not coordinators:
        return True

    # Safely remove coordinator
    coordinator = coordinators.pop(entry.entry_id, None)

    if coordinator:
        _LOGGER.info("Unloading EMS V1 entry_id=%s", entry.entry_id)

        # Optional cleanup hook (only if you implement it later)
        if hasattr(coordinator, "async_shutdown"):
            await coordinator.async_shutdown()

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        ["sensor"],
    )

    # Cleanup domain if empty
    if not coordinators:
        hass.data.pop(DOMAIN)

    return unload_ok
