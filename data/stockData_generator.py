import random
import string
from datetime import datetime, timedelta
import json


def generate_symbols(num_symbols=10, symbol_length=3):
    """
    Generate a list of unique symbols.

    :param num_symbols: Number of symbols to generate.
    :param symbol_length: Length of each symbol.
    :return: List of unique symbols.
    """
    symbols = []
    while len(symbols) < num_symbols:
        symbol = ''
        for _ in range(symbol_length):
            symbol += random.choice(string.ascii_uppercase)
        if symbol not in symbols:
            symbols.append(symbol)
    return symbols


def generate_mock_stock_data(num_records=100, start_date=datetime(2023, 1, 1), end_date=datetime(2023, 12, 31), initial_price_range=(50.0, 100.0), volatility=0.12):
    """
    Generate a list of stock data.
    :param num_records: Number of records to generate.
    :param start_date: Start date of record.
    :param end_date: End date of record.
    :param initial_price_range: Initial price range for different stocks.
    :param volatility: -
    :return: List of stock data
    """
    date_range = end_date - start_date
    date_list = []

    for _ in range(num_records):
        random_days = random.randint(0, date_range.days)
        date_list.append(start_date + timedelta(days=random_days))

    symbols = generate_symbols()  # Generating symbols

    stock_data = []

    for date in date_list:
        symbol = random.choice(symbols)

        # Randomize initial price within the specified range
        initial_price = random.uniform(initial_price_range[0], initial_price_range[1])

        price_change = random.uniform(-volatility, volatility)
        close_price = initial_price * (1 + price_change)
        high = initial_price * random.uniform(1.01, 1.25)
        low = initial_price * random.uniform(0.75, 0.99)
        volume = random.randint(100000, 500000)

        hours = random.randint(9, 15)
        minutes = random.randint(30, 59)
        seconds = random.randint(0, 59)
        timestamp = datetime(date.year, date.month, date.day, hours, minutes, seconds)

        daily_price_change = round(close_price - initial_price, 2)  # Calculate daily price change

        stock_data.append({
            'symbol': symbol,
            'timestamp': int(timestamp.timestamp()),
            'open_price': round(initial_price, 2),
            'close_price': round(close_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'volume': volume,
            'daily_price_change': daily_price_change
        })

    return stock_data


def generate_json_file(file_path, stock_data):

    try:
        with open(file_path, 'w') as json_file:
            json.dump(stock_data, json_file, indent=2)

        print(f'{file_path} has been generated.\n')

    except Exception as e:
        print(f'Error writing to {file_path}: {e}')



# Load all data into json file for streaming
data = generate_mock_stock_data()
generate_json_file('data.json', data)


if __name__ == "__main__":
    num_records = 100
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    initial_price_range = (50.0, 110.0)
    volatility = 0.12

    mock_stock_data = generate_mock_stock_data(num_records, start_date, end_date, initial_price_range, volatility)

    for data_point in mock_stock_data:
        print(f"Symbol: {data_point['symbol']}, "
              f"Timestamp: {datetime.fromtimestamp(data_point['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}, "
              f"Open Price: ${data_point['open_price']}, "
              f"Close Price: ${data_point['close_price']}, "
              f"High: ${data_point['high']}, "
              f"Low: ${data_point['low']}, "
              f"Volume: {data_point['volume']} shares",
              f"Daily Price Change: ${data_point['daily_price_change']}")
