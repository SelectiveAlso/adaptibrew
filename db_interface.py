#!/usr/bin/env python
import exchange
from exchange import Info
from exchange import Setting
from exchange import Request
import time
import settings

db = exchange.connect()

if not Info.table_exists():
    db.create_tables([Info])

if not Setting.table_exists():
    db.create_tables([Setting])

if not Request.table_exists():
    db.create_tables([Request])

exchange.write_settings()

while True:
    exchange.write_latest_data()
    exchange.check_for_requests()
    time.sleep(0.5)
