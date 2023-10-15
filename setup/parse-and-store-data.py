#!/usr/bin/env python3
from datetime import datetime as _dt
from sys import version
from os import scandir
from re import sub

from bs4 import BeautifulSoup
from dateparser import parse

from extract_raw_data import source_url, oldest_draw, newest_draw

output_comments = [
    'Euromilhões data from each draw (top 3 prize count)',
    'Scraped from file {!r} (oldest, Oct/2004) to {!r} (Oct/2023)'.format(oldest_draw, newest_draw),
    'Between the first file, 373.0 (Oct/2004), and 12994.0 (Oct/2023), over 1600+ draws happened',
    'Attention to files as 4630.0 (draw 2004/34), added after draw 373.0 (2004/35) and 2391.0 (2006/50)',
    'Since 2011-05-06 (draw 6721.0) Euromilhões has draws every Friday and Tuesday (before the date, only Fridays)',
    'Run using Python v{} with libraries: requests, BeautifulSoup'.format('.'.join(version.split('.')[0:2])),
    'Created by Fernando Abreu, at {:%Y-%m-%d %H:%M:%S UTC}'.format(_dt.utcnow()),
    'Source of data: {}'.format(source_url),
]

raw_data_directory = 'data/raw'
target_filename_prefix = 'data/euromilhoes'
file_handler = None

print(f'Start data fetch, parse and store from {raw_data_directory}')
print(f'Data set will be stored in {target_filename_prefix}')


def parse_and_transform(buffer_reader: object) -> dict:
    """Parse and transform raw data and return dictionary with data points

    :param buffer_reader: (object), The return from open('sample-file.html', 'r')
    :return: dict having data points, as in: {
                 "draw_seq": "2004.034",
                 "draw_date": "2004-10-01",
                 "wins": None,  # Some draws do not report wins os bids
                 "bids": 1234567,
             }
    """
    draw_file = buffer_reader.name.split('/')[-1]

    res = dict(
        draw_seq=None,
        draw_date=None,
        wins=None,
        bids=None,
    )

    soup = BeautifulSoup(buffer_reader.read(), 'html.parser')
    draw_info = soup.find('span', attrs={'class': 'dataInfo'})
    if not soup.contents or not draw_info:
        print(f'Draw info not found in {draw_file}')
        return res

    # Find date of draw in page
    t = [s for s in draw_info.stripped_strings]
    res['draw_date'] = parse(t[1].split(' ')[-1], languages=['pt'])
    res['draw_seq'] = '{}.{:03d}'.format(res['draw_date'].year, int(t[0].replace('/', ' ').split(' ')[1]))

    # Find wins in page
    draw_top3_wins = soup.find_all('ul', attrs={'class': 'colums'})
    t = [sub(r'([\t \n])+', ' ', t.text).strip() for t in draw_top3_wins][1:4]
    if len(t) != 3:
        t = soup.find('div', attrs={'class': 'onecol'})
        msg = t.find('li').string if t else '(no reason found)'
        print(f'Draw win numbers could not be fetched for {draw_file}: "{msg}"')

    else:
        try:
            res['wins'] = sum([int(r.split(' ')[7]) for r in t])
        except IndexError as e:
            print(f'Draw win numbers could not be parsed for {draw_file}: {type(e)}({e})')

    # Find bids in page
    draw_bids_in_portugal = [
        sub(r'([\t \n])+', ' ', t.text).strip() for t in soup.find_all('ul', attrs={'class': 'noLine'})
        if 'Apostas registadas' in t.text
    ]
    if not draw_bids_in_portugal:
        print(f'Bids number could not be fetched for {draw_file}')

    else:
        try:
            res['bids'] = int(draw_bids_in_portugal[0].split(' ')[-1].replace('.', ''))
        except (IndexError, ValueError) as e:
            print(f'Bids number could not be parsed for {draw_file}: {type(e)}({e})')

    if res.get('bids'):
        print(f'All datapoints parsed for {draw_file}')

    return res


def get_csv_file_handler(area_code: str, csv_headers: iter) -> object:
    """Return a file handler for the CSV where to store data into

    :param area_code: (str), As in "eu" for "Europe" or "pt" for "Portugal
    :param csv_headers: (iter), As in ('draw', 'sequence', 'date', 'wins', 'bids')
    :return: BufferReader object
    """
    global file_handler
    if not file_handler:  # Create if not already set
        file_handler = open('{}.{}.csv'.format(target_filename_prefix, area_code.lower()), 'w')

        t = output_comments[:]
        t[0] += ' - Bids per draw in {}'.format(area_code.upper())
        t = [f'# {header}\n' for header in t]
        file_handler.writelines(t)

        print(','.join(csv_headers), file=file_handler, flush=True)

    return file_handler


def store_data_in_csv(data: dict, csv_file_handler: object):
    """Store draw data as CSV

    :param data: A dictionary having the country as key and the following data per country, as an inner dict:
                 draw_file: str, draw_seq: int, draw_date: str, wins: int, bids: int (bids are optional)
                 Sample: {
                    "draw_seq": "2004.034",
                    "draw_date": "2004-10-01",
                    "wins": None,  # Some draws do not report wins os bids
                    "bids": 1234567,
                 }
    :param csv_file_handler: TextIOWrapper object
    """

    print('{draw_seq},{draw_date:%Y-%m-%d},{wins},{bids}'.format(**data), file=csv_file_handler)


def run():
    fetch_count, parse_count, store_count = 0, 0, 0
    fh = None

    with scandir(raw_data_directory) as draw_files:
        for f in sorted(draw_files, key=lambda entry: entry.name):
            if all([f.is_file(), f.name.startswith('draw-'), f.name.endswith('.0.html')]):
                with open(f.path, 'rb') as g:
                    fetch_count += 1

                    parsed = parse_and_transform(g)
                    if not parsed.get('draw_date'):
                        continue
                    parse_count += 1

                    if not fh:
                        fh = get_csv_file_handler('pt', tuple(parsed.keys()))
                    store_data_in_csv(data=parsed, csv_file_handler=fh)
                    store_count += 1

    if fh:
        fh.close()

    print(f'Fetched raw files: {fetch_count}')
    print(f'Parsed raw data: {parse_count}')
    print(f'Draws stored in {target_filename_prefix}*.csv: {store_count}')


if __name__ == '__main__':
    run()
