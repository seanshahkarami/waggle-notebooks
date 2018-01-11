import pandas as pd


def load_dataset(url):
    column_names = ['node_id', 'timestamp', 'plugin', 'topic', 'sensor', 'param', 'value']
    df = pd.read_csv(url, sep=';', names=column_names, parse_dates=['timestamp'])

    series = []

    for (sensor, param), rows in df.groupby(('sensor', 'param')):
        name = '.'.join([sensor, param])

        try:
            s = pd.Series(rows['value'].astype(float).values, index=rows['timestamp'].values, name=name)
        except ValueError:
            continue

        series.append(s)

    return pd.concat(series, axis=1)


def load_datasets(urls):
    dfs = []
    
    for url in urls:
        try:
            dfs.append(load_dataset(url))
        except:
            continue
    
    return pd.concat(dfs)
