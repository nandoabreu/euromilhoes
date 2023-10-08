#!/usr/bin/env python3
from datetime import datetime as _dt, timedelta

import pandas as pd

from app import config as cfg


def load_data(
    area: str = 'pt',
    since_date: _dt.date = _dt.today() - timedelta(days=30),
    until_date: _dt.date = _dt.today(),
) -> pd.DataFrame:
    df = pd.read_csv(cfg.DATA_SOURCE_FILE.format(area), comment='#')

    df.date = pd.to_datetime(df.date)
    df.sort_values(['draw', 'date'], ascending=True, inplace=True)

    if since_date:
        df = df[df.date >= since_date]
    if until_date:
        df = df[df.date <= until_date]

    if len(df.draw.unique()) != df.shape[0]:
        df.drop_duplicates(keep='last', inplace=True)

    # df.set_index('draw', drop=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # print(df.head(3))
    # print(df.dtypes)
    # print('\ndescribe:\n', df.wins.describe())

    return df