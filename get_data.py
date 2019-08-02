import requests
from collections import OrderedDict
import json
from datetime import datetime as dt
from datetime import timedelta
import time

today = dt.today().strftime("%Y%m%d")
period = 7
timeframe_type = 'previous'

country_acr = ['NL']
language = ['nld']

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


def get_overlap_and_gap(channel_prog, gap_size=3):
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
    for channel, dict_prog in channel_prog.items():
        try:
            prev_program = dict_prog.popitem(last=False)

            for crid, times in dict_prog.items():
                prev_times = prev_program[_start]
                if crid != prev_program[_id] and times[_start] < prev_times[_end]:
                    overlap.setdefault(channel, []).append((prev_times[0], prev_program[_id],
                                                            date_format(prev_times[_end]),
                                                            times[0], crid, date_format(times[_start])))
                if crid != prev_program[_id] and times[_start] - prev_times[_end] > gap_size:
                    gap.setdefault(channel, []).append((prev_times[0], prev_program[_id],
                                                        date_format(prev_times[_end]),
                                                        times[0], crid, date_format(times[_start])))
                prev_program = (crid, times)
        except KeyError:
            print('{} empty dictionary?!'.format(channel))
    return overlap, gap


def date_format(seconds):
    return str(dt.strptime(time.ctime(int(seconds) / 1000), '%a %b %d %H:%M:%S %Y'))


def get_html_from_dict_list(dict_list):
    """
    Converts 'dict_list' to html string (table)
    :param dict_list: input structure
    :return: string with html tags
    """
    html_string = ""
    for ch, gaps_list in dict_list.items():
        html_table = "<table border=1>{}</table>"
        cells = ""
        channel_row = '<tr bgcolor="#ddd"><th width="100px">{channel}</th>{line}</tr>'
        for frame in gaps_list:
            first_title, first_id, first_end, next_title, next_id, next_start = frame
            cells += '<td>{} {}<br><i>{}</i> <br>{} {}<br><i>{}</i></td>'. \
                format(first_title, first_end, first_id,
                       next_title, next_start, next_id)
        html_string += html_table.format(channel_row.format(channel=ch, line=cells))

    return html_string


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
        channel_prog, _ = get_main_data(get_response_json(url), channel_prog, missing_epg, id_title_stations)

    overlap, gap = get_overlap_and_gap(channel_prog)

    with open('/epg/static_files/gap_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
        file.write((json.dumps(gap)))

    with open('/epg/static_files/overlap_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
        file.write((json.dumps(overlap)))
