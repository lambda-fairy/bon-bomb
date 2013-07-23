#!/usr/bin/env python3

import json
from urllib.request import urlopen

if __name__ == '__main__':
    s = urlopen('http://freegeoip.net/json/').read().decode('utf-8')
    data = json.reads(s)
    print('IP address is', data['ip'])
