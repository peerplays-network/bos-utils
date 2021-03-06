#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import numpy as np
import json
import time
from multiprocessing import Pool

urlBase = 'https://dick-faucet.peerplays.download'
# urlBase = 'http://35.182.6.94:5000'
api = '/api/v1/accounts'
# api = '/api/v2/accounts'

url = urlBase + api


def JTest(name=None):
    jTemplate = {'account': {
        'name': 'qa3',
        'owner_key': 'TEST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV',
        'active_key': 'TEST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV',
        'memo_key': 'TEST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV',
        'refcode': '',
        'referrer': ''}}
    if isinstance(name, type(None)):
        name = 'j1-' + str(np.random.randint(100000000000000000))
    jTest = jTemplate
    jTest['account']['name'] = name
    return jTest

def Bombard(jTest):
    tic = time.time()
    try:
        r = requests.post(url, json=jTest, timeout=(300, 600))
        tocReq = time.time() - tic
        # print('time = ', time.time() - tic)
        text = r.text
        # print(jTest)
        textDict = json.loads(text)
        if 'account' in textDict:
            print('name:', textDict['account']['name'], tocReq, time.time() - tic)
            return (True, time.time(), tocReq)
            # return True, textDict
        else:
            print('FAILED:', text, tocReq, time.time() - tic)
            # return False, textDict
            return (False, time.time(), tocReq)
    except Exception as e:
        # print('text:', text)
        print('exception Type:', type(e))
        print('exception Args:', e.args)
        print('e', e)
        return (False, time.time(), 0)


def Bombards(count, numberOfProcesses):
    jTests = []
    for k in range(count):
        jTest = JTest()
        jTests.append(jTest)
    # resBombards = []
    # textDicts = []
    tic = time.time()
    p = Pool(processes=numberOfProcesses)
    print('starting pool map')
    r = p.map(Bombard, jTests)
    print('done pool map')
    p.close()
    print('closed pool')
    #r = list(map(Bombard, jTests))
    toc = time.time() - tic
    print('timePerCall = ', toc / count, 'succeesScore:', np.sum(r) * 100 / count)
    return r
#    for k in range(count):
#        jTest = jTests[k]
#        print(k, jTest)
#        resBombard, textDict = Bombard(jTest)
#        resBombards.append(resBombard)
#        textDicts.append(textDict)
#    return resBombards, textDicts

    

