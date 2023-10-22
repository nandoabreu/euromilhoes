#!/usr/bin/env python3
from datetime import datetime as _dt

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns


def plot(df: pd.DataFrame, area: dict, save_to: str = None) -> None:
    acf_values_to_display = int(len(df) * .05)
    area_code = list(area.keys())[0]
    area_name = area[area_code]

    acf_result = sm.tsa.acf(df.bids, nlags=acf_values_to_display)

    sns.set_theme()
    sns.axes_style('whitegrid')
    plt.subplots(figsize=(5, 3))  # 500x300 px

    plt.stem(list(range(len(acf_result))), acf_result, basefmt='k-')

    plt.title(f'Autocorrelation of the Euromilhões bids in {area_name}')
    plt.gcf().text(.855, .300, _dt.utcnow().strftime('FRA, %F %T UTC'), fontsize=5, color='gray', ha='right')
    plt.show() if not save_to else plt.savefig(save_to)
