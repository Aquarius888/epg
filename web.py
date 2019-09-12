# import bjoern

import bottle
from bottle import Bottle, template
import json
from time import gmtime, strftime
from datetime import datetime as dt
from datetime import timedelta
import time
import os

try:
    from config import settings
except ImportError as err:
    print("Make sure settings.py exists in 'config' directory. {err}".format(err=err))

app = Bottle()

date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
now = int(time.time() * 1000)
today = dt.today()

period = settings.PERIOD
timeframe_type = settings.TIMEFRAME_TYPE

location = 'preprod'


def get_available_country():
    # TODO: extend with Prod, Sugar etc (may be as dictionary{type:set(acr)})
    return set([file.strip('.txt').split('_')[1] for file in os.listdir(f'./static_files/{location}/') if 'line' in file])


def get_dates(period, timeframe_type):
    """
    Get list of dates for processing
    :param period: amount of days
    :param timeframe_type: around ('period/2' before and 'period/2' days after today)
                           OR previous ('period' days before today)
    :return: list of strings with dates
    """
    if timeframe_type == 'around':
        return [(dt.today() - timedelta(period / 2) + timedelta(day)) for day in range(period)]
    elif timeframe_type == 'previous':
        return [dt.today() - timedelta(period) + timedelta(day) for day in range(1, period)]


dates = get_dates(period, timeframe_type)


@app.route('/<filename>')
def get_line(filename):
    """
    Open text file with EPG in json, render templates and compose html 'page'
    :param filename: name of file with info in json
    :param day: string with date, format ('YYYYMMDD')
    :return: html 'page'
    """
    country_list = get_available_country()
    location, filename = filename.split('-')
    with open(f'./static_files/{location}/line_{filename}_{today.strftime("%Y%m%d")}.txt', 'r') as file:
        data = json.loads(file.read())
        print("Channels: {}".format(len(data.keys())))
        data_generator = ((ch, line) for ch, line in data.items())

        lst = template('line', rows=data_generator, date=now)
        main = template('main', date=now, today=today, dates=dates, available=country_list)
        return main + lst


def get_miss(filename):
    country_list = get_available_country()
    with open('./static_files/{}.txt'.format(filename), 'r') as file:
        data = json.loads(file.read())
        lst = template('missing_epg', rows=data)
        main = template('main', date=now, today=today, dates=dates,
                        available=country_list)
        return main + lst


def get_gap(filename):
    country_list = get_available_country()
    with open('./static_files/{}.txt'.format(filename), 'r') as file:
        data = json.loads(file.read())
        lst = template('gaps_overlaps', rows=data)
        main = template('main', date=now, today=today, dates=dates, available=country_list)
        return main + lst


@app.route('/')
def main():
    country_list = get_available_country()
    return template('main', date=now, today=today, dates=dates, available=country_list)


if __name__ == '__main__':
    bottle.run(app, reloader=True, debug=True, host='0.0.0.0', port=8080)
    # bottle.run(app, reloader=True, debug=True, host='0.0.0.0', port=8080, server='bjoern')
