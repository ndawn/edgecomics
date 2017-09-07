#!/usr/bin/python3


import os


curdir = os.path.realpath('.')

bind = 'unix:/tmp/edgecomics.sock'

workers = 5
timeout = 7200
preload = True
daemon = True
pidfile = '/tmp/edgecomics.pid'

accesslog = os.path.join(curdir, 'logs/access.log')
errorlog = os.path.join(curdir, 'logs/error.log')
loglevel = 'debug'
capture_output = True
