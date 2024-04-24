from flask import Flask, jsonify, request
import yfinance as yf
from datetime import datetime, timedelta
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

def get_data(symbol):
    # Fetch historical data for the specified symbol
    stock = yf.Ticker(symbol)
    # Calculate the start and end time for fetching data
    end_time = datetime.now() - timedelta(minutes=5)  # 5 minutes older than current time
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    data = stock.history(start=start_time, end=end_time, interval="2m")
    return data

def calculate_metrics(data):
    # Calculate average price and average trade volume change
    average_price = data['Close'].mean()
    average_volume_change = (data['Volume'].shift(1) - data['Volume']).mean()
    # Determine expectation of going up or down based on the closing prices
    expectation = 'up' if data['Close'].iloc[-1] > data['Close'].iloc[0] else 'down'
    return average_price, average_volume_change, expectation

@app.route('/livedata')
def get_live_data():
    data = get_data("^GSPC")  # S&P 500 data
    X = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in data.index]
    Y = data['Close'].tolist()
    V = data['Volume'].tolist()
    data_list = list(zip(X, Y, V))
    return jsonify(data_list)

@app.route('/7days')
def get_seven_days_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    #data = get_data("^GSPC")  # S&P 500 data
    stock = yf.Ticker("^GSPC")
    data = stock.history(start=start_date, end=end_date, interval="1d")
    average_price, average_volume_change, expectation = calculate_metrics(data)
    return jsonify({
        'average_price': average_price,
        'average_volume_change': average_volume_change,
        'expectation': expectation
    })

@app.route('/1month')
def get_one_month_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    #data = get_data("^GSPC")  # S&P 500 data
    stock = yf.Ticker("^GSPC")
    data = stock.history(start=start_date, end=end_date, interval="1d")
    average_price, average_volume_change, expectation = calculate_metrics(data)
    return jsonify({
        'average_price': average_price,
        'average_volume_change': average_volume_change,
        'expectation': expectation
    })

@app.route('/compare')
def compare_latest_price():
    data = get_data("^GSPC")  # S&P 500 data
    average_percentage_change = (data['Close'].iloc[-1] - data['Close'].iloc[-8]) / data['Close'].iloc[-8] * 100
    latest_price = data['Close'].iloc[-1]
    threshold = 5
    if latest_price > average_percentage_change:
        message = f"The latest price ({latest_price}) change is greater than the average percentage change ({average_percentage_change}%)."
    elif latest_price < average_percentage_change:
        message = f"The latest price ({latest_price}) change is less than the average percentage change ({average_percentage_change}%)."
    else:
        message = "The latest price is equal to the average percentage change."
    return jsonify({'message': message})

# For NASDAQ
@app.route('/nasdaq/livedata')
def get_nasdaq_live_data():
    data = get_data("^IXIC")  # NASDAQ data
    X = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in data.index]
    Y = data['Close'].tolist()
    V = data['Volume'].tolist()
    data_list = list(zip(X, Y, V))
    return jsonify(data_list)

@app.route('/nasdaq/7days')
def get_nasdaq_seven_days_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    #data = get_data("")  # NASDAQ data
    stock = yf.Ticker("^IXIC")
    data = stock.history(start=start_date, end=end_date, interval="1d")
    average_price, average_volume_change, expectation = calculate_metrics(data)
    return jsonify({
        'average_price': average_price,
        'average_volume_change': average_volume_change,
        'expectation': expectation
    })

@app.route('/nasdaq/1month')
def get_nasdaq_one_month_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    stock = yf.Ticker("^IXIC")
    data = stock.history(start=start_date, end=end_date, interval="1d")
    average_price, average_volume_change, expectation = calculate_metrics(data)
    return jsonify({
        'average_price': average_price,
        'average_volume_change': average_volume_change,
        'expectation': expectation
    })

@app.route('/nasdaq/compare')
def compare_nasdaq_latest_price():
    data = get_data("^IXIC")  # NASDAQ data
    average_percentage_change = (data['Close'].iloc[-1] - data['Close'].iloc[-8]) / data['Close'].iloc[-8] * 100
    latest_price = data['Close'].iloc[-1]
    threshold = 5
    if latest_price > average_percentage_change:
        message = f"The latest price ({latest_price}) change is greater than the average percentage change ({average_percentage_change}%)."
    elif latest_price < average_percentage_change:
        message = f"The latest price ({latest_price}) change is less than the average percentage change ({average_percentage_change}%)."
    else:
        message = "The latest price is equal to the average percentage change."
    return jsonify({'message': message})


# Define the indices
indices = {
    'NASDAQ': '^IXIC',
    'S&P 500': '^GSPC',
    'Dow Jones': '^DJI'
}


def fetch_historical_data(start_date="1995-01-01", end_date="2024-04-01"):
    data = {}
    for name, ticker in indices.items():
        df = yf.download(ticker, start=start_date, end=end_date)
        if not df.empty:
            print(f"Data for {name} fetched successfully.")
            data[name] = df
        else:
            print(f"Failed to fetch data for {name}")
    return data


def detect_anomalies(df, days=2, threshold=15):
    anomalies = {}
    for column in df.columns:
        # Calculate the percentage change over the specified number of days
        df[f'{column} Pct Change'] = df[column].pct_change(periods=days) * 100

        # Find dates where the absolute percentage change is greater than the threshold
        significant_changes = df[np.abs(df[f'{column} Pct Change']) >= threshold]
        anomalies[column] = significant_changes.index.tolist()

    return anomalies


@app.route('/history')
def get_historical_data():
    start_date = request.args.get('start_date', default="1995-01-01", type=str)
    end_date = request.args.get('end_date', default="2024-04-01", type=str)
    data = fetch_historical_data(start_date, end_date)

    # Convert DataFrame to dictionary for each index
    data_dict = {}
    for name, df in data.items():
        data_dict[name] = df.to_dict(orient='list')

    return jsonify(data_dict)


@app.route('/anomalies')
def get_anomalies():
    start_date = request.args.get('start_date', default="1995-01-01", type=str)
    end_date = request.args.get('end_date', default="2024-04-01", type=str)
    data = fetch_historical_data(start_date, end_date)

    anomalies = {}
    for name, df in data.items():
        anomalies[name] = detect_anomalies(df)

    return jsonify(anomalies)









if __name__ == '__main__':
    app.run()
