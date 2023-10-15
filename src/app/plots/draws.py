#!/usr/bin/env python3
from datetime import datetime as _dt

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot(df: pd.DataFrame, area: dict, save_to: str = None) -> None:
    area_code = list(area.keys())[0]
    area_name = area[area_code]

    df['day_of_week'] = df.draw_date.dt.day_name()

    ranges = ['< 2M', '2-3M', '3-4M', '4-5M', '>=5M']
    df['bids_ranges'] = np.where(df.bids.lt(2_000_000), ranges[0], '')
    df.bids_ranges = np.where(df.bids.ge(2_000_000) & df.bids.lt(3_000_000), ranges[1], df.bids_ranges)
    df.bids_ranges = np.where(df.bids.ge(3_000_000) & df.bids.lt(4_000_000), ranges[2], df.bids_ranges)
    df.bids_ranges = np.where(df.bids.ge(4_000_000) & df.bids.lt(5_000_000), ranges[3], df.bids_ranges)
    df.bids_ranges = np.where(df.bids.ge(5_000_000), ranges[4], df.bids_ranges)
    df.bids_ranges = pd.Categorical(df.bids_ranges, ranges)

    # ranges_per_day = pd.DataFrame(df.groupby('day_of_week').bids.agg('sum'))
    # ranges_per_day.reset_index(inplace=True)
    # print(ranges_per_day)

    fig, axs = plt.subplots(figsize=(7, 7), nrows=2)  # 700x700 px
    sns.set_theme()
    sns.axes_style('whitegrid')

    p0 = sns.barplot(data=df, x='day_of_week', y='bids', estimator=sum, ax=axs[0], color='skyblue')
    p1 = sns.histplot(data=df, x='day_of_week', hue='bids_ranges', ax=axs[1], color='skyblue', multiple='dodge')

    years = list(range(df.draw_date.min().year, df.draw_date.max().year + 1))
    p0.set(
        title=f'Total number of bids in {area_name}, (by draw day, {years[0]}-{years[-1]})',
        xlabel=None, ylabel='Bids counts'
    )
    p1.set(
        title=f'Distribution of bids in {area_name}, (by draw day, {years[0]}-{years[-1]})',
        xlabel=None, ylabel='Distribution'
    )
    plt.gcf().text(.985, .015, _dt.utcnow().strftime('FRA, %F %T UTC'), fontsize=7, color='gray', ha='right')

    plt.tight_layout()

    if save_to:
        plt.savefig(save_to)

    else:
        plt.show()
