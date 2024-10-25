import sys

sys.path.append('..')

def main():
    
    with open('data/stations_files/no_historical_data_stations.txt') as f:
        print(f.read())
        

if __name__ == '__main__':
    main()