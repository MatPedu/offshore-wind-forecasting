import requests
import pandas as pd


def load_data(station_number: int):
    
    url = f'https://www.ndbc.noaa.gov/data/realtime2/{station_number}.txt'

    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
    # Save the content to a local file
        with open(f'data/downloaded_file_{station_number}.txt', 'wb') as file:
            file.write(response.content)

        print("File downloaded successfully!")

    else:
        print(f"Failed to retrieve the file. Status code: {response.status_code}")

def create_dataframe(station_number: int):
    
    # Now load the downloaded file into a DataFrame
    df = pd.read_csv(f'data/downloaded_file_{station_number}.txt', delim_whitespace=True, skiprows=2)

    # Rename the columns
    df.columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']

    # Display the first few rows of the dataframe
    print(df.head())

def main():
    # URL of the .txt file
    station_numbers = [44013]
    
    for station_number in station_numbers:
        load_data(station_number)
        create_dataframe(station_number)
        
    

if __name__ == '__main__':
    main()
