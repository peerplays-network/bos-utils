#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as dt
import requests
import json
from pprint import pprint


def ManufactureHead(timeDt):
    timeIso = timeDt.isoformat()
    return timeIso


class RemoteControl():
    def __init__(self):
        self.urlBos1 = "http://35.183.41.242:8010/trigger"
        self.urlBos2 = "http://54.93.116.158:8010/trigger"
        self.urlBos3 = "http://52.62.37.137:8010/trigger"
        self.timeDeltaHrs = 1
        self.remotes = dict()
        self.remotes['174'] = 'http://174.138.14.239:8010/replay'
        self.remotes['149'] = 'http://149.56.89.138:8010/replay'
        self.remotes['yam'] = 'http://95.216.65.79:8010/replay'
        self.remotes['h1'] = 'http://h1.couchpotato.network/replay'
        self.remotes['h2'] = 'http://h2.couchpotato.network/replay'
#        self.params = {'manufacture':
#                       '2020-01-11T20:00:00Z__Soccer__SerieA__Bologna_\
#                       Cagliari__create__2020',
#                       'restrict_witness_group': 'elizabeth',
#                       'token': 'pbsabookie'}
        self.params = {'manufacture':
                       '2020-01-11T20:00:00Z__Soccer__\
                       EPL__Manchester City__Arsenal__\
                       create__2020',
                       'restrict_witness_group': 'elizabeth',
                       'token': 'pbsabookie'}
#        self.manufactureTail = \
#            'Z__Basketball__NBA Regular Season__Chicago Bulls__Cleveland Cavaliers__create__2021'
#        self.manufactureTail = \
#            'Z__Ice Hockey__NHL Regular Season__Dallas Stars__New York Rangers__create_2020'
#        self.manufactureTail = \
#            'Z__Soccer__EPL__Manchester City__Arsenal__create__2020'
        self.manufactureTail = \
            'Z__Soccer__SerieA__Bologna__Cagliari__create__2020'
        pass

    def Params(self, timeDt):
        self._timeIso = ManufactureHead(timeDt)
        self.params['manufacture'] = self._timeIso + self.manufactureTail
        return self.params

    def Create(self, remote, timeDt):
        self.params = self.Params(timeDt)
        self._r = requests.get(url=remote, params=self.params)
        # return self._r.ok
        return self._r

    def TimeDeltaHrs(self, timeDeltaHrs):
        timeDt = dt.datetime.now() + dt.timedelta(hours=timeDeltaHrs)
        return timeDt

    def EventsSetBy(self, numberOfEvents):
        self._times = []
        for k in range(numberOfEvents):
            timeDeltaHrs = k + 1
            timeDt = self.TimeDeltaHrs(timeDeltaHrs)
            self.timeDt = timeDt
            self._times.append(timeDt)
        for timeDt in self._times:
            self.Create(self.remotes['149'], timeDt)
            print(k, '/', numberOfEvents, '149')
        for timeDt in self._times:
            self.Create(self.remotes['174'], timeDt)
            print('174 ,', timeDt)

    def TriggerLocal(self):
        timeDeltaHrs = self.timeDeltaHrs
        timeDt = dt.datetime.now() + dt.timedelta(hours=timeDeltaHrs)
        r = self.Create(self.remotes['174'], timeDt)
        self._r = r
        pprint(r.text)
        rj = json.loads(r.text)
        incident = rj['incidents'][0]
        incident['provider_info']['name'] = 'jemshid'
        rBos1 = requests.post(self.urlBos1, json=incident)
        rBos2 = requests.post(self.urlBos2, json=incident)
        rBos3 = requests.post(self.urlBos3, json=incident)
        incident['provider_info']['name'] = 'ragnarDanneskjold'
        rBos1 = requests.post(self.urlBos1, json=incident)
        rBos2 = requests.post(self.urlBos2, json=incident)
        rBos3 = requests.post(self.urlBos3, json=incident)


    def EventEnter(self, timeDt):
        # self.Create(self.remotes['yam'], timeDt)
        # print('yam called')
        self.Create(self.remotes['149'], timeDt)
        print('149 called')
        self.Create(self.remotes['h1'], timeDt)
        print('h1 called')
        self.Create(self.remotes['h2'], timeDt)
        print('h2 called')
        # self.Create(self.remotes['174'], timeDt)
        # print('174 called')

    def EventsEnter(self, numberOfEvents):
        for k in range(numberOfEvents):
            timeDeltaHrs = k + 24
            timeDt = dt.datetime.now() + dt.timedelta(hours=timeDeltaHrs)
            self.timeDt = timeDt
            self.EventEnter(timeDt)
            print(k, '/', numberOfEvents, timeDt)


if __name__ == '__main__':
    remoteControl = RemoteControl()
