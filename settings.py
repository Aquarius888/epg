# Get data configs

PERIOD = 3
TIMEFRAME_TYPE = 'previous'
# TIMEFRAME_TYPE = 'around'

# ACRONYM_LANG = {'NL': 'nld',
#                 'AT': 'deu',
#                 'CH': 'eng',
#                 'CZ': 'ces',
#                 'HU': 'eng',
#                 'PL': 'pol',
#                 'RO': 'eng',
#                 'SK': 'eng',
#                 'UK': 'eng',
#                 'BE': 'eng',
#                 'DE': 'deu'}
ACRONYM_LANG = {'NL': 'nld'}

PROD = {'NL': 'nld', 'AT': 'deu', 'CH': 'eng', 'UK': 'eng', 'BE': 'eng', 'IE': 'eng'}
SUGAR = {'CL': 'spa', 'PR': 'eng'}
PEP_N_SALT = {'NL': 'nld', 'AT': 'deu', 'CH': 'eng', 'CZ': 'ces',
              'HU': 'eng', 'PL': 'pol', 'RO': 'eng', 'SK': 'eng',
              'UK': 'eng', 'BE': 'eng', 'DE': 'deu', 'IE': 'eng'}

PROD_URL = 'prod-obo'
PREPROD_URL = 'preprod-obo'
SUGAR_URL = 'sugar'
PEPPER_URL = 'pepper'
SALT_URL = 'salt'

OESP_WEB = 'https://web-api-{source}.horizon.tv/oesp/v3/{country_acr}/{language}/web/{api}'
# for test run
PREPROD_OESP_WEB = 'https://pp-api.oesp.horizon.tv/oesp/v3/{country_acr}/{language}/web/{api}'

CHANNEL = 'channels'
SCHEDULES = 'programschedules'
SCHEDULES_DATES = '/{date}/{part}'

# SCHEDULES = 'programschedules/{date}/{part}'

LISTING = 'listings/{id}?byLocationId=65535'
STATIONS = 'stations'
