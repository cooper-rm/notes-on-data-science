import io
import zipfile

import pandas as pd
import requests

from src import config


def _get(url, params=None):
    response = requests.get(url, params=params, headers=config.HEADERS, timeout=180)
    response.raise_for_status()
    return response


def _write(frame, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return path


def download_french(path=config.FRENCH_FILE):
    archive = zipfile.ZipFile(io.BytesIO(_get(config.FRENCH_URL).content))
    lines = archive.read(archive.namelist()[0]).decode('utf-8').splitlines()

    start = next(i for i, line in enumerate(lines) if line.startswith(','))
    end = next(i for i, line in enumerate(lines[start + 1:], start + 1) if not line.strip())

    frame = pd.read_csv(io.StringIO('\n'.join(lines[start:end])))
    frame.columns = ['date'] + [c.strip().lower().replace('-', '_') for c in frame.columns[1:]]
    frame['date'] = pd.to_datetime(frame['date'], format='%Y%m%d')
    return _write(frame, path)


def download_crypto(path=config.CRYPTO_FILE, symbols=config.CRYPTO_SYMBOLS):
    columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume']
    frames = []
    for symbol in symbols:
        url = config.BITFINEX_URL.format(symbol=symbol)
        candles = _get(url, params={'limit': config.CRYPTO_LIMIT, 'sort': 1}).json()
        frame = pd.DataFrame(candles, columns=columns)
        frame['date'] = pd.to_datetime(frame['timestamp'], unit='ms')
        frame['symbol'] = symbol
        frames.append(frame.drop(columns='timestamp'))

    frame = pd.concat(frames, ignore_index=True)
    return _write(frame[['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']], path)


def download_hmda(path=config.HMDA_FILE, params=config.HMDA_PARAMS):
    response = _get(config.HMDA_URL, params=params)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.content)
    return path


def load_french(path=config.FRENCH_FILE):
    return pd.read_csv(path, parse_dates=['date'])


def load_crypto(path=config.CRYPTO_FILE):
    return pd.read_csv(path, parse_dates=['date'])


def load_hmda(path=config.HMDA_FILE, usecols=None):
    return pd.read_csv(path, usecols=usecols, low_memory=False)
