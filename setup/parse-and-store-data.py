#!/usr/bin/env python3
from datetime import datetime as _dt
from sys import version
from os import scandir

import numpy as np
from bs4 import BeautifulSoup
from dateparser import parse

from extract_raw_data import source_url, oldest_draw, newest_draw

raw_data_directory = 'data/raw'
target_filename_prefix = 'data/euromilhoes'

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

fh_pt, fh_eu = None, None
print(f'Start data fetch, parse and store from {raw_data_directory}')
print(f'Data set will be stored in {target_filename_prefix}')


def run(draw_ref: str, html_content: str) -> int:
    print(f'Parse and store draw of ref.: {draw_ref}')

    global fh_pt, fh_eu
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find date of draw in page
    t = [c.text for c in soup.find_all('span', attrs={'class': 'dataInfo'})]
    if not t:
        print("Draw date not found in response")
        return 0

    content_date = parse(t[0].split(' ')[-1], languages=['pt']).date()

    # Find wins in page
    t = [c.text for c in soup.find_all('ul', attrs={'class': 'colums'})]
    if len(t) < 4:
        print("Draw win numbers could not be fetched")
        return 0

    try:
        results = np.array([
            [int(n) for n in t[1].split('\n')[3:5]],
            [int(n) for n in t[2].split('\n')[3:5]],
            [int(n) for n in t[3].split('\n')[3:5]],
        ]).transpose()
    except IndexError:
        print("Draw win numbers could not be parsed")
        return 0

    pt_wins, eu_wins = results

    # Find PT bids in page
    t = [c.text for c in soup.find_all('ul', attrs={'class': 'noLine'})]
    if not t:
        print("Bids number could not be fetched")
        return 0

    bids = [item.replace('.', '') for item in t[-1].split('\n') if item and item.replace('.', '').isnumeric()]
    if not bids:
        print("Bids number could not be parsed")
        return 0

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

    print('Data parsed and stored')
    return 1


with scandir(raw_data_directory) as draw_files:
    fetched_files = 0
    stored_draws = 0
    for f in sorted(draw_files, key=lambda entry: entry.name):
        if all([f.is_file(), f.name.startswith('draw-'), f.name.endswith('.0.html')]):
            current_draw = '{:.1f}'.format(float(f.name.replace('draw-', '').replace('.html', '')))
            with open(f.path, 'rb') as g:
                fetched_files += 1
                stored_draws += run(current_draw, g.read())

    if fh_eu:
        fh_eu.close()

    if fh_pt:
        fh_pt.close()

    print(f'Fetched raw files: {fetched_files}')
    print(f'Draws stored in {target_filename_prefix}*.csv: {stored_draws}')
