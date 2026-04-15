# custom_components/ems_v1/config_flow.py

from homeassistant import config_entries

DOMAIN = "ems_v1"

class EMSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="EMS V1", data={})

        return self.async_show_form(step_id="user")