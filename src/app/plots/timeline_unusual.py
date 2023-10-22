#!/usr/bin/env python3
from datetime import datetime as _dt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


def plot(df: pd.DataFrame, area: dict, save_to: str = None) -> None:
    area_code = list(area.keys())[0]
    area_name = area[area_code]

    sns.set_theme()
    sns.axes_style('whitegrid')
    plt.subplots(figsize=(15, 5))  # 1500x500 px

    peaks_threashold = .0075
    quantiles = df.bids.quantile([0 + peaks_threashold, .25, .5, .75, 1 - peaks_threashold]).to_list()

    p = sns.scatterplot(data=df, x=df.draw_date, y=df.bids, color='blue')
    p.axhline(quantiles[3], color='gray', linestyle='dashed', label='Q3')
    p.axhline(quantiles[2], color='red', linestyle='dashed', label='Median')
    p.axhline(quantiles[1], color='gray', linestyle='dashed', label='Q1')

    p.xaxis.set_major_locator(mdates.YearLocator())
    p.xaxis.set_major_formatter(mdates.DateFormatter('%b, %Y'))

    higher_peaks = sorted([
        (xi, df.loc[xi, 'draw_date'], y)
        for xi, y in enumerate(df.bids)
        if quantiles[-1] < y
    ])

    lower_peaks = sorted([
        (xi, df.loc[xi, 'draw_date'], y)
        for xi, y in enumerate(df.bids)
        if y < quantiles[0]
    ], key=lambda v: v[-1], reverse=True)

    peaks = higher_peaks + lower_peaks

    for i in range(len(peaks)):
        cmp = min if peaks[i] in lower_peaks else max
        xi, x, y = peaks[i]

        if i < len(peaks) - 1:
            next_xi, next_x, next_y = peaks[i+1]
            x_lag = abs(xi - next_xi)

            if x_lag < 9:
                if y != cmp(y, next_y):
                    continue

        plt.annotate(
            '{s}{x:%d/%b}, {y:.0f} bids{s}'.format(x=x, y=y, s=' '*2),
            xy=(x, y), xytext=(x, y), textcoords='data', fontsize=11, color='brown', va='top', ha='left',
            arrowprops=dict(arrowstyle='->'),
        )

    years = list(range(df.draw_date.min().year, df.draw_date.max().year + 1))
    p.set(title=f'Euromilhões bids in {area_name} (bids by day, {years[0]}-{years[-1]})', xlabel=None, ylabel='Bids')
    plt.gcf().text(.945, .285, _dt.utcnow().strftime('FRA, %F %T UTC'), fontsize=7, color='gray', ha='right')

    plt.tight_layout()
    plt.legend()

    if save_to:
        plt.savefig(save_to)

    else:
        plt.show()
