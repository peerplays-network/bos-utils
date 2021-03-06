#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bos_incidents import factory
from pprint import pprint
from dateutil import parser
import datetime as dt

class IncidentAnalytics():

    def __init__(self):
        self.storage = factory.get_incident_storage()
        self.providers = self.storage.get_distinct("provider_info.name")
        pass

    def EventsResultDone(self, begin=None, end=None, call='result'):
        eventsCursor = self.storage.get_events_by_call_status(call=call, status_name='done')
        eventsResultDone = []
        for eventCursor in eventsCursor:
            eventResultDone = self.storage.get_event_by_id(eventCursor['id_string'])
            if not isinstance(begin, type(None)):
                startTime = parser.parse(eventResultDone['id']['start_time']).replace(tzinfo=None)
                if startTime < begin:
                    continue
            if not isinstance(end, type(None)):
                startTime = parser.parse(eventResultDone['id']['start_time']).replace(tzinfo=None)
                if startTime > end:
                    continue
            eventsResultDone.append(eventResultDone)
        return eventsResultDone

    def ProvidersResult(self, event, fate='result'):
        if fate == 'result':
            calls = ['create', 'in_progress', 'finish', 'result']
        else:
            calls = ['create', 'canceled']
        providers = dict()
        for call in calls:
            providers[call] = []
            if call not in event:
                return set()
            incidents = event[call]['incidents']
            _providersList = []
            for incident in incidents:
                _providersList.append(incident['provider_info']['name'])
            providers[call] = set(_providersList)
        providersValues = providers.values()
        assert len(providersValues) == len(calls), 'no incidents for some calls'
        providersResult = set.intersection(*providersValues)
        return providersResult

    def ProvidersDict(self, events, fate='result'):
        providersDict = dict()
        for event in events:
            providersResult = self.ProvidersResult(event, fate=fate)
            for providerResult in providersResult:
                if providerResult not in providersDict:
                    providersDict[providerResult] = []
                providersDict[providerResult].append(event['id_string'])
        return providersDict

    def SumUp(self, providersDict):
        sumUp = dict()
        for providerName in providersDict.keys():
            sumUp[providerName] = len(providersDict[providerName])
        return sumUp

    def All(self, begin=None, end=None, fate='result'):
        if fate != 'result':
            fate = 'canceled'
        eventsResultDone = self.EventsResultDone(begin, end, call=fate)
        providersDict = self.ProvidersDict(eventsResultDone, fate=fate)
        sumUp = self.SumUp(providersDict)
        return sumUp


if __name__ == "__main__":
    incidentAnalytics = IncidentAnalytics()
    print('')
    print('Analytics for Settled events')
    settledAnalytics = incidentAnalytics.All(fate='result')
    pprint(settledAnalytics)

    print('')
    print('Anlytics for Canceled events')
    canceledAnalytics = incidentAnalytics.All(fate='canceled')
    pprint(canceledAnalytics)
# ------------------------------
    print('')
    print('Analytics for Settled events between two dates')
    settledAnalytics = incidentAnalytics.All(begin=dt.datetime(2020,1,1), end=dt.datetime(2020,2,28), fate='result')
    pprint(settledAnalytics)

    self = incidentAnalytics
