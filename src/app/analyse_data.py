#!/usr/bin/env python3
from tabulate import tabulate
from pandas import DataFrame


def describe(df: DataFrame):
    overview = [
        ['observation', 'value'],
        ['min draw date', df.draw_date.min().strftime('%F')],
        ['max draw date', df.draw_date.max().strftime('%F')],
        ['count draw dates', df.draw_date.count()],
        ['sum of all bids', int(df.bids.sum())],
    ]
    print(tabulate(overview, headers='firstrow', floatfmt='.1f', colalign=('left', 'right'), tablefmt='orgtbl'))

    stats = [['statistic', 'value']]

    t = set([i for i in df.groupby([df.draw_date.dt.year]).size()])
    stats.append(['count draws/year', '-'.join(sorted(map(str, t)))])
    stats.append(['average draws/week', int((sum(t) / len(t) / 54) * 10) / 10])

    t = df.bids.quantile([.25, .75])
    stats.append(['Q1', '{:.1f}'.format(t.iloc[0])])
    stats.append(['Q3', '{:.1f}'.format(t.iloc[1])])

    print('\n' + tabulate(stats, headers='firstrow', floatfmt='.1f', colalign=('left', 'right'), tablefmt='orgtbl'))

    # print(df.describe())
