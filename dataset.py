import pandas as pd
import requests
import gzip
import datetime
import re


def guess_type(x):
    # numeric type
    if re.match('^[+-]?[0-9\.]+$', x):
        return float(x)

    # default leaves alone
    return x


def load(blob):
    events = {}

    lines = gzip.decompress(blob).decode().splitlines()

    for line in lines:
        fields = line.split(';')

        timestamp = datetime.datetime.fromtimestamp(float(fields[1]) // 1000)
        # plugin = fields[3]
        sensor = fields[4]
        param = fields[5]
        value = guess_type(fields[6])

        if timestamp not in events:
            events[timestamp] = {}

        events[timestamp]['{}.{}'.format(sensor, param)] = value

    rows = list(pd.DataFrame(events).items())

    return pd.DataFrame([r[1] for r in rows], index=[r[0] for r in rows])


def load_from_url(url):
    r = requests.get(url)
    assert r.status_code == 200
    return load(r.content)
