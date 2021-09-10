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

__version__ = '0.1.3'

REQUIREMENTS = ['lxml','MechanicalSoup','beautifulsoup4']

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
        browser.open("https://internetaccount.myt.mu")

        # Enter credentials
        login_form = browser.select_form('#id3')
        browser["signInForm.username"] = self._config.get(CONF_USERNAME)
        browser["signInForm.password"] = self._config.get(CONF_PASSWORD)

        # Sign in
        login_form.choose_submit('signInContainer:submit')
        browser.submit_selected()

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
            remaining_allowance = stats[5]

            # Extract the value and convert to GB
            gb_amount = float(re.findall(r'\d*\.?\d+', remaining_allowance.text)[0]) * float(0.001)

            # Conversion to GB
            if (gb_amount < 1):
                remaining = gb_amount
            else:
                remaining = int(round(gb_amount))

            _LOGGER.debug("Value Extracted")
            self._state = remaining

        # If login fails, print error message from website
        else:
            error_message = page.select(".feedbackPanelERROR")[0]
            _LOGGER.error(error_message.text)
