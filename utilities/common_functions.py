import pandas as pd


def clean_dataframe(station_dataframe: pd.DataFrame):
    station_dataframe.rename(columns={'YY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm': 'minute'}, inplace=True)
    station_dataframe['datetime'] = pd.to_datetime(station_dataframe[['year', 'month', 'day', 'hour', 'minute']])
    station_dataframe.set_index('datetime', inplace=True)
    station_dataframe.drop(columns=['year', 'month', 'day', 'hour', 'minute', 'TIDE', 'VIS', 'WVHT',   'DPD' ,  'APD' ,'MWD', 'WTMP'], inplace=True)

    unwanted_values = [99.0, 999.0, 9999.0]
    df_cleaned = station_dataframe[~station_dataframe.isin(unwanted_values).any(axis=1)]
    return df_cleaned


def create_historical_dataframe(station_number: int, year: int, station_dataframe: pd.DataFrame):
    df = pd.read_csv(f'data/downloaded_historical_file_{station_number}_{year}.txt', delim_whitespace=True, skiprows=1)
    df.columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                  'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'TIDE']
    station_dataframe = pd.concat([station_dataframe, df])
    return station_dataframe
            

