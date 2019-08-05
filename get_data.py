import requests
from collections import OrderedDict
import json
from datetime import datetime as dt
from datetime import timedelta
import time

today = dt.today().strftime("%Y%m%d")
period = 7
timeframe_type = 'previous'

acronym_lang = {'NL': 'nld', 'AT': 'deu', 'CH': 'eng', 'CZ': 'ces', 'HU': 'eng', 'PL': 'pol', 'RO': 'eng', 'SK':'eng'}

source_url = 'web-api-prod-obo.horizon.tv'
oesp_web = 'https://{source}/oesp/v3/{country_acr}/{language}/web/{api}'

channel = 'channels'
schedules = 'programschedules/{date}/{part}'
listing = 'listings/{id}?byLocationId=65535'
stations = 'stations'


def get_dates(period, timeframe_type):
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
    response = requests.get(url)
    try:
        return response.json()
    except BaseException as error:
        return "Can't obtain {} with error {}".format(url, error)


def get_title_matching(stations_json):
    station_dict = {}
    for station in stations_json['stations']:
        station_dict[station['id']] = station['title']
    return station_dict


def get_main_data(schedule_json, channel_prog, missing_epg, id_title):
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


def get_overlap_and_gap(channel_prog, gap_size=10000):
    """
    Derives info about overlaps and gaps from program line
    :param channel_prog: structure ('dict') with info about all programs for period/country
    :param gap_size: time delta
    :return: two structure ('dict_list') - info about overlap and gaps
    """
    _id = 0
    _start = 1
    _end = 2
    overlap, gap = dict(), dict()
    missing_epg = list()
    for channel, dict_prog in channel_prog.items():

        try:
            prev_program = dict_prog.popitem(last=False)
            prev_times = prev_program[_start]

            for crid, times in dict_prog.items():
                if crid != prev_program[_id] and times[_start] < prev_times[_end]:
                    overlap.setdefault(channel, []).append((prev_program[_id], prev_program[_start], crid, times))
                if crid != prev_program[_id] and times[_start] - prev_times[_end] > gap_size:
                    gap.setdefault(channel, []).append((prev_program[_id], prev_program[_start], crid, times))
                prev_program = (crid, times)
                prev_times = prev_program[_start]
        except KeyError:
            missing_epg.append(channel)
    return overlap, gap, missing_epg


def date_format(seconds):
    return str(dt.strptime(time.ctime(int(seconds) / 1000), '%a %b %d %H:%M:%S %Y'))


for acr, lang in acronym_lang.items():

    dates = get_dates(period, timeframe_type)
    schedule_url = url_constructor(acr, lang, schedules)
    schedule_url_list = [schedule_url.format(date=date, part=part) for date in dates for part in range(1, 5)]

    id_title_stations = dict()
    stations_json = get_response_json(url_constructor(acr, lang, stations))
    [id_title_stations.setdefault(stat['id'], stat['title']) for stat in stations_json['stations']]

    # channel_titles = get_title_matching(stations_json)

    channel_prog = dict()
    missing_epg = dict()

    for url in schedule_url_list:
        channel_prog, m_epg = get_main_data(get_response_json(url), channel_prog, missing_epg, id_title_stations)

    overlap, gap, miss_epg = get_overlap_and_gap(channel_prog)

    # with open('./static_files/line_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(channel_prog))

    with open('./static_files/gap_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
        file.write((json.dumps(gap)))

    with open('./static_files/overlap_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
        file.write((json.dumps(overlap)))

    with open('./static_files/m_epg_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
        file.write((json.dumps(m_epg)))
