import pandas as pd
import requests   
import sys
sys.path.append('..')   
import geopandas as gpd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
       


def clean_dataframe(station_dataframe: pd.DataFrame):
    station_dataframe.rename(columns={'YY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm': 'minute'}, inplace=True)
    station_dataframe['datetime'] = pd.to_datetime(station_dataframe[['year', 'month', 'day', 'hour', 'minute']])
    station_dataframe.set_index('datetime', inplace=True)
    station_dataframe.drop(columns=['year', 'month', 'day', 'hour', 'minute', 'TIDE', 'VIS', 'WVHT',   'DPD' ,  'APD' ,'MWD', 'WTMP'], inplace=True)

    unwanted_values = [99.0, 999.0, 9999.0]
    df_cleaned = station_dataframe[~station_dataframe.isin(unwanted_values).any(axis=1)]
    return df_cleaned

def create_historical_dataframe(station_number: str, year: int, year_dataframe: pd.DataFrame, geo_dataframe: gpd.GeoDataFrame):         
    df = pd.read_csv(f'../data/historical_data/downloaded_historical_file_{station_number.lower()}_{year}.txt', sep='\s+', skiprows=1)
    df.columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                  'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'TIDE']
    # Get the station's latitude and longitude from the geo_dataframe
    station_data = geo_dataframe[geo_dataframe['station'] == station_number]
    
    # Check if the station exists
    if not station_data.empty:
        latitude = station_data['latitude'].values[0]
        longitude = station_data['longitude'].values[0]
    else:
        print(f"Station {station_number} not found in geo_dataframe.")
        latitude = None
        longitude = None
    
    # Add new columns for station ID, longitude, and latitude
    df['station_id'] = station_number
    df['latitude'] = latitude
    df['longitude'] = longitude
    
    year_dataframe = pd.concat([year_dataframe, df])
    return year_dataframe

def create_continous_wind_dataframe(station_number: str, year: int, year_dataframe: pd.DataFrame, geo_dataframe: gpd.GeoDataFrame):         
    df = pd.read_csv(f'../data/continous_wind/downloaded_historical_file_{station_number.lower()}_{year}.txt', sep='\s+', skiprows=1)
    df.columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GDR', 'GST', 'GTIME']
    # Get the station's latitude and longitude from the geo_dataframe
    station_data = geo_dataframe[geo_dataframe['station'] == station_number]
    
    # Check if the station exists
    if not station_data.empty:
        latitude = station_data['latitude'].values[0]
        longitude = station_data['longitude'].values[0]
    else:
        print(f"Station {station_number} not found in geo_dataframe.")
        latitude = None
        longitude = None
    
    # Add new columns for station ID, longitude, and latitude
    df['station_id'] = station_number
    df['latitude'] = latitude
    df['longitude'] = longitude
    
    year_dataframe = pd.concat([year_dataframe, df])
    return year_dataframe


def create_dataframe(station_number: int, station_dataframe: pd.DataFrame):
    df = pd.read_csv(f'../data/downloaded_file_{station_number}.txt', sep='\s+', skiprows=1)
    df.columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                  'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']
    station_dataframe = pd.concat([station_dataframe, df])
    return station_dataframe


def load_data_real_time(station_name: str):
    url = f'https://www.ndbc.noaa.gov/data/realtime2/{station_name.lower()}.txt'
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'../data/downloaded_file_{station_name}.txt', 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully!")
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")


def load_history_data(station_name: str, year: int, failed_stations_per_year: dict):
    url = f'https://www.ndbc.noaa.gov/view_text_file.php?filename={station_name.lower()}h{year}.txt.gz&dir=data/historical/stdmet/'
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'../data/historical_data/downloaded_historical_file_{station_name}_{year}.txt', 'wb') as file:
            file.write(response.content)
        return 1, failed_stations_per_year
    else:
        print(f"Failed to download file. Status code: {response.status_code} for {station_name} and {year}") 
        failed_stations_per_year[str(year)].append(station_name) 
        return 0, failed_stations_per_year  
    

def load_continous_wind(station_name: str, year: int, failed_stations_per_year: dict):
    url = f'https://www.ndbc.noaa.gov/view_text_file.php?filename={station_name.lower()}c{year}.txt.gz&dir=data/historical/cwind/'
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'../data/continous_wind/downloaded_historical_file_{station_name}_{year}.txt', 'wb') as file:
            file.write(response.content)
        return 1, failed_stations_per_year
    else:
        print(f"Failed to download file. Status code: {response.status_code} for {station_name} and {year}") 
        failed_stations_per_year[str(year)].append(station_name) 
        return 0, failed_stations_per_year  

def clean_continous_wind_dataframe(station_dataframe: pd.DataFrame):
    station_dataframe.rename(columns={'YY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm': 'minute'}, inplace=True)
    station_dataframe['datetime'] = pd.to_datetime(station_dataframe[['year', 'month', 'day', 'hour', 'minute']])
    station_dataframe.set_index('datetime', inplace=True)
    station_dataframe.drop(columns=['year', 'month', 'day', 'hour', 'minute'], inplace=True)

    # unwanted_values = [99.0, 999.0, 9999.0]
    # df_cleaned = station_dataframe[~station_dataframe.isin(unwanted_values).any(axis=1)]
    return station_dataframe
    
def clean_dataframe(station_dataframe: pd.DataFrame):
    station_dataframe.rename(columns={'YY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm': 'minute'}, inplace=True)
    station_dataframe['datetime'] = pd.to_datetime(station_dataframe[['year', 'month', 'day', 'hour', 'minute']])
    station_dataframe.set_index('datetime', inplace=True)
    station_dataframe.drop(columns=['year', 'month', 'day', 'hour', 'minute', 'TIDE', 'VIS', 'WVHT', 'DPD' , 'APD' ,'MWD'], inplace=True)

    # unwanted_values = [99.0, 999.0, 9999.0]
    # df_cleaned = station_dataframe[~station_dataframe.isin(unwanted_values).any(axis=1)]
    return station_dataframe

def plot_time_series(station_dataframe: pd.DataFrame):
    station_dataframe[['WSPD', 'ATMP', 'PRES']].plot(figsize=(12, 6))
    plt.title('Wind Speed, Air Temperature, and Pressure Over Time')
    plt.ylabel('Value')
    plt.show()  

def plot_histograms(station_dataframe: pd.DataFrame):
    station_dataframe['WSPD'].hist(bins=20, figsize=(8, 6))
    plt.title('Distribution of Wind Speed')
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Frequency')
    plt.show()
    
def plot_windrose(station_dataframe: pd.DataFrame):
    ax = WindroseAxes.from_ax()
    ax.bar(station_dataframe['WDIR'], station_dataframe['WSPD'], normed=True, opening=0.8, edgecolor='white')
    ax.set_title('Wind Rose Plot')
    plt.show()
            

