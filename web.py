# from gevent import monkey
# monkey.patch_all()
from bottle import Bottle, template, request
import json
from time import gmtime, strftime
from datetime import datetime as dt
from datetime import timedelta
import time

try:
    from config import settings
except ImportError as err:
    print("Make sure settings.py exists in 'config' directory. {err}".format(err=err))

app = Bottle()

date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
today = dt.today()

period = settings.PERIOD
timeframe_type = settings.TIMEFRAME_TYPE


def get_dates(period, timeframe_type):
    """
    Get list of dates for processing
    :param period: amount of days
    :param timeframe_type: around ('period/2' before and 'period/2' days after today)
                           OR previous ('period' days before today)
    :return: list of strings with dates
    """
    if timeframe_type == 'around':
        return [(dt.today() - timedelta(period/2) + timedelta(day)) for day in range(period)]
    elif timeframe_type == 'previous':
        return [dt.today() - timedelta(period) + timedelta(day) for day in range(1, period)]


dates = get_dates(period, timeframe_type)


def get_line(filename, day):
    """
    Open text file with EPG in json, render templates and compose html 'page'
    :param filename: name of file with info in json
    :param day: string with date, format ('YYYYMMDD')
    :return: html 'page'
    """
    with open('./static_files/{}.txt'.format(filename), 'r') as file:
        data = json.loads(file.read())
        data_generator = ((ch, line) for ch, line in data.items())
        # Back convert date in string format to seconds
        sec = time.mktime(time.strptime('{}:{}:{}'.format(day[:4], day[4:6], day[6:]), '%Y:%m:%d'))
        lst = template('line', rows=data_generator, date=sec)
        main = template('main', date='EPG', today=today, dates=dates)
        return main + lst


def get_miss(filename):
    with open('./static_files/{}.txt'.format(filename), 'r') as file:
        filename_parts = filename.split('_')
        data = json.loads(file.read())
        lst = template('missing_epg', rows=data)
        main = template('main', date='missing EPG {}'.format(filename_parts[2]), today=today, dates=dates)
        return main + lst


def get_gap(filename):
    with open('./static_files/{}.txt'.format(filename), 'r') as file:
        data = json.loads(file.read())
        lst = template('gaps_overlaps', rows=data)
        main = template('main', date=filename, today=today, dates=dates)
        return main + lst


@app.route('/', method='POST')
def main():
    typ = request.forms.get('type')
    day = request.forms.get('date')
    acr = request.forms.get('country')
    if typ == 'line':
        filename = 'line_{acr}_{date}'.format(acr=acr, date=day)
        return get_line(filename, day=day)
    elif typ == 'gap':
        filename = 'gap_{}'.format(acr)
        return get_gap(filename)
    elif typ == 'overlap':
        filename = 'overlap_{}'.format(acr)
        return get_gap(filename)
    elif typ == 'missing':
        filename = 'm_epg_{}'.format(acr)
        return get_miss(filename)


@app.route('/')
def main():
    return template('main', date='main', today=today, dates=dates)


if __name__ == '__main__':
    app.run(reloader=True, debug=True, host='0.0.0.0', port=8080)
