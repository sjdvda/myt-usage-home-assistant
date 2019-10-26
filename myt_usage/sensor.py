import json
import logging
import voluptuous as vol
import requests
import re
from bs4 import BeautifulSoup

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

import mechanicalsoup

__version__ = '0.1.0'

REQUIREMENTS = ['lxml','MechanicalSoup']

REMAINING_DATA = 'remaining_data'

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    _LOGGER.debug("Setup platform myt usage")
    """Setup the myt usage scraper platform."""
    add_devices([MytSensor("my.t Remaining Data", config)], True)

class MytSensor(Entity):
    """Representation of the myt Scraper."""

    def __init__(self, name, config):
        """Initialize the myt scraper."""
        self._name = name
        self._state = None
        self._config = config

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return 'mdi:gauge'

    @property
    def unit_of_measurement(self):
        return 'GB'

    def update(self):
        """Get the latest data from the myt portal."""

        _LOGGER.debug("update called.")

        # Set browser
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'}
        )

        _LOGGER.debug("Attempting Login")

        # Open my.t website
        browser.open("http://internetaccount.myt.mu")

        # Enter credentials
        form = browser.select_form('.loginarea')
        browser["signInForm.username"] = self._config.get(CONF_USERNAME)
        browser["signInForm.password"] = self._config.get(CONF_PASSWORD)

        # Sign in
        form = browser.select_form()
        form.choose_submit('signInContainer:submit')
        resp = browser.submit_selected()

        # Load page
        page = browser.get_current_page()

        # Check if login is successful
        login_verify = page.select("#ContentBody")

        if login_verify:
            _LOGGER.debug("Login Successful")
            # Get values from page
            stats = (page.find_all("table")[5]).find_all("table")[1].find_all("td", bgcolor="#FFFFFF")

            _LOGGER.debug("Scraping Page")
            # Extract remaining data
            remaining_data = stats[5]

            # Regex black magic to extract the value
            amt = float(re.findall(r'\d*\.?\d+', remaining_data.text)[0])

            # Conversion to GB
            gb_amount = amt * float(0.001)
            if (gb_amount < 1):
                remaining = gb_amount
            else:
                remaining = int(round(gb_amount))

            _LOGGER.debug("Value Extracted")
            self._state = remaining

        # If login fails, print error message from website
        else:
            error_message = page.select(".feedbackPanelERROR")[0]
            _LOGGER.debug(error_message.text)
