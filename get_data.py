import asyncio
from aiohttp import ClientSession
from asyncio_throttle import Throttler

import requests

from argparse import ArgumentParser
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

source_url = settings.PROD_URL
preprod_url = settings.PREPROD_URL
sugar_url = settings.SUGAR_URL

oesp_web = settings.OESP_WEB
channel = settings.CHANNEL
schedules = settings.SCHEDULES
schedules_dates = settings.SCHEDULES_DATES
listing = settings.LISTING
stations = settings.STATIONS
# !!! Attention! Script should use proxy inside Vie cluster
# proxy = 'http://172.31.101.80:8888'
proxy = ''

orange = '#f97'
red = '#f8a'
green = '#dfb'
grey = '#ccc'
blue = '#dff'

semaphore = Throttler(rate_limit=15, period=10)

fetch_counter = 0

today = dt.today().strftime("%Y%m%d")


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


def url_constructor(country_acr, language, api, constructor=oesp_web, source=preprod_url):
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
    response = requests.get(url, proxies={'https': proxy})
    try:
        return response.json()
    except BaseException as error:
        return "Can't obtain {} with error {} \n {}".format(url, error, response.text)


async def get_async_response_json(url, session):
    global fetch_counter
    fetch_counter += 1
    async with session.get(url, proxy=proxy) as response:
        try:
            return await response.json()
        except BaseException as err:
            return "Can't obtain {} with ASYNC with error {} \n {}".format(url, err, response.text)


async def get_replay_from_listings(acr, lang, crid, session):
    url = url_constructor(acr, lang, listing.format(id=crid))
    now = dt.now()
    async with semaphore:
        try:
            response_json = await get_async_response_json(url, session)
            print(f'Fetching of {url} took {(dt.now() - now).total_seconds()} seconds')
            return crid, response_json['replayTvAvailable']
        except KeyError as err:
            print(err)
        except TypeError as err:
            print(err)


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
            channel_number, channel_name, replay_enabled = id_title[entry['o']]
        except KeyError:
            continue
        except ValueError:
            continue
        channel_title = "{}|{}".format(channel_number, channel_name)
        for prog in entry['l']:
            try:
                if replay_enabled:
                    if not prog['r']:
                        channel_prog.setdefault(channel_title,
                                                OrderedDict()).setdefault(prog['i'], [prog['t'], prog['s'],
                                                                                      prog['e'], orange])
                    else:
                        channel_prog.setdefault(channel_title,
                                                OrderedDict()).setdefault(prog['i'], [prog['t'], prog['s'],
                                                                                      prog['e'], blue])

                else:
                    channel_prog.setdefault(channel_title,
                                            OrderedDict()).setdefault(prog['i'], [prog['t'], prog['s'],
                                                                                  prog['e'], grey])
            except KeyError:
                missing_epg.setdefault(channel_title, []).append((prog['s'], prog['e']))

    return OrderedDict(sorted(channel_prog.items(), key=lambda x: int(x[0].split('|')[0]))),\
           OrderedDict(sorted(missing_epg.items(), key=lambda x: int(x[0].split('|')[0])))


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


async def get_color(channels_n_programms, acr, lang):
    session = ClientSession()
    tasks = list()

    for channel_title, programm_line in channels_n_programms.items():
        for crid, list_info in programm_line.items():
            if blue in list_info:
                task = asyncio.ensure_future(get_replay_from_listings(acr, lang, crid, session))
                tasks.append(task)
        # delete me!
        break
    print(f'Amount of async tasks: {len(tasks)}')
    response = await asyncio.gather(*tasks)

    await session.close()
    return response


