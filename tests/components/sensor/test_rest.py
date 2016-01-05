"""
tests.components.sensor.test_rest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests rest sensor.
"""
from unittest.mock import patch

import pytest

import homeassistant.core as ha
import homeassistant.components.sensor as sensor


@pytest.mark.usefixtures('betamax_session')
class TestSensorRest:
    """ Test the rest sensor. """

    def setup_method(self, method):
        self.hass = ha.HomeAssistant()

    def teardown_method(self, method):
        """ Stop down stuff we started. """
        self.hass.stop()

    def test_configuration(self, betamax_session):
        # Bad resource
        assert sensor.setup(self.hass, {
            'sensor': {
                'platform': 'rest',
                'resource': 'test.com',
            }
        })

        assert self.hass.states.get('sensor.test') is None

    def test_good_reading(self, betamax_session):
        with patch('homeassistant.components.sensor.rest.requests.Session',
                   return_value=betamax_session):
            assert sensor.setup(self.hass, {
                'sensor': {
                    'platform': 'rest',
                    'name': 'test',
                    'resource': 'https://test.test',
                    'unit_of_measurement': '°F',
                    'value_template': '{{ value_json.result | round(2) }}'
                }
            })

        state = self.hass.states.get('sensor.test')
        assert state.state == "68.36"
        assert state.attributes['unit_of_measurement'] == '°F'
        assert state.attributes['friendly_name'] == 'test'
