#!/usr/bin/env python
import exchange
import time

db = exchange.connect()

exchange.create_info_table()
exchange.create_request_table()

exchange.write_latest_data()

# while True:
#     exchange.write_latest_data()
#     exchange.check_for_requests()
#     time.sleep(0.5)
