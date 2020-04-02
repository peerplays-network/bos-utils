#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getch
import time
import numpy as np
import json
import os
import sys
import yaml
from peerplays import PeerPlays
from getpass import getpass
from pprint import pprint
import re


class EventCount():

    def __init__(self):
        self.helpText =\
            """
            """
        with open('config_mint_auto.yaml', 'r') as fid:
            config = yaml.safe_load(fid)
        self.config = config
        self.ppy = self.Ppy()

    def Ppy(self):
        self.ppy = PeerPlays(
            self.config['node'],
            proposer=self.config['proposer'],
            proposal_expiration=self.config['proposal_expiration'],
            nobroadcast=False,
            bundle=True
        )
        if 'password' in self.config:
            self.ppy.wallet.unlock(self.config['password'])
        else:
            self.ppy.wallet.unlock(getpass())
        return self.ppy

    def Count(self, eventGroup='1.21.13'):
        events = self.ppy.rpc.list_events_in_group(eventGroup)
        print('lenEvents:', len(events))
        print('lastEvent:', events[-1]['id'].split('.')[-1])
        pass 

if __name__ == "__main__":
    eventCount = EventCount()
