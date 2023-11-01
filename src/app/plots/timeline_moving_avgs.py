#!/usr/bin/env python3
from datetime import datetime as _dt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


def plot(df: pd.DataFrame, window_size: int, area: dict, save_to: str = None) -> None:
    area_code = list(area.keys())[0]
    area_name = area[area_code]

    plt.figure(figsize=(17, 3))

    plt.plot(df.draw_date, df.bids, label='Bids')
    plt.plot(df.draw_date, df.moving_avg, label=f'Moving Average ({window_size}-day)')
    plt.xlabel('Date')
    plt.ylabel('Bids')
    plt.title('Time Series with Moving Average')

    # plt.set(title=f'Variance change points from {area_name}\'s Euromilhões bids', xlabel=None, ylabel='Bids')
    plt.title(f"Variance change points from {area_name}\'s Euromilhões bids")
    plt.gcf().text(.950, .295, _dt.utcnow().strftime('FRA, %F %T UTC'), fontsize=7, color='gray', ha='right')

    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show() if not save_to else plt.savefig(save_to)
