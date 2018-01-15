"""
Unit Tests for forecast_compare.py
"""

import pytest
from .. import forecast_compare
from mock import patch

REQUEST_PATCH = 'ForecastCompare.forecast_compare.requests.get'


@pytest.mark.smoke
@patch(REQUEST_PATCH)
def test_get_forecast_not_none(mock_get):
    mock_get.return_value.ok = True
    response = forecast_compare.get_forecast("Toronto")
    assert response is not None


@pytest.mark.smoke
@patch(REQUEST_PATCH)
def test_get_forecast_response(mock_get):
    weather = [{
        'name': 'Toronto',
        'main': {
            'temp': 10
        },
        'weather': [{
            'description': 'sunny'
        }]
    }]

    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = weather
    response = forecast_compare.get_forecast("Toronto")
    assert weather == response


@pytest.mark.smoke
@pytest.mark.parametrize("temp, expected",
                         [
                             # Test city1 is warmer
                             (10, "Toronto is warmer by 12 C!"),
                             # Test city2 is  warmer
                             (-10, "Vancouver is warmer by 8 C!"),
                             # Test city1 and city2 same temp
                             (-2, "Both Toronto and Vancouver have "
                                  "the same temperature of -2 C"),
                         ])
def test_compare_forecast(temp, expected, capsys):
    weather1 = {
        'name': 'Toronto',
        'main': {
            'temp': temp
        },
        'weather': [{
            'description': 'sunny'
        }]
    }

    weather2 = {
        'name': 'Vancouver',
        'main': {
            'temp': -2
        },
        'weather': [{
            'description': 'cold'
        }]
    }

    forecast_compare.compare_forecast(weather1, weather2)
    # Use capsys to assert print to standard out
    out, err = capsys.readouterr()
    assert expected in out
