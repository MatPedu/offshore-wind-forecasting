

import requests
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes


def load_data_real_time(station_number: int):
    """
    Load the data from the NOAA website and save it to a local file.
    
    Args:
        station_number (int): The station number of the buoy.
    """
    url = f'https://www.ndbc.noaa.gov/data/realtime2/{station_number}.txt'

    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
    # Save the content to a local file
        with open(f'data/downloaded_file_{station_number}.txt', 'wb') as file:
            file.write(response.content)

        print("File downloaded successfully!")

    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")

def load_history_data(station_number: int, year: int):
    
    url = f'https://www.ndbc.noaa.gov/view_text_file.php?filename={station_number}h{year}.txt.gz&dir=data/historical/stdmet/'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(f'data/downloaded_historical_file_{station_number}_{year}.txt', 'wb') as file:
            file.write(response.content)
            
        print("File downloaded successfully!")
        
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")
    
    
        
def create_dataframe(station_number: int, station_dataframe: pd.DataFrame):
    """
    Create a DataFrame from the downloaded file.
    
    Args:
        station_number (int): The station number of the buoy.
        station_dataframe (pd.DataFrame): The DataFrame containing the data from all stations.
        
    Returns:
        pd.DataFrame: The DataFrame containing the data from all stations.
    """
    
    # Now load the downloaded file into a DataFrame
    df = pd.read_csv(f'data/downloaded_file_{station_number}.txt', delim_whitespace=True, skiprows=2)

    # Rename the columns
    df.columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']

    # Display the first few rows of the dataframe
    print(df.head())
    
    # Complete the main dataframe because the columns are the same
    station_dataframe = pd.concat([station_dataframe, df])
    
    return station_dataframe

# def clean_dataframe(station_dataframe: pd.DataFrame):


def create_historical_dataframe(station_number: int, year: int, station_dataframe: pd.DataFrame):
    
    df = pd.read_csv(f'data/downloaded_historical_file_{station_number}_{year}.txt', delim_whitespace=True, skiprows=2)
    #YY  MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS  TIDE
    df.columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'TIDE']
    
    print(df.head())
    
    
    station_dataframe = pd.concat([station_dataframe, df])
    
    return station_dataframe
    
    
def main():
    # URL of the .txt file
    station_numbers = [44013]
    year = 2015
    
    
    station_dataframe = pd.DataFrame()
    
    for station_number in station_numbers:
        load_history_data(station_number, year)
        station_dataframe = create_historical_dataframe(station_number, year, station_dataframe)
    
    
    # Create a 'datetime' column
    station_dataframe.rename(columns={'YY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm': 'minute'}, inplace=True)

    station_dataframe['datetime'] = pd.to_datetime(station_dataframe[['year', 'month', 'day', 'hour', 'minute']])
    station_dataframe.set_index('datetime', inplace=True)
    station_dataframe.drop(columns=['year', 'month', 'day', 'hour', 'minute', 'TIDE', 'DEWP',  'VIS'], inplace=True)
    
    # Define the list of unwanted values
    unwanted_values = [99.0, 999.0, 9999.0]

    # Filter out rows where any column contains these unwanted values
    df_cleaned = station_dataframe[~station_dataframe.isin(unwanted_values).any(axis=1)]

    # Verify the result
    print(f"Original DataFrame shape: {station_dataframe.shape}")
    print(f"Cleaned DataFrame shape: {df_cleaned.shape}")
    
    df_cleaned[['WSPD', 'ATMP', 'PRES']].plot(figsize=(12, 6))
    plt.title('Wind Speed, Air Temperature, and Pressure Over Time')
    plt.ylabel('Value')
    plt.show()
    # Summary statistics for numerical columns
    summary_stats = df_cleaned.describe()
    print(summary_stats)
    
    # Plot distribution of wind speed
    df_cleaned['WSPD'].hist(bins=20, figsize=(8, 6))
    plt.title('Distribution of Wind Speed')
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Frequency')
    plt.show()
    
    
    # Wind rose for Wind Speed (WSPD) and Wind Direction (WDIR)
    ax = WindroseAxes.from_ax()
    ax.bar(df_cleaned['WDIR'], df_cleaned['WSPD'], normed=True, opening=0.8, edgecolor='white')
    ax.set_title('Wind Rose Plot')
    plt.show()
    
    
    
    
    
        
    

if __name__ == '__main__':
    main()
