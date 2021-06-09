from os import environ


SESSION_CONFIGS = [
    dict(
        name='public_goods',
        app_sequence=['public_goods', 'payment_info'],
        num_demo_participants=3,
    ),
    dict(
        name='guess_two_thirds',
        display_name="Guess 2/3 of the Average",
        app_sequence=['guess_two_thirds', 'payment_info'],
        num_demo_participants=3,
    ),
    dict(
        name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    ),
    dict(
        name='my_survey_test',
        display_name='MattTest123',
        num_demo_participants = 3,
        app_sequence=['my_survey_test']
    ),

    dict(
        name='sumcalc',
        display_name='Sum Calculation',
        num_demo_participants=3,
        app_sequence=['my_survey_test']
    ),

    dict(
        name='imagelike',
        display_name='Like an Image',
        num_demo_participants=3,
        app_sequence=['my_survey_test']
    ),

    dict(
        name='visualtrace',
        display_name='Visual Trace',
        num_demo_participants=3,
        app_sequence=['my_survey_test']
    ),

dict(
        name='check_VT',
        display_name='check_VT',
        num_demo_participants=3,
        app_sequence=['check_VT']
    ),

dict(
        name='CausalDetermine',
        display_name='CausalDetermine',
        num_demo_participants=3,
        PARTICIPANT_FIELDS=['InfoOrder', 'ParticipantNum'],
        app_sequence=['CausalDetermine']
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '4996418643569'

INSTALLED_APPS = ['otree']
