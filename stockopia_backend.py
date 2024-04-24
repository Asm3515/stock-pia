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


from datetime import timedelta


def check_market_behavior(symbol, duration=timedelta(minutes=20), interval=timedelta(minutes=5)):
    """
    Check market behavior over a specified duration.
    Returns True if the market has fallen or risen, otherwise False.
    """

    stock = yf.Ticker(symbol)
    # Get data for the specified duration
    end_time = datetime.now()
    start_time = end_time - duration

    data = stock.history(start=start_time, end=end_time, interval="1m")

    # Calculate percentage change over the duration
    percentage_change = (data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100

    return percentage_change
def compare_and_alert(symbol):
    # Get data for the last 7 days

    percentage_change_20_minutes = check_market_behavior(symbol)

    stock = yf.Ticker(symbol)
    end_date_7days = datetime.now()
    start_date_7days = end_date_7days - timedelta(days=7)
    data_7days = stock.history(start=start_date_7days, end=end_date_7days, interval="5m")

    # Calculate average price for the last 7 days
    average_price_7days = data_7days['Close'].mean()

    # Get data for the last 1 month
    end_date_1month = datetime.now()
    start_date_1month = end_date_1month - timedelta(days=30)
    data_1month = stock.history(start=start_date_1month, end=end_date_1month, interval="5m")
    threshold = 0.5
    # Calculate average price for the last 1 month
    average_price_1month = data_1month['Close'].mean()

    # Check if the market has fallen or risen in the last 20 minutes
    if percentage_change_20_minutes < -threshold:
        alert_message = f"The market has fallen by {abs(percentage_change_20_minutes):.2f}% in the last 20 minutes."
    elif percentage_change_20_minutes > threshold:
        alert_message = f"The market has risen by {percentage_change_20_minutes:.2f}% in the last 20 minutes."
    else:
        alert_message = "OK"

    # Compare last 7 days average with last 1 month average
    if average_price_7days > average_price_1month:
        alert_message = f"The average price for the last 7 days ({average_price_7days}) is higher than the average price for the last 1 month ({average_price_1month})."
    elif average_price_7days < average_price_1month:
        alert_message = f"The average price for the last 7 days ({average_price_7days}) is lower than the average price for the last 1 month ({average_price_1month})."
    else:
        alert_message = "The average prices for the last 7 days and the last 1 month are equal."

    # Check recent market behavior
    data_recent = get_data(symbol)
    latest_price = data_recent['Close'].iloc[-1]
    average_percentage_change = (data_recent['Close'].iloc[-1] - data_recent['Close'].iloc[-8]) / data_recent['Close'].iloc[-8] * 100

    # Define threshold for market behavior
    threshold = 0.5  # 0.5 percentage change
    if latest_price < average_price_7days - threshold:
        alert_message += f" The market has fallen by {threshold}% compared to the average price for the last 7 days."
    elif latest_price > average_price_7days + threshold:
        alert_message += f" The market has risen by {threshold}% compared to the average price for the last 7 days."

    # If no alert conditions are met, return "OK"
    if "fallen" not in alert_message.lower() and "risen" not in alert_message.lower():
        return "OK"
    else:
        return alert_message

@app.route('/alert')
def get_alert():
    symbol = request.args.get('symbol', default="^GSPC", type=str)  # Default to S&P 500 if symbol is not provided
    alert_message = compare_and_alert(symbol)
    return jsonify({'alert_message': alert_message})

@app.route('/nasdaq/alert')
def get_nasdaq_alert():  # Renamed the function to 'get_nasdaq_alert'
    symbol = request.args.get('symbol', default="^IXIC", type=str)  # Default to NASDAQ if symbol is not provided
    alert_message = compare_and_alert(symbol)
    return jsonify({'alert_message': alert_message})




if __name__ == '__main__':
    app.run()
