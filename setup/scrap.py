#!/usr/bin/env python3
from datetime import datetime as _dt
from sys import version
from os import makedirs

import requests
import ssl
import urllib3
import numpy as np
from bs4 import BeautifulSoup
from dateparser import parse

oldest_draw, newest_draw = 373.0, 12994.0  # 373.0 is the first registered draw number; there are 1600 draws by Oct/2023
source_url = 'https://www.jogossantacasa.pt/web/SCCartazResult/euroMilhoes'
target_filename_prefix = 'data/euromilhoes'
target_raw_directory = 'data/raw'

output_comments = [
    'Euromilhões data from each draw (top 3 prize count)',
    'Scraped from draw {!r} (oldest, Oct/2004) to {!r} (Oct/2023)'.format(oldest_draw, newest_draw),
    'Between the first draw, 373.0 (Oct/2004), and the draw ID 12994.0 (Oct/2023), over 1600 draws happened',
    'Since 2011-05-06 (draw 6721.0) Euromilhões has draws every Friday and Tuesday (before the date, only Fridays)',
    'Run using Python v{} with libraries: requests, BeautifulSoup'.format('.'.join(version.split('.')[0:2])),
    'Created by Fernando Abreu, at {:%Y-%m-%d %H:%M:%S UTC}'.format(_dt.utcnow()),
    'Source of data: {}'.format(source_url),
]
output_headers = ['draw', 'date', 'wins']

makedirs(target_raw_directory, exist_ok=True)


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        urllib3.disable_warnings()
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_OPTIONAL
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


responses_size = 0
fh_pt, fh_eu = None, None
print(f'Start scrapping {source_url}')

for current_draw in range(int(oldest_draw), int(newest_draw) + 1):
    current_draw = f'{current_draw:.1f}'
    print(f'Scrap draw of ref.: {current_draw}')

    raw_storage_file = f'{target_raw_directory}/draw-{current_draw}.html'

    data = dict(selectContest=current_draw, Consultar='Consultar')
    session = requests.session()
    session.mount('https://', TLSAdapter())
    response = session.post(source_url, verify=False, data=data)

    responses_size += len(response.content)

    if response.status_code != 200:
        print(f'Scrap request responded HTTP status {response.status_code}')
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    if "Últimos Resultados" not in str(soup.title):
        print("Expected title not found in response")
        continue

    # Find date of draw in page
    t = [c.text for c in soup.find_all('span', attrs={'class': 'dataInfo'})]
    if not t:
        print("Draw date not found in response")
        continue

    content_date = parse(t[0].split(' ')[-1], languages=['pt']).date()

    # Find wins in page
    t = [c.text for c in soup.find_all('ul', attrs={'class': 'colums'})]
    if len(t) < 4:
        print("Draw win numbers could not be fetched")
        continue

    try:
        results = np.array([
            [int(n) for n in t[1].split('\n')[3:5]],
            [int(n) for n in t[2].split('\n')[3:5]],
            [int(n) for n in t[3].split('\n')[3:5]],
        ]).transpose()
    except IndexError:
        print("Draw win numbers could not be parsed")
        continue

    pt_wins, eu_wins = results

    # Find PT bids in page
    t = [c.text for c in soup.find_all('ul', attrs={'class': 'noLine'})]
    if not t:
        print("Bids number could not be fetched")
        continue

    bids = [item.replace('.', '') for item in t[-1].split('\n') if item and item.replace('.', '').isnumeric()]
    if not bids:
        print("Bids number could not be parsed")
        continue

    bids = bids[0]

    # Open CSV file for EU data
    if not fh_eu:
        fh_eu = open('{}.eu.csv'.format(target_filename_prefix), 'w')
        t = output_comments[:]
        t[0] += ' - All participating countries'
        t = [f'# {header}\n' for header in t]
        fh_eu.writelines(t)
        print(','.join(output_headers), file=fh_eu, flush=True)

    # Open CSV file for PT data
    if not fh_pt:
        fh_pt = open('{}.pt.csv'.format(target_filename_prefix), 'w')
        t = output_comments[:]
        t[0] += " - Portugal's bids"
        t = [f'# {header}\n' for header in t]
        fh_pt.writelines(t)
        output_headers.insert(2, 'bids')
        print(','.join(output_headers), file=fh_pt, flush=True)

    print(f'{current_draw},{content_date:%Y-%m-%d},{sum(eu_wins)}', file=fh_eu, flush=True)
    print(f'{current_draw},{content_date:%Y-%m-%d},{bids},{sum(pt_wins)}', file=fh_pt, flush=True)

    with open(raw_storage_file, 'wb') as f:
        f.write(response.content)

    print('Data scraped and stored')

if fh_eu:
    fh_eu.close()

if fh_pt:
    fh_pt.close()

print(f'{responses_size} bytes of data fetched')
