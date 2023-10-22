#!/usr/bin/env python3
from tabulate import tabulate
from pandas import DataFrame


def describe(df: DataFrame):
    #
    # Overview report

    min_bids, max_bids = [df.loc[df.bids.idxmin()], df.loc[df.bids.idxmax()]]

    overview = [
        ['observation', 'value'],
        ['min draw date', df.draw_date.min().strftime('%F')],
        ['max draw date', df.draw_date.max().strftime('%F')],
        ['count draw dates', df.draw_date.count()],
        ['missing values', int(sum(df.bids.isna()))],
        ['sum of all bids', int(df.bids.sum())],
        ['min bids in all draws', '{:.0f} ({:%F})'.format(min_bids.bids, min_bids.draw_date.to_pydatetime())],
        ['max bids in all draws', '{:.0f} ({:%F})'.format(max_bids.bids, max_bids.draw_date.to_pydatetime())],
    ]

    print(tabulate(overview, headers='firstrow', floatfmt='.1f', colalign=('left', 'right'), tablefmt='orgtbl'))

    #
    # Basic stats report

    stats = [['statistic', 'value']]

    t = set([i for i in df.groupby([df.draw_date.dt.year]).size()])
    stats.append(['count draws/year', '-'.join(sorted(map(str, t)))])
    stats.append(['average draws/week', int((sum(t) / len(t) / 54) * 10) / 10])
    stats.append(['median of all bids', df.bids.median()])

    t = df.bids.quantile([.25, .75])
    stats.append(['Q1', '{:.1f}'.format(t.iloc[0])])
    stats.append(['Q3', '{:.1f}'.format(t.iloc[1])])

    print('\n' + tabulate(stats, headers='firstrow', floatfmt='.1f', colalign=('left', 'right'), tablefmt='orgtbl'))

    # print(df.describe())
