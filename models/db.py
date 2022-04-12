# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
from gluon import current


# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig()

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'],
             lazy_tables=True)
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))
current.auth_user = auth.user

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = [Field('top_ten_picks', type='list:string', writable=False, readable=False, default=["Default"]),
                                           Field('is_active', type='boolean', writable=False, readable=False),
                                           Field('season_points', type='integer', writable=False, readable=False, default=0),
                                           Field('league', type='integer', writable=False, readable=False),
                                           Field('twenty_one_points', type='integer', writable=False, readable=False, default=0),
                                           Field('twenty_one_placement', type='string', writable=False, readable=False)]
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
#mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.server = 'smtp.gmail.com:465'
#mail.settings.sender = configuration.get('smtp.sender')
mail.settings.sender = 'gskent7@gmail.com'
#mail.settings.login = 'configuration.get('smtp.login')'
mail.settings.login = 'gskent7@gmail.com:eglcvighfeyfjoqd'
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
auth.settings.expiration = 3600
auth.settings.remember_me_form = False

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
#auth.enable_record_versioning(db)


db.define_table('tier_one_field',
                Field('player_name', type='string'),
                Field('player_rank', type='string'),
                format='(%(player_rank)s) %(player_name)s'
                )

db.define_table('tier_two_field',
                Field('player_name', type='string'),
                Field('player_rank', type='string'),
                format='(%(player_rank)s) %(player_name)s'
                )

db.define_table('tier_three_field',
                Field('player_name', type='string'),
                Field('player_rank', type='string'),
                format='(%(player_rank)s) %(player_name)s'
                )

db.define_table('events',
                Field('league_name', type='string', requires = IS_NOT_EMPTY()),
                Field('season', type='string', requires = [IS_NOT_EMPTY(),
                                                           IS_INT_IN_RANGE(2020, 3000)]),
                Field('event_number', type='string', requires = IS_NOT_EMPTY()),
                Field('tournament_name', type='string', requires = IS_NOT_EMPTY()),
                Field('starting_date', type='string'),
                Field('completed', type='boolean'),
                Field('ready', type='boolean'),
                Field('playing', type='boolean'),
                Field('logo', type='string'),
                Field('course_img', type='string'),
                format='%(league_name)s - %(tournament_name)s (%(season)s)'
                )

db.define_table('picks',
                Field('user_id', db.auth_user, writable=False),
                Field('event_id', db.events, writable=False),
                Field('pick_one', db.tier_one_field, ondelete="NO ACTION"),
                Field('one_name', type='string', writable=False, readable=False),
                Field('one_points', type='integer', default=0, writable=False, readable=False),
                Field('pick_two', db.tier_two_field, ondelete="NO ACTION"),
                Field('two_name', type='string', writable=False, readable=False),
                Field('two_points', type='integer', default=0, writable=False, readable=False),
                Field('pick_three', db.tier_two_field, ondelete="NO ACTION"),
                Field('three_name', type='string', writable=False, readable=False),
                Field('three_points', type='integer', default=0, writable=False, readable=False),
                Field('pick_four', db.tier_three_field, ondelete="NO ACTION"),
                Field('four_name', type='string', writable=False, readable=False),
                Field('four_points', type='integer', default=0, writable=False, readable=False),
                Field('pick_five', db.tier_three_field, ondelete="NO ACTION"),
                Field('five_name', type='string', writable=False, readable=False),
                Field('five_points', type='integer', default=0, writable=False, readable=False),
                Field('total_points', type='integer', default=0, writable=False, readable=False)
                )
