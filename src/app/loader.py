#!/usr/bin/env python3
import datetime

import pandas as pd


class MainDataFrame:
    """Instanciate a pandas DataFrame"""
    def __init__(self):
        self.df = pd.DataFrame()

    def load_df(
        self,
        data_source_file: str,
        date_column_in_source: str = None,
        since_date: datetime.date = None,
        until_date: datetime.date = None,
    ) -> bool:
        """
        Load data into the frame

        Args:
            data_source_file (str): path and file name of the data source (aka: the CSV file)
            date_column_in_source (str, optional): name of column having dates in the data source
            since_date (date, optional): use to limit the data to be loaded (if date_column_in_source is set)
            until_date (date, optional): use to limit the data to be loaded (if date_column_in_source is set)

        Returns:
            bool: True, if data was loaded

        Example:
            >>> m = MainDataFrame()
            >>> m.load_df('my-data.csv')
            >>> df = m.get_df()
        """
        df = pd.read_csv(
            data_source_file,
            parse_dates=[date_column_in_source],
            index_col=date_column_in_source,
            comment='#',
        )

        if since_date or until_date:
            df = df[since_date:until_date]

        df.draw_seq = df.draw_seq.astype('category')
        df.sort_values(['draw_date'], ascending=True, inplace=True)

        if len(df.draw_seq.unique()) != df.shape[0]:
            df.drop_duplicates(keep='last', inplace=True)

        self.df = df
        # df.reset_index(drop=True, inplace=True)

        return True

    def get_df(self):
        return self.df
