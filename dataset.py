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

        timestamp = datetime.datetime.strptime(fields[1], '%Y/%m/%d %H:%M:%S')
        # plugin = fields[3]
        sensor = fields[4]
        param = fields[5]
        value = guess_type(fields[6])

        if timestamp not in events:
            events[timestamp] = {}

        events[timestamp]['.'.join([sensor, param])] = value

    rows = list(pd.DataFrame(events).items())

    return pd.DataFrame([r[1] for r in rows], index=[r[0] for r in rows])


def load_from_file(filename):
    """Load a dataset from a file."""
    with open(filename, 'rb') as f:
        return load(f.read())


def load_from_url(url):
    """Load a dataset from a URL."""
    r = requests.get(url)
    assert r.status_code == 200
    return load(r.content)


def load_from_urls(urls):
    """Loads and concatenates multiple datasets from a list of URLs."""
    return pd.concat([load_from_url(url) for url in urls])
