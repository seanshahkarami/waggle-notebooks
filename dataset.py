import pandas as pd
from contextlib import suppress


def read_dataset(url):
    column_names = ['node_id', 'timestamp', 'plugin', 'topic', 'sensor', 'param', 'value']
    return pd.read_csv(url, sep=';', names=column_names, parse_dates=['timestamp'])


def read_datasets(urls):
    dfs = []

    for url in urls:
        with suppress(Exception):
            dfs.append(read_dataset(url))

    df = pd.concat(dfs)

    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df['key'] = df['sensor'] + '.' + df['param']

    return df.pivot('timestamp', 'key', 'value')
