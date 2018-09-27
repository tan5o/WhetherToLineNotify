#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import urllib.parse
import urllib.request
import datetime
import os

# weather's API
WEATHER_URL="http://weather.livedoor.com/forecast/webservice/json/v1?city=%s"
CITY_CODE="130010" # TOKYO

# LINE notify's API
LINE_TOKEN= os.environ.get("LINE_NOTIFY_API_KEY")
LINE_NOTIFY_URL="https://notify-api.line.me/api/notify"

def get_weather_info():
    try:
        url = WEATHER_URL % CITY_CODE
        html = urllib.request.urlopen(url)
        html_json = json.loads(html.read().decode('utf-8'))
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)
    return html_json

def set_weather_info(weather_json, day):
    min_temperature = None
    max_temperature = None
    try:
        weather = weather_json['forecasts'][day]['telop']
        max_temperature = weather_json['forecasts'][day]['temperature']['max']['celsius']
        min_temperature = weather_json['forecasts'][day]['temperature']['min']['celsius']
    except TypeError:
        # temperature data is None etc...
        pass
    msg = "\n天気: %s\n最低気温: %s\n最高気温: %s" % \
               (weather, min_temperature, max_temperature)
    return msg

def send_weather_info(msg):
    method = "POST"
    headers = {"Authorization": "Bearer %s" % LINE_TOKEN}
    payload = {"message": msg}
    try:
        payload = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(
            url=LINE_NOTIFY_URL, data=payload, method=method, headers=headers)
        urllib.request.urlopen(req)
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)

def OtenkiNotify():
    weather_json = get_weather_info()

    now = datetime.datetime.now() + datetime.timedelta(hours=9) ## GMT+9:00
    weekday = now.weekday()
    yobi = ["月", "火", "水", "木", "金", "土", "日"]
    msg_header = "\n本日" + str(now.date()) +"(" + yobi[weekday] + ")"

    msg = set_weather_info(weather_json, 0)
    print (msg_header + msg)
    send_weather_info(msg_header + msg)
    if("雨" in weather_json['forecasts'][0]['telop']):
        send_weather_info(msg_header+"\n☔☔☔☔☔☔☔☔\n今日は雨が降ります。\n傘を忘れずに！\n☔☔☔☔☔☔☔☔")