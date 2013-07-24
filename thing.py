#!/usr/bin/env python3
"""
Pony Haxxinator 3000
by Lambda Fairy (github.com/lfairy)
(c) so much it hurts
"""

import json
from itertools import count
from random import random
from threading import Thread, current_thread
from time import sleep
from urllib.request import urlopen

BEST_PONY = 'Rarity'  # XXX DO NOT CHANGE THIS LINE

# Set this too low, and best pony will lose.
# Set this too high, and your computer crashes.
# Decisions, decisions.
PARALLELIZM = 50

NAMES = ['Twilight Sparkle', 'Rainbow Dash', 'Pinkie Pie', 'Fluttershy', 'Applejack', 'Rarity']

URL_TEMPLATE = 'http://www.hubworld.com/api/index.php?method=answerPoll&questionId=6cf8294f-e87c-4b73-a59a-75936fc6e678&answerId=6cf8294f-e87c-4b73-a59a-75936fc6e678_{}'


def name_spinner():
    """Yield a bunch of names, all beginning with Bob."""
    for i in count():
        yield 'Bob-' + str(i)


def interpolate(pony):
    """Turn a pony name into a URL."""
    pony_id = NAMES.index(pony)
    return URL_TEMPLATE.format(pony_id)


def processify(data):
    """Given a bytes object, return a dict mapping each pony to its
    number of votes."""
    data = json.loads(data.decode('utf-8'))
    def streamyolo():
        for blob in data['answers']:
            pony_id = int(blob['answerId'].split('_')[1])
            count = int(blob['count'])
            yield NAMES[pony_id], count
    return dict(streamyolo())


def regurgitate(status):
    """Dump the return value of processify() in a pony-readable format."""
    entries = list(status.items())
    entries.sort(key=lambda entry: entry[1], reverse=True)

    for pony, count in entries:
        print('{:>20}: {:>6}'.format(pony, count))


def loopdaloop(best_pony):
    cl_name = current_thread().name

    def log(msg, *args):
        print('[{}]'.format(cl_name), msg.format(*args))

    while True:
        sleep(random()*3)
        try:
            log('Sending vote...')
            data = urlopen(interpolate(best_pony)).read()
            status = processify(data)
            print()
            log('Vote for {} locked in!', best_pony.upper())
            print('Current votes:')
            regurgitate(status)
            print()
        except Exception as ex:
            log('** {!r}', ex)


if __name__ == '__main__':
    print(__doc__)
    print('Preparing to deploy {} changelings'.format(PARALLELIZM))
    print('{} is best pony ({})'.format(BEST_PONY, 'bwahaha' if BEST_PONY == 'Rarity' else 'traitor!'))
    names = name_spinner()
    for i in range(PARALLELIZM):
        changeling = Thread(target=loopdaloop, name=next(names), args=[BEST_PONY])
        changeling.start()
