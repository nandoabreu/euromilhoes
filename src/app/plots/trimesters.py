#!/usr/bin/env python3
from datetime import datetime as _dt

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def plot(df: pd.DataFrame, area: dict, colors: iter = None, save_to: str = None) -> None:
    months_in_period = 3  # trimesters
    area_code = list(area.keys())[0]
    area_name = area[area_code]

    df['period'] = (df.date.dt.strftime('%m').astype(int) + 2) / months_in_period
    df['period'] = df['period'].astype(int)

    years = sorted(list(range(df.date.max().year, df.date.min().year - 1, -1)), reverse=True)
    periods = sorted(df.period.unique().tolist(), reverse=False)
    fig, axs = plt.subplots(figsize=(9, 13), nrows=len(years), ncols=int(12 / months_in_period))  # 900x1300 px

    for i, year in enumerate(years):
        color = colors[i % len(colors) if i > 0 else 0]
        sns.set_palette(sns.color_palette([color]))
        # For another color reference, see:
        # https://stackoverflow.com/questions/46173419/change-bar-color-according-to-hue-name/46174007#46174007

        for j, period in enumerate(periods):
            data = df[(df.date.dt.year == year) & (df.period == period)]
            p = sns.boxplot(
                data=data, x='bids', hue='period', vert=False, ax=axs[i, j],
                legend=False, palette=['C0'],
            )

            p.set_xlim(1_000_000, 7_000_000)
            p.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x/1e6:.0f}M'))
            p.set(xlabel=None, ylabel=None if j > 0 else year)

            # if year != years[-1]:
            #     axs[i, j].set_xticklabels([])

    fig.suptitle(f"Bids in {area_name} (per draw in years' trimesters, {years[0]}-{years[-1]})")
    plt.gcf().text(.985, .003, _dt.utcnow().strftime('FRA, %F %T UTC'), fontsize=7, color='gray', ha='right')

    plt.tight_layout()

    if save_to:
        plt.savefig(save_to)

    else:
        plt.show()
