#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

urlsBase = [
    "http://174.138.14.239:8010/replay?token=pbsabookie&restrict_witness_\
group=elizabeth&manufacture=2020-04-01T20:00:00Z_",
    "http://149.56.89.138:8010/replay?token=pbsabookie&restrict_witness_\
group=elizabeth&manufacture=2020-04-01T20:00:00Z_"
]

urlsEvent = [
    "_Soccer__SerieA__Bologna__Cagliari_",
    "_basketball__nba__Brooklyn__Detroit_",
    "_Soccer__Epl__Chelsea__Brighton_",
    "_Soccer__SerieA__Lazio__Parma_",
    "_Basketball__NBA Playoffs__Orlando Magic__Toronto Raptors_",
    "_Baseball__MLB__New York Yankees__Minnesota Twins_",
    "_Baseball__MLB__Los Angeles Angels__Oakland Athletics_",
    "_Baseball__MLB__San Francisco Giants__Arizona Diamondbacks_",
    "_baseball__mlb-regular-season__tampa-bay-rays__new-york-yankees_",
    "_Baseball__MLB__Los Angeles Angels__Oakland Athletics_"
]

urlsAction = [
    "_create__2020",
    "_in_progress__2020-04-01T200000z",
    "_result__2__3"
]


class RemoteTest():

    def __init__(self):
        pass

    def Trigger(self, baseI, eventI, actionI):
        url = urlsBase[baseI] + urlsEvent[eventI] + urlsAction[actionI]
        print("remoteUrl:", urlsBase[baseI])
        print("event:", urlsEvent[eventI])
        print("action:", urlsAction[actionI])
        self._url = url
        print("url:", url)
        r = requests.get(url)
        print("returned:", r.text)


if __name__ == "__main__":
    remoteTest = RemoteTest()
