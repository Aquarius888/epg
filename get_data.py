import requests
from collections import OrderedDict
import json
from datetime import datetime as dt
from datetime import timedelta
import time

try:
    from config import settings
except ImportError as err:
    print("Make sure settings.py exists in 'config' directory. {err}".format(err=err))


period = settings.PERIOD
timeframe_type = settings.TIMEFRAME_TYPE
acronym_lang = settings.ACRONYM_LANG
source_url = settings.SOURCE_URL
oesp_web = settings.OESP_WEB
channel = settings.CHANNEL
schedules = settings.SCHEDULES
schedules_dates = settings.SCHEDULES_DATES
listing = settings.LISTING
stations = settings.STATIONS


def get_dates(period, timeframe_type):
    """
    Get list of dates for processing
    :param period: amount of days
    :param timeframe_type: around ('period/2' before and 'period/2' days after today)
                           OR previous ('period' days before today)
    :return: list of strings with dates
    """
    if timeframe_type == 'around':
        return [(dt.today() - timedelta(period/2) + timedelta(day)).strftime("%Y%m%d") for day in range(period)]
    elif timeframe_type == 'previous':
        return [(dt.today() - timedelta(period) + timedelta(day)).strftime("%Y%m%d") for day in range(1, period + 1)]


def url_constructor(country_acr, language, api, constructor=oesp_web, source=source_url):
    return constructor.format(source=source,
                              country_acr=country_acr,
                              language=language,
                              api=api)


def get_response_json(url):
    """
    Send GET call to API
    :param url: API url
    :return: response in json
    """
    response = requests.get(url)
    try:
        return response.json()
    except BaseException as error:
        return "Can't obtain {} with error {} \n {}".format(url, error, response.text)


def get_main_data(schedule_json, channel_prog, missing_epg, id_title):
    """
    Parse main channel info json, fill dictionary {channel: OrderedDict(programms id, title, time of start and end)}
    :param schedule_json: main channel info json
    :param channel_prog:
    :param missing_epg:
    :param id_title: dictionary {channel id: channel title}
    :return: two dictionary: main info and info about missing EPG
    """
    for entry in schedule_json['entries']:
        try:
            channel_name = id_title[entry['o']]
        except KeyError:
            channel_name = 'NoChannelName'
        for prog in entry['l']:
            try:
                channel_prog.setdefault(channel_name, OrderedDict()).setdefault(prog['i'], (prog['t'],
                                                                                            prog['s'],
                                                                                            prog['e']))
            except KeyError:
                missing_epg.setdefault(channel_name, []).append((date_format(prog['s']), date_format(prog['e'])))

    return channel_prog, missing_epg


def get_overlap_and_gap(channel_prog, overlap, gap, gap_size=10000):
    """
    Derives info about overlaps and gaps from program line
    :param channel_prog: structure ('dict') with info about all programs for period/country
    :param gap_size: time delta
    :return: two structure ('dict_list') - info about overlaps and gaps
    """
    _id = 0
    _start = 1
    _end = 2

    missing_epg = list()
    for channel, dict_prog in channel_prog.items():
        try:
            prev_program = dict_prog.popitem(last=False)
            prev_times = prev_program[_start]

            for crid, times in dict_prog.items():
                if crid != prev_program[_id] and times[_start] < prev_times[_end]:
                    overlap.setdefault(channel, []).append((prev_program[_id], prev_times, crid, times))
                if crid != prev_program[_id] and times[_start] - prev_times[_end] > gap_size:
                    gap.setdefault(channel, []).append((prev_program[_id], prev_program[_start], crid, times))

                prev_program = (crid, times)
                prev_times = prev_program[_start]
        except KeyError:
            missing_epg.append(channel)
    return overlap, gap


def date_format(seconds):
    # convert seconds to string format
    return str(dt.strptime(time.ctime(int(seconds) / 1000), '%a %b %d %H:%M:%S %Y'))


if __name__ == '__main__':

    today = dt.today().strftime("%Y%m%d")

    for acr, lang in acronym_lang.items():

        dates = get_dates(period, timeframe_type)
        schedule_url = url_constructor(acr, lang, schedules)

        id_title_stations = dict()
        stations_json = get_response_json(url_constructor(acr, lang, stations))
        # fill dictionary {channel id: channel title}
        [id_title_stations.setdefault(stat['id'], stat['title']) for stat in stations_json['stations']]

        missing_epg = dict()
        overlap, gap = dict(), dict()

        for date in dates:
            channel_prog = dict()
            # API divides main info for 4 parts (~6 hours for each part)
            for part in range(1, 5):
                url = schedule_url + schedules_dates.format(date=date, part=part)
                api_response = get_response_json(url)
                channel_prog, missing_epg = get_main_data(api_response, channel_prog, missing_epg, id_title_stations)

            # !!! write FULL json
            with open('./static_files/line_{}_{}.txt'.format(acr, date), 'w', encoding='utf-8') as file:
                file.write(json.dumps(channel_prog))

            overlap, gap = get_overlap_and_gap(channel_prog, overlap, gap)
            print("Schedule API for {acr} {date} has been processed".format(acr=acr, date=date))

        with open('./static_files/m_epg_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
            file.write((json.dumps(missing_epg)))

        with open('./static_files/gap_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
            file.write((json.dumps(gap)))

        with open('./static_files/overlap_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
            file.write((json.dumps(overlap)))
