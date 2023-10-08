#!/usr/bin/env python3
from dateparser import parse

import seaborn as sns

from app import config as cfg
from app.load_data import load_data
from app.plots.timeline import plot as plot_line
from app.plots.trimesters import plot as plot_trimesters
from app.plots.monthly import plot as plot_months
from app.plots.draws import plot as plot_draws


if __name__ == '__main__':
    since_date = parse(cfg.DATA_SINCE_ISO_DATE)
    until_date = parse(cfg.DATA_UNTIL_ISO_DATE)
    df = load_data(area='pt', since_date=since_date, until_date=until_date)

    area_code = 'pt'
    area = {area_code: 'Portugal'}

    set2_palette = sns.color_palette('Set2', n_colors=15)
    year_colors = [set2_palette.as_hex()[i] for i in range(len(set2_palette))]

    from os.path import exists, getmtime  # todo: remove
    t = 'data/euromilhoes-line.pt.png'
    if not exists(t) or getmtime('src/app/plots/timeline.py') > getmtime(t):
        plot_line(df=df, area=area, save_to=cfg.PLOT_DESTINATION_FILE.format('line', area_code))
    t = 'data/euromilhoes-months.pt.png'
    if not exists(t) or getmtime('src/app/plots/monthly.py') > getmtime(t):
        plot_months(df=df, area=area, save_to=cfg.PLOT_DESTINATION_FILE.format('months', area_code), colors=year_colors)
    t = 'data/euromilhoes-trimesters.pt.png'
    # if not exists(t) or getmtime('src/app/plots/trimesters.py') > getmtime(t):
    #     plot_trimesters(
    #         df=df, area=area, save_to=cfg.PLOT_DESTINATION_FILE.format('months', area_code),
    #         colors=year_colors
    #     )
    t = 'data/euromilhoes-draws.pt.png'
    if not exists(t) or getmtime('src/app/plots/draws.py') > getmtime(t):
        plot_draws(df=df, area=area, save_to=cfg.PLOT_DESTINATION_FILE.format('draws', area_code))
