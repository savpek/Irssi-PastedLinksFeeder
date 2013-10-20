#!/usr/bin/python

# Description: Script generates RSS from pasted links.
# Notes:
#    - Feed is generated from IRSSI log files.
#    - Script need access to irssi log path and www server folder.
#    - Set irssi log format '%d.%m.%y %H:%M'

import datetime
import os
import PyRSS2Gen
import time
import re

LOG_PATH = "/home/users/someuser/irclogs/"
OUTPUT_FILE = "/home/users/someuser/sites//www/ltpyamt9psoasksa232.xml"

rss = PyRSS2Gen.RSS2(
    title="Irc links",
    link="http://savpek.kapsi.fi/",
    description="",
    lastBuildDate=datetime.datetime.now(),
    items=[])


def get_logs(folder):
    result = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".log"):
                title = file.replace(".log", "")
                result.append({'name': title, 'contents': open(os.path.join(root, file), 'r').read()})
    return result


def get_item(logfile, logurl, logtime):
    return PyRSS2Gen.RSSItem(
        title="{0}, {1}".format(logfile, logurl),
        link=logurl,
        description=logurl,
        guid=PyRSS2Gen.Guid(logtime.strftime('%d.%m.%y %H:%M') + logfile + logurl),
        pubDate=logtime)

while True:
    rss.items = []

    logFiles = get_logs(LOG_PATH)

    for logFile in logFiles:
        matches = re.findall('(\d*?\.\d*?\.\d*? \d*?:\d*).*?(http.*?)[\n| ]', logFile['contents'], re.S)
        for match in matches:
            date = datetime.datetime.strptime(match[0], '%d.%m.%y %H:%M')
            rss.items.append(get_item(logFile['name'], match[1], date))

    rss.lastBuildDate = datetime.datetime.now()
    rss.write_xml(open(OUTPUT_FILE, "w"))

    print "Feed updated."
    time.sleep(60)