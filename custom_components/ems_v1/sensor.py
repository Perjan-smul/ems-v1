from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        EMSROISensor(coordinator),
        EMSActionSensor(coordinator),
        EMSLearningSensor(coordinator),
        EMSPVForecastSensor(coordinator),
        EMSLoadForecastSensor(coordinator),
    ]

    async_add_entities(entities)


# --------------------------------------------------
# ROI SENSOR
# --------------------------------------------------

class EMSROISensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = "EMS ROI"
        self._attr_unique_id = "ems_roi"
        self._attr_unit_of_measurement = "€"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self):
        sim = self.coordinator.data.get("simulation")
        if not sim:
            return None
        return round(sim[0]["roi"], 3)

    @property
    def extra_state_attributes(self):
        sim = self.coordinator.data.get("simulation")
        if not sim:
            return None

        attrs = {}

        for s in sim:
            cap = s["capacity_kwh"]
            attrs[f"{cap}kWh_roi"] = round(s["roi"], 3)

        attrs["best_capacity_kwh"] = sim[0]["capacity_kwh"]

        return attrs


# --------------------------------------------------
# ACTION SENSOR
# --------------------------------------------------

class EMSActionSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = "EMS Action"
        self._attr_unique_id = "ems_action"

    @property
    def native_value(self):
        return self.coordinator.data.get("action")


# --------------------------------------------------
# LEARNING SENSOR
# --------------------------------------------------

class EMSLearningSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = "EMS Learning"
        self._attr_unique_id = "ems_learning"
        self._attr_icon = "mdi:brain"

    @property
    def native_value(self):
        return "active"

    @property
    def extra_state_attributes(self):
        learning = self.coordinator.data.get("learning")
        if not learning:
            return None

        return {
            "pv_bias": round(learning.get("pv_bias", 0), 4),
            "load_bias": round(learning.get("load_bias", 0), 4),
        }


# --------------------------------------------------
# FORECAST SENSORS
# --------------------------------------------------

class EMSPVForecastSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = "EMS PV Forecast"
        self._attr_unique_id = "ems_pv_forecast"

    @property
    def native_value(self):
        forecast = self.coordinator.data.get("forecast")
        if not forecast:
            return None
        return round(forecast["pv_kw"][0], 3)


class EMSLoadForecastSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = "EMS Load Forecast"
        self._attr_unique_id = "ems_load_forecast"

    @property
    def native_value(self):
        forecast = self.coordinator.data.get("forecast")
        if not forecast:
            return None
        return round(forecast["load_kw"][0], 3)
