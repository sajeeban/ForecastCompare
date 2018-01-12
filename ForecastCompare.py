'''
Python script to compare forecast for 2 cities given via command line arguments. 
Program outputs a text indicating the temperatures of both cities
'''

import requests
import argparse
from config import API_KEY

__author__ = "sajeeban.lingam"

URL = 'http://api.openweathermap.org/data/2.5/weather?APPID={API}&units=metric&'.format(API=API_KEY)


# Simple decorator to log our API calls, this can be uploaded to AWS CloudWatch
# and metrics or alerts can be made
def logger(f):
    import logging
    logging.basicConfig(filename='{}.log'.format(f.__name__), level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    def wrapper(*args, **kwargs):
        logging.info(
            'Open Weather Map API called with args: {} and kwargs: {}'.format(args, kwargs))
        return f(*args, **kwargs)

    return wrapper


def main():
    city1, city2 = get_cities()
    forecast_city1 = get_forecast(city1)
    forecast_city2 = get_forecast(city2)
    compare_forecast(forecast_city1, forecast_city2)


# Parse command line arguments and return
def get_cities():
    parser = argparse.ArgumentParser(description='Program to compare forecast of 2 cities')
    parser.add_argument('--city1', required=True, help='Please enter name of city 1')
    parser.add_argument('--city2', required=True, help='Please enter name of city 2')

    args = parser.parse_args()
    return args.city1, args.city2


# return API call object, also log API calls to a log file
@logger
def get_forecast(city):
    query = "{}q={}".format(URL, city)
    print query
    r = requests.get(query).json()
    return r


# Comparing 2 city forecasts 
def compare_forecast(c1, c2):
    c1_name, c1_temp, c1_desc = c1['name'], int(c1['main']['temp']), c1['weather'][0]['description']
    c2_name, c2_temp, c2_desc = c2['name'], int(c2['main']['temp']), c2['weather'][0]['description']

    print "Current weather in {} is {} C with {}".format(c1_name, c1_temp, c1_desc)
    print "Current weather in {} is {} C with {}\n".format(c2_name, c2_temp, c2_desc)

    if c1_temp > c2_temp:
        print "{} is warmer by {} C!".format(c1_name, c1_temp - c2_temp)
    elif c1_temp < c2_temp:
        print "{} is warmer by {} C!".format(c2_name, c2_temp - c1_temp)
    else:
        print "Both {} and {} have the same temperature of {} C".format(c1_name, c2_name, c1_temp)


if __name__ == '__main__':
    main()
