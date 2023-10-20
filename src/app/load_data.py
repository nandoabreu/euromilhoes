#!/usr/bin/env python3
from datetime import datetime as _dt, timedelta

import pandas as pd

from app import config as cfg


def load_data(
    area: str = 'pt',
    since_date: str = '{:%F}'.format(_dt.today() - timedelta(days=30)),
    until_date: str = '{:%F}'.format(_dt.today() + timedelta(days=30)),
) -> pd.DataFrame:
    since_date = _dt.strptime(since_date, '%Y-%m-%d')
    until_date = _dt.strptime(until_date, '%Y-%m-%d')

    df = pd.read_csv(cfg.DATA_SOURCE_FILE.format(area), comment='#')
    df.draw_date = pd.to_datetime(df.draw_date, format='%Y-%m-%d')
    df = df[df['draw_date'].between(since_date, until_date)]
    df.draw_seq = df.draw_seq.astype('category')
    df.sort_values(['draw_seq', 'draw_date'], ascending=True, inplace=True)

    if len(df.draw_seq.unique()) != df.shape[0]:
        df.drop_duplicates(keep='last', inplace=True)

    # df.set_index('draw', drop=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df
