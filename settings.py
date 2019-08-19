# Get data configs

PERIOD = 7
TIMEFRAME_TYPE = 'previous'
# TIMEFRAME_TYPE = 'around'

ACRONYM_LANG = {'NL': 'nld', 'AT': 'deu', 'CH': 'eng', 'CZ': 'ces', 'HU': 'eng', 'PL': 'pol', 'RO': 'eng', 'SK':'eng'}
# ACRONYM_LANG = {'NL': 'nld'}

SOURCE_URL = 'web-api-prod-obo.horizon.tv'
OESP_WEB = 'https://{source}/oesp/v3/{country_acr}/{language}/web/{api}'

CHANNEL = 'channels'
SCHEDULES = 'programschedules'
SCHEDULES_DATES = '/{date}/{part}'
LISTING = 'listings/{id}?byLocationId=65535'
STATIONS = 'stations'