def get_start():
    for acr, lang in acronym_lang.items():

        schedule_url = url_constructor(acr, lang, schedules)
        channel_url = url_constructor(acr, lang, channel)

        dates = get_dates(period, timeframe_type)

        id_title_channel = dict()
        channel_json = get_response_json(channel_url)
        try:
            for chnl in channel_json['channels']:
                channel_info = chnl['stationSchedules'][0]['station']
                try:
                    id_title_channel.setdefault(channel_info['id'], (chnl['channelNumber'], channel_info['title'],
                                                                     channel_info['replayTvEnabled']))
                except KeyError:
                    id_title_channel.setdefault(channel_info['id'], (channel_info['title'], None))

        except TypeError as err:
            print(channel_json)
            print(err)
            continue

        missing_epg = dict()
        overlap, gap = dict(), dict()
        channel_prog = dict()

        for date in dates:
            print("Schedule API for {acr} {date} will be processed".format(acr=acr, date=date))

            # API divides main info into 4 parts (~6 hours for each part)
            for part in range(1, 5):
                url = schedule_url + schedules_dates.format(date=date, part=part)

                api_response = get_response_json(url)
                try:
                    channel_prog, missing_epg = get_main_data(api_response, channel_prog, missing_epg,
                                                              id_title_channel)
                except TypeError as err:
                    print(api_response)
                    print(err)

        # !!! write FULL json
        with open(f'./static_files/preprod/line_{acr}_{today}.txt', 'w', encoding='utf-8') as file:
            file.write(json.dumps(channel_prog))

        print(f"line_{acr}_{today}.txt has been written")

        # overlap, gap = get_overlap_and_gap(channel_prog, overlap, gap)

        # with open('./static_files/missing_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
        #     file.write((json.dumps(missing_epg)))
        #
        # with open('./static_files/gap_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
        #     file.write((json.dumps(gap)))
        #
        # with open('./static_files/overlap_{}.txt'.format(acr), 'w', encoding='utf-8') as file:
        #     file.write((json.dumps(overlap)))


def get_n_fill_colors():

    for acr, lang in acronym_lang.items():

        schedule_url = url_constructor(acr, lang, schedules)
        channel_url = url_constructor(acr, lang, channel)

        date, hour = dt.today().strftime("%Y%m%d %H").split(' ')
        part = int(hour)//6 + 1

        id_title_channel = dict()
        channel_json = get_response_json(channel_url)
        try:
            for chnl in channel_json['channels']:
                channel_info = chnl['stationSchedules'][0]['station']
                try:
                    id_title_channel.setdefault(channel_info['id'], (chnl['channelNumber'], channel_info['title'],
                                                                     channel_info['replayTvEnabled']))
                except KeyError:
                    id_title_channel.setdefault(channel_info['id'], (channel_info['title'], None))

        except TypeError as err:
            print(channel_json)
            print(err)
            continue

        missing_epg = dict()
        channel_prog = dict()

        print(f"Schedule API for {acr} {date} {part} will be processed")

        url = schedule_url + schedules_dates.format(date=date, part=part)
        api_response = get_response_json(url)
        try:
            channel_prog, missing_epg = get_main_data(api_response, channel_prog, missing_epg,
                                                      id_title_channel)
        except TypeError as err:
            print(api_response)
            print(err)

        ioloop = asyncio.get_event_loop()

        replay_colors = ioloop.run_until_complete(get_color(channel_prog, acr, lang))
        print(f"Amount of async calls: {len(replay_colors)} with {fetch_counter} fetches")
        ioloop.close()

        with open(f'./static_files/preprod/line_{acr}_{today}.txt', 'r') as file:
            channel_prog = json.loads(file.read())
            try:
                for crid, replay_data in replay_colors:
                    for channel_title in channel_prog.keys():
                        if crid in channel_prog[channel_title]:
                            if replay_data:
                                channel_prog[channel_title][crid][3] = green
                            else:
                                channel_prog[channel_title][crid][3] = red
            except TypeError as err:
                print(err)

        with open(f'./static_files/preprod/line_{acr}_{today}.txt', 'w') as file:
            file.write(json.dumps(channel_prog))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-",
                        dest="arg",
                        default='',
                        type=str,
                        help='''Run with one of the following functions:
                              - "start" is getting start data (Schedule API);
                              - "fill" is getting and filling colorful data (Listing API)''')

    args = parser.parse_args()

    print('Start {}'.format(time.ctime()))

    # session initiate
    requests = requests.Session()

    if args.arg == 'start':
        get_start()
    elif args.arg == 'fill':
        get_n_fill_colors()
    else:
        print('Argument is mandatory!')
    requests.close()

    print("Finish {}".format(time.ctime()))
