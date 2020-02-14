#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import json
import os
import sys
import yaml
from peerplays import PeerPlays
from getpass import getpass
from pprint import pprint
import re


def RemoveBraces(string):
    res = re.sub('{', '', string)
    res = re.sub('}', '', res)
    return res


class MintAuto():

    def __init__(self):
        self.helpText =\
            """
            This is a small script to automate proposals.
            The proposals automated are
            in_progress to finished and
            finsihed to settled
            The usage is
            python3 mint_auto finish <eventid>, <scoreHomeTeam>,<scoreAwayTeam>
            python3 mint_auto finish 1.22.199, 3,2
            python3 mint_auto settle <eventid>, <scoreHomeTeam>,<scoreAwayTeam>
            python3 mint_auto settle 1.22.199, 3,2
            """
        with open('config_mint_auto.yaml', 'r') as fid:
            config = yaml.safe_load(fid)
        self.config = config
        # self.ppy = PeerPlays(config['node'])
        # self.ppy.wallet.unlock(getpass())

    def InProgress(self, eventIds):
        self.ppy = PeerPlays(self.config['node'])
        self.ppy.wallet.unlock(getpass())
        self.proposal = self.ppy.proposal(
            proposer=self.config['proposer'],
            proposal_expiration=self.config['proposal_expiration'])
        eventIds = eventIds.replace(' ', '')
        eventIds = eventIds.split(',')
        for eventId in eventIds:
            print(eventId)
            self.ppy.event_update_status(
                event_id=eventId, status="in_progress",
                append_to=self.proposal)
        pprint(self.proposal.broadcast())

    def Finish(self, eventId, scores="test"):
        self.ppy = PeerPlays(
            self.config['node']
        )
        self.ppy.wallet.unlock(getpass())
        self.proposal = self.ppy.proposal(
            proposer=self.config['proposer'],
            proposal_expiration=self.config['proposal_expiration'])
        self.ppy.event_update_status(
            event_id=eventId, status="finished", scores=scores,
            append_to=self.proposal)
        """event_id=eventId, status="finished",
        scores=["2,1"], append_to=proposal)"""
        pprint(self.proposal.broadcast())

    def Ppy(self):
        self.ppy = PeerPlays(
            self.config['node'],
            proposer=self.config['proposer'],
            proposal_expiration=self.config['proposal_expiration'],
            nobroadcast=False,
            bundle=True
        )
        self.ppy.wallet.unlock(getpass())
        return self.ppy

    def Proposal(self):
        self.proposal = self.ppy.proposal(
            proposer=self.config['proposer'],
            proposal_expiration=self.config['proposal_expiration'])
        return self.proposal

    def Bms(self, ppy, bmg):
        bms = ppy.rpc.list_betting_markets(bmg)
        return bms

    def Rule(self, ppy, ruleId):
        ruleAll = ppy.rpc.get_object(ruleId)
        self._ruleAll = ruleAll
        metric = json.loads(ruleAll['description'][1][1])['metric']
        resolutions = json.loads(ruleAll['description'][1][1])['resolutions']
        metric = RemoveBraces(metric)
        for resolution in resolutions:
            for key in resolution.keys():
                resolution[key] = RemoveBraces(resolution[key])
        return metric, resolutions

    def Result(self, score):
        class ResultClass():
            def __init__(self, score):
                self.hometeam = score[0]
                self.awayteam = score[1]
                self.total = score[0] + score[1]
        result = ResultClass(score)
        return result

    def Resolution(self, metric, resolution, bm):
        keys = list(resolution.keys())
        logic = resolution.values()
        logic = list(map(eval, logic))
        if sum(logic) != 1:
            raise Exception('More than one condition is valid in resolution')
        whereTrue = np.where(logic)[0][0]
        keyTrue = keys[whereTrue]
        resolution = [bm['id'], keyTrue]
        #  resolution = ['whatever', keyTrue]
        return resolution

    def Resolutions(self, metric, resolutions, bms):
        self._resolutions = resolutions
        self._bms = bms
        if len(resolutions) < len(bms):
            raise Exception(
                "Length of resolutions doesn't match with lenght of bms")
        resolves = []
        for k in range(len(bms)):
            resolve = self.Resolution(metric, resolutions[k], bms[k])
            resolves.append(resolve)
        return resolves

    def SettleBmg(self, bmg, score, ppy):
        self._bmg = bmg
        rulesId = bmg['rules_id']
        metric, resolutions = self.Rule(ppy, rulesId)
        self._metric = metric
        result = self.Result(score)
        if result:  # dummy line to remove PEP warning
            metric = eval(metric)
        bms = ppy.rpc.list_betting_markets(bmg['id'])
        self._bms = bms
        resolves = self.Resolutions(metric, resolutions, bms)
        self._resolves = resolves
        ppy.betting_market_resolve(bmg['id'], resolves)

    def SettleScore(self, eventId, score):
        if type(eventId) != str:
            raise Exception('eventId should be a string')
        if len(eventId.split('.')) != 3:
            raise Exception(
                'eventId should have three numbers separated by a .')
        if eventId.split('.')[0] != '1' and \
                eventId.split('.')[1] != '22':
            raise Exception('Argument is not a valid eventId')
        ppy = self.Ppy()
        #  proposal = self.Proposal()
        #  eventDetails = ppy.rpc.get_object(eventId)
        #  eventName = eventDetails['name'][0][1]
        #  teams = eventName.split(' v ')
        #  self.eventDetails = eventDetails
        bmgs = self.ppy.rpc.list_betting_market_groups(eventId)
        self.bmgs = bmgs
        k = 0
        for bmg in bmgs:
            k += 1
            print('bmg', k, '/', len(bmgs))
            self.SettleBmg(bmg, score, ppy)
        ppy.txbuffer.broadcast()
        print('Proposal broadcasted to settle', eventId)

    def Settle(self, eventIds):
        eventIds = eventIds.replace(' ', '')
        eventIds = eventIds.split(',')
        self.ppy = PeerPlays(
            self.config['node'],
            proposer=self.config['proposer'],
            proposal_expiration=300,
            nobroadcast=False,
            bundle=True
        )
        self.ppy.wallet.unlock(getpass())
        self.proposal = self.ppy.proposal(
            proposer=self.config['proposer'],
            proposal_expiration=self.config['proposal_expiration'])
        for eventId in eventIds:
            print(eventId)
            eventDetails = self.ppy.rpc.get_object(eventId)
            print(eventDetails)
            self._eventDetails = eventDetails
            eventName = eventDetails['name'][0][1]
            teams = eventName.split(' v ')
            bmgs = self.ppy.rpc.list_betting_market_groups(eventId)
            kBmg = 0
            lenBmgs = len(bmgs)

            for bmg in bmgs:
                kBmg += 1
                # pprint(bmg['id'])
                pprint(bmg)
                pprint(teams)
                print(' ')
                bms = self.ppy.rpc.list_betting_markets(bmg['id'])
                result = []
                for k in range(len(bms)):
                    print('Index: ', k)
                    pprint(bms[k])
                    print('   ')
                    result.append([bms[k]['id'], 'not_win'])
                option = input(
                    str(kBmg) + '/' + str(lenBmgs) +
                    'Enter the winner index or most suitable bm index: ')
                result[int(option)][1] = 'win'
                self._result = result
                self._bmg = bmg
                self.ppy.betting_market_resolve(bmg['id'], result)
                os.system('clear')
        self.ppy.txbuffer.broadcast()
        # pprint(self.ppy.txbuffer.broadcast())
        # self.ppy.event_update_status(
        #        event_id=eventId, status="settled", append_to=self.proposal)
        # event_id=eventId, status="finished",
        # scores=["2,1"], append_to=proposal)
        # pprint(self.proposal.broadcast())


if __name__ == "__main__":
    mintAuto = MintAuto()
    if len(sys.argv) == 1:
        print(mintAuto.helpText)
        #  print('init object')
    elif len(sys.argv) >= 3:
        method = sys.argv[1]
        eventIds = sys.argv[2]
        print('method:', method, '  eventId:', eventIds)

        if method == "in_progress":
            mintAuto.InProgress(eventIds)
        elif method == 'finish':
            if len(sys.argv) >= 4:
                scores = sys.argv[3]
            else:
                scores = []
            mintAuto.Finish(eventIds, scores)
        elif method == 'settle':
            if len(sys.argv) != 4:
                print(
                    """Add score to argumenets in""",
                    """[homeTeam, awayTeam], for eg [4, 2]"""
                )
                raise Exception("Score missing in arguments")
            score = eval(sys.argv[3])
            mintAuto.SettleScore(eventIds, score)
        else:
            print('Wrong command')
            print(mintAuto.helpText)
    else:
        print(mintAuto.helpText)
