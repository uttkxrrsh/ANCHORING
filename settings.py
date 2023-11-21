from os import environ

SESSION_CONFIGS = [
    dict(
        name='BASIC',
        app_sequence=['BASIC'],
        num_demo_participants=2,
    ),
    dict(name ='COMPLEX',
         app_sequence=['COMPLEX'],
         num_demo_participants=2,
         ),
    dict(name = 'CONTROLB',
         app_sequence=['CONTROLB'],
         num_demo_participants=2,
         ),
    dict(name = 'CONTROLC',
            app_sequence=['CONTROLC'],
            num_demo_participants=2,
            ),
    dict(name = 'mpl',
         display_name = 'Multiple Price List (Holt/Laury)',
         num_demo_participants=1,
            app_sequence=['mpl'],
            ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9026458176029'
