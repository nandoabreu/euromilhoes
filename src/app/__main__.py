#!/usr/bin/env python3
from os.path import exists, getmtime
from sys import modules

import seaborn as sns

from app import config as cfg
from app.load_data import load_data
from app.analyse_data import describe
# noinspection PyUnresolvedReferences
from app.plots import (
    timeline,
    trimesters,
    monthly,
    draws,
    timeline_unusual,
    # timeline_acf,
)

if __name__ == '__main__':
    since_date: str = cfg.DATA_SINCE_ISO_DATE
    until_date = cfg.DATA_UNTIL_ISO_DATE
    df = load_data(area='pt', since_date=since_date, until_date=until_date)

    # Describe the data
    describe(df)

    # Trigger plots creation or recriation

    area_code = 'pt'
    area = {area_code: 'Portugal'}

    set2_palette = sns.color_palette('Set2', n_colors=15)
    year_colors = [set2_palette.as_hex()[i] for i in range(len(set2_palette))]

    data_modules = {m.__name__: m for m in modules.values() if m.__name__.startswith('app')}
    data_loader = data_modules.pop('app.load_data')

    for mname, module in [(n, m) for n, m in data_modules.items() if n.startswith('app.plots.')]:
        mname = mname.split('.')[-1]
        img_file = cfg.PLOT_DESTINATION_FILE.format(mname, area_code)
        csv_file = cfg.DATA_SOURCE_FILE.format(area_code)

        if (
            not exists(img_file)
            or getmtime(csv_file) > getmtime(img_file)
            or getmtime(module.__file__) > getmtime(img_file)
            or (getmtime(data_loader.__file__) > getmtime(img_file))
        ):
            kwargs = dict(df=df, area=area, save_to=img_file)
            if 'colors' in module.plot.__code__.co_varnames:
                kwargs['colors'] = year_colors

            module.plot(**kwargs)
            print(f'{mname} plot created')
