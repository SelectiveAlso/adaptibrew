#!/usr/bin/env python
from peewee import *
import os
import omegacn7500
import settings
import str116
import time

db_dir = os.path.expanduser("~/.brewer/db/")
db_file = "exchange.db"
db = SqliteDatabase(db_dir + db_file)
omega = omegacn7500.OmegaCN7500(settings.port, settings.rimsAddress)


# Models
class Info(Model):
    pv = DecimalField()
    sv = DecimalField()
    pid_running = BooleanField()
    hltToMash = BooleanField()
    hlt = BooleanField()
    rimsToMash = BooleanField()
    pump = BooleanField()
    timestamp = DecimalField()

    class Meta:
        database = db

class Request(Model):
    method = CharField()
    args = CharField()
    timestamp = DecimalField()

    class Meta:
        database = db

class Setting(Model):
    port = CharField()
    rimsAddress = IntegerField()
    switchAddress = IntegerField()
    baudRate = DecimalField()
    timeout = DecimalField()
    MA0 = CharField()
    MA1 = CharField()
    MAE = CharField()
    CN = CharField()
    hltToMash = IntegerField()
    hlt = IntegerField()
    rimsToMash = IntegerField()
    pump = IntegerField()
    webhook_url = CharField()
    DEBUG = BooleanField()

    class Meta:
        database = db

def connect():
    create_brewer_dir()
    create_db_dir()
    db.connect()
    return db

def create_brewer_dir():
    brewer_dir = os.path.expanduser("~") + "/.brewer/"
    if not os.path.exists(brewer_dir):
        os.makedirs(brewer_dir)

def create_db_dir():
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

def delete_db():
    if os.path.isfile(db_dir + db_file):
        os.remove(db_dir + db_file)
        return True
    else:
        return False

def recent(timestamp):
    if time.time() - 5 < timestamp:
        return True
    else:
        return False

def write_settings():

    try:
        if Setting.get().webhook_url:
            webhook = Setting.select().order_by(Setting.id.desc()).get().webhook_url
    except Setting.DoesNotExist:
        webhook = ""

    settings_record = Setting(
        port=str(settings.port),
        rimsAddress=int(settings.rimsAddress),
        switchAddress=int(settings.switchAddress),
        baudRate=float(settings.baudRate),
        timeout=float(settings.timeout),
        MA0=str(settings.MA0),
        MA1=str(settings.MA1),
        MAE=str(settings.MAE),
        CN=str(settings.CN),
        hltToMash=int(settings.relays['hltToMash']),
        hlt=int(settings.relays['hlt']),
        rimsToMash=int(settings.relays['rimsToMash']),
        pump=int(settings.relays['pump']),
        webhook_url=webhook,
        DEBUG=settings.DEBUG
    )
    settings_record.save()


def write_latest_data():
    info = Info(
        pv=omega.get_pv(),
        sv=omega.get_setpoint(),
        pid_running=omega.is_running(),
        hltToMash=str116.get_relay(settings.relays['hltToMash']),
        hlt=str116.get_relay(settings.relays['hlt']),
        rimsToMash=str116.get_relay(settings.relays['rimsToMash']),
        pump=str116.get_relay(settings.relays['pump']),
        timestamp=time.time(),
    )
    db.begin()
    try:
        info.save()
    except ErrorSavingData:
        db.rollback()
    db.commit()

def check_for_requests():
    try:
        request = Request.select(Request, fn.MAX(Request.timestamp)).get()
        if recent(request.timestamp):
            # Execute request
            execute(request.method, request.args)
    except Info.DoesNotExist:
        return False


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
