import sqlite3
import os
from os.path import expanduser
import omegacn7500
import settings
import str116
import time

db_dir = expanduser("~/.brewer/db/")
db_file = "exchange.db"

db = sqlite3.connect(db_dir + db_file)

omega = omegacn7500.OmegaCN7500(settings.port, settings.rimsAddress)


# Models
# class Info(Model):
#     pv = DecimalField()
#     sv = DecimalField()
#     pid_running = BooleanField()
#     hltToMash = BooleanField()
#     hlt = BooleanField()
#     rimsToMash = BooleanField()
#     pump = BooleanField()
#     timestamp = DecimalField()

#     class Meta:
#         database = db

# class Request(Model):
#     method = CharField()
#     args = CharField()
#     timestamp = DecimalField()

#     class Meta:
#         database = db




def connect():
    create_brewer_dir()
    create_db_dir()
    return db

def create_brewer_dir():
    brewer_dir = expanduser("~") + "/.brewer/"
    if not os.path.exists(brewer_dir):
        os.makedirs(brewer_dir)

def create_db_dir():
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

def create_info_table():
    db.execute("""create table if not exists info
        (
            pv REAL NOT NULL,
            sv REAL NOT NULL,
            pid_running INTEGER NOT NULL,
            hltToMash INTEGER NOT NULL,
            hlt INTEGER NOT NULL,
            rimsToMash INTEGER NOT NULL,
            pump INTEGER NOT NULL,
            timestamp REAL NOT NULL
        );
    """)

def create_request_table():
    db.execute("""create table if not exists request
        (
            method TEXT,
            args TEXT,
            timestamp REAL NOT NULL
        );
    """)

def delete_db():
    if os.path.isfile(db_dir + db_file):
        os.remove(db_dir + db_file)
        return True
    else:
        return False

def recent(timestamp):
    if time.time() - 3 < timestamp:
        return True
    else:
        return False


def write_latest_data():
    # info = Info(
    #     pv = omega.get_pv(),
    #     sv = omega.get_setpoint(),
    #     pid_running = omega.is_running(),
    #     hltToMash = str116.get_relay(settings.relays['hltToMash']),
    #     hlt = str116.get_relay(settings.relays['hlt']),
    #     rimsToMash = str116.get_relay(settings.relays['rimsToMash']),
    #     pump = str116.get_relay(settings.relays['pump']),
    #     timestamp = time.time(),
    # )
    db.execute("""
        INSERT INTO info (pv, sv, pid_running, hltToMash, hlt, rimsToMash, pump, timestamp)
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        );
    """ % (omega.get_pv(), omega.get_setpoint(), omega.is_running(),
           str116.get_relay(settings.relays['hltToMash']),
           str116.get_relay(settings.relays['hlt']),
           str116.get_relay(settings.relays['rimsToMash']),
           str116.get_relay(settings.relays['pump']), time.time()))

# def check_for_requests():
#     try:
#         request = Request.select(Request, fn.MAX(Request.timestamp)).get()
#         if recent(request.timestamp):
#             # Execute request
#             execute(request.method, request.args)
#     except Info.DoesNotExist:
#         return False


def parse_args(args):
    return args.split()

def execute(request, args=""):
    args = parse_args(args)
    # there's a better way to do this...
    if request == "set_relay":
        str116.set_relay(int(args[0]), int(args[1]))
    if request == "set_sv":
        omega.set_setpoint(float(args[0]))
    if request == "set_pid_on":
        omega.run()
    if request == "set_pid_off":
        omega.stop()
