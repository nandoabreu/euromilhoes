#!/usr/bin/env python3
from datetime import datetime as _dt

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot(df: pd.DataFrame, area: dict, save_to: str = None) -> None:
    area_code = list(area.keys())[0]
    area_name = area[area_code]

    sns.set_theme()
    sns.axes_style('whitegrid')
    plt.subplots(figsize=(17, 3))  # 1700x300 px

    p = sns.lineplot(x='date', y='bids', data=df)

    p.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    p.xaxis.set_major_formatter(mdates.DateFormatter('%b, %Y'))
    plt.gcf().autofmt_xdate(rotation=60)

    xticks = plt.gca().get_xticklabels()
    # noinspection PyProtectedMember
    covid_emergency = [i for i, t in enumerate(xticks) if t._text in ('Mar, 2020', 'Apr, 2021')]
    [xticks[i].set_color('red') for i in range(covid_emergency[0], covid_emergency[-1] + 1)]

    # plt.annotate(
    #     'Covid Emergency state',
    #     xycoords='axes pixels', xy=(1295, 125), color='red',
    #     # bbox=dict(boxstyle='round,pad=0.', fc='black'),
    # )
    leg = plt.legend(
        loc='upper right', frameon=False, labels=['Covid Emergency state'], labelcolor='red',
    )
    leg.legendHandles[0].set_visible(False)  # Remove line from legend's first item

    years = list(range(df.date.min().year, df.date.max().year + 1))
    p.set(title=f'Euromilhões bids in {area_name} (bids by day, {years[0]}-{years[-1]})', xlabel=None, ylabel='Bids')
    plt.gcf().text(.995, .015, _dt.utcnow().strftime('FRA, %F %T UTC'), fontsize=7, color='gray', ha='right')

    plt.tight_layout()

    if save_to:
        plt.savefig(save_to)

    else:
        plt.show()
