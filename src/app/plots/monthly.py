#!/usr/bin/env python3
from datetime import datetime as _dt

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter


def plot(df: pd.DataFrame, area: dict, colors: iter = None, save_to: str = None) -> None:
    area_code = list(area.keys())[0]
    area_name = area[area_code]

    years = list(range(df.date.min().year, df.date.max().year + 1))
    month_by_number = dict((i, _dt(1, i, 1).strftime('%b')) for i in range(1, 12+1))

    fig = plt.figure(figsize=(11, 11))
    gs = GridSpec(nrows=len(years), ncols=2, width_ratios=[2, 1])

    for i, year in enumerate(sorted(years, reverse=True)):
        data = pd.DataFrame(df[df.date.dt.year == year].groupby(df.date.dt.month).bids.agg('sum'))
        data.rename(index=month_by_number, inplace=True)

        #
        # Set the bar plot on the left

        ax = plt.subplot(gs[i, 0])
        p = sns.barplot(data=data, x='date', y='bids', ax=ax, legend=False, palette='pastel', hue='date')

        p.set_ylim(5_000_000, 40_000_000)
        p.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x/1e6:.0f}M'))
        p.axhline(data.bids.mean(), color='red', linestyle='--')

        p.text(0.015, 0.879, '{}: {} bids in {} draws'.format(
            year,
            '{:.1f}M'.format(df[df.date.dt.year == year].bids.sum() / 1e6),
            df[df.date.dt.year == year].count().iloc[0],
        ), fontsize=11, transform=p.transAxes, horizontalalignment='left')

        p.set(xlabel=None, ylabel=None)

        #
        # Set the box plot on the right

        ax = plt.subplot(gs[i, 1])
        p = sns.boxplot(data=data, x='bids', ax=ax, legend=False, color=colors[i % len(colors) if i > 0 else 0])

        p.set_xlabel('')
        p.set_xlim(12.5 * 1e6, 37.5 * 1e6)
        p.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x/1e6:.0f}M'))

        p.text(0.985, 0.879, str(year), fontsize=11, transform=p.transAxes, ha='right')

    fig.suptitle(f'Bids in {area_name} (months per year, {years[0]}-{years[-1]})')
    plt.gcf().text(.985, .005, _dt.utcnow().strftime('FRA, %F %T UTC'), fontsize=7, color='gray', ha='right')

    plt.tight_layout()

    if save_to:
        plt.savefig(save_to)

    else:
        plt.show()
