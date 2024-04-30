
from flask import Flask, jsonify, request
import yfinance as yf
from datetime import datetime, timedelta
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

def get_data(symbol):
    stock = yf.Ticker(symbol)
    end_time = datetime.now() - timedelta(minutes=5)
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    data = stock.history(start=start_time, end=end_time, interval="2m")
    return data

def calculate_metrics(data):
    average_price = data['Close'].mean()
    average_volume_change = (data['Volume'].shift(1) - data['Volume']).mean()
    expectation = 'up' if data['Close'].iloc[-1] > data['Close'].iloc[0] else 'down'
    return average_price, average_volume_change, expectation

@app.route('/livedata')
def get_live_data():
    data = get_data("^GSPC")
    X = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in data.index]
    Y = data['Close'].tolist()
    V = data['Volume'].tolist()
    data_list = list(zip(X, Y, V))
    return jsonify(data_list)

@app.route('/7days')
def get_seven_days_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    stock = yf.Ticker("^GSPC")
    data = stock.history(start=start_date, end=end_date, interval="1d")
    average_price, average_volume_change, expectation = calculate_metrics(data)
    return jsonify({
        'average_price': average_price,
        'average_volume_change': average_volume_change,
        'expectation': expectation
    })

@app.route('/nasdaq/checkmarket/<float:percentage_change>')
def check_market_nasdaq(percentage_change):
    symbol = request.args.get('symbol', default="^IXIC", type=str)
    end_date = datetime.now()
    start_date = datetime.now().replace(hour=0, minute=0, second=0)
    data_today = yf.Ticker(symbol).history(start=start_date, end=end_date, interval="1m")
    if data_today.empty:
        return jsonify({'error': 'No data found for today'}), 404
    average_price_today = data_today['Close'].mean()
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=10)
    data_recent = yf.Ticker(symbol).history(start=start_time, end=end_time, interval="2m")
    if data_recent.empty:
        return jsonify({'error': 'No data found for the last 10 minutes'}), 404
    notifications = []
    last_above_threshold = False
    previous_time = None
    for index, row in data_recent.iterrows():
        current_price = row['Close']
        difference_percentage = ((current_price - average_price_today) / average_price_today) * 100
        if abs(difference_percentage) >= percentage_change:
            if last_above_threshold and previous_time:
                notifications.append(f"Market price was {'above' if difference_percentage > 0 else 'below'} the critical point by {abs(difference_percentage):.3f}% twice in a row starting at {previous_time}.")
            last_above_threshold = True
            previous_time = index.strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_above_threshold = False
    if notifications:
        return jsonify({'message': notifications[0]})
    else:
        return jsonify({'message': 'No significant changes detected.'})

@app.route('/sp500/checkmarket/<float:percentage_change>')
def check_market_sp500(percentage_change):
    symbol = request.args.get('symbol', default="^GSPC", type=str)
    end_date = datetime.now()
    start_date = datetime.now().replace(hour=0, minute=0, second=0)
    data_today = yf.Ticker(symbol).history(start=start_date, end=end_date, interval="1m")
    if data_today.empty:
        return jsonify({'error': 'No data found for today'}), 404
    average_price_today = data_today['Close'].mean()
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=10)
    data_recent = yf.Ticker(symbol).history(start=start_time, end=end_time, interval="2m")
    if data_recent.empty:
        return jsonify({'error': 'No data found for the last 10 minutes'}), 404
    notifications = []
    last_above_threshold = False
    previous_time = None
    for index, row in data_recent.iterrows():
        current_price = row['Close']
        difference_percentage = ((current_price

 - average_price_today) / average_price_today) * 100
        if abs(difference_percentage) >= percentage_change:
            if last_above_threshold and previous_time:
                notifications.append(f"Market price was {'above' if difference_percentage > 0 else 'below'} the critical point by {abs(difference_percentage):.3f}% twice in a row starting at {previous_time}.")
            last_above_threshold = True
            previous_time = index.strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_above_threshold = False
    if notifications:
        return jsonify({'message': notifications[0]})
    else:
        return jsonify({'message': 'No significant changes detected.'})

@app.route('/1month')
def get_one_month_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
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
    data = get_data("^GSPC")
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

@app.route('/nasdaq/livedata')
def get_nasdaq_live_data():
    data = get_data("^IXIC")
    X = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in data.index]
    Y = data['Close'].tolist()
    V = data['Volume'].tolist()
    data_list = list(zip(X, Y, V))
    return jsonify(data_list)

@app.route('/nasdaq/7days')
def get_nasdaq_seven_days_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
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
    data = get_data("^IXIC")
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

if __name__ == '__main__':
    app.run()
