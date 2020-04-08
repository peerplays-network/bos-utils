#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import numpy as np
import json
import time
from multiprocessing import Pool

urlBase = 'https://dick-faucet.peerplays.download'
api = '/api/v1/accounts'

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
    r = requests.post(url, json=jTest)
    print('time = ', time.time() - tic)
    text = r.text
    # print(jTest)
    textDict = json.loads(text)
    if 'account' in textDict:
        print('name:', textDict['account']['name'])
        return True
        # return True, textDict
    else:
        print('FAILED:', text)
        # return False, textDict
        return False

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

    

