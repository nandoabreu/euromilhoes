#!/usr/bin/env python3
from os.path import exists, getmtime
from sys import modules

import seaborn as sns
from dateparser import parse

from app import config as cfg
from app.load_data import load_data
# noinspection PyUnresolvedReferences
from app.plots import (
    timeline,
    trimesters,
    monthly,
    draws,
)

if __name__ == '__main__':
    since_date = parse(cfg.DATA_SINCE_ISO_DATE)
    until_date = parse(cfg.DATA_UNTIL_ISO_DATE)
    df = load_data(area='pt', since_date=since_date, until_date=until_date)

    area_code = 'pt'
    area = {area_code: 'Portugal'}

    set2_palette = sns.color_palette('Set2', n_colors=15)
    year_colors = [set2_palette.as_hex()[i] for i in range(len(set2_palette))]

    for module in [m for m in modules.values() if m and m]:
        if not module.__name__.startswith('app.plots.'):
            continue

        mname = module.__name__.split('.')[-1]
        img_file = cfg.PLOT_DESTINATION_FILE.format(mname, area_code)
        csv_file= cfg.DATA_SOURCE_FILE.format(area_code)

        if any([
            not exists(img_file),
            getmtime(csv_file) > getmtime(img_file),
            getmtime(module.__file__) > getmtime(img_file),
        ]):
            kwargs = dict(df=df, area=area, save_to=img_file)
            if 'colors' in module.plot.__code__.co_varnames:
                kwargs['colors'] = year_colors

            module.plot(**kwargs)
            print(f'{mname} plot created')
