#!/usr/bin/env python3
from pandas import DataFrame
from scipy.stats import ttest_ind
from statsmodels.tsa.stattools import adfuller
from tabulate import tabulate


def is_stationary(df: DataFrame, column: str) -> bool:
    """Discover if data is stationary or has a trend"""
    alpha = .05
    result = adfuller(df[column])

    p_value = result[1]
    return p_value < alpha


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

    stats.append(['bids are stationary', is_stationary(df, 'bids')])

    print('\n' + tabulate(stats, headers='firstrow', floatfmt='.1f', colalign=('left', 'right'), tablefmt='orgtbl'))


def normalize_data(df: DataFrame, column: str) -> DataFrame:
    """Apply z-score normalization to bids and return the data frame with an additional "normal" column

    This process will parse the data to have a mean of 0 and a standard deviation of 1.
    """
    df['normal'] = (df.bids - df.bids.mean()) / df.bids.std()

    return df


def set_moving_avg(df: DataFrame, column: str, window_size: int) -> df:
    df['moving_avg'] = df[column].rolling(window=window_size, min_periods=1).mean()
    return df


# def find_change_points(df: DataFrame) -> list:
#     window_size = int(len(df) * .05)
#     alpha = 0.05  # Significance level
#
#     segments = [df.iloc[i:i + window_size] for i in range(0, len(df), window_size)]
#     print(f'{len(segments)=}')
#
#     change_points = []
#     for i in range(1, len(segments)):
#         segment1 = segments[i - 1]['normal']
#         segment2 = segments[i]['normal']
#         t_stat, p_value = ttest_ind(segment1, segment2)
#
#         if p_value < alpha:
#             change_points.append(i)
#
#     return change_points
