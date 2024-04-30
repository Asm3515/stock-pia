def get_data(symbol):
    stock = yf.Ticker(symbol)
    end_time = datetime.now() - timedelta(minutes=5)
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    data = stock.history(start=start_time, end=end_time, interval="2m")
    return data


def get_live_data():
    data = get_data("^GSPC")
    X = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in data.index]
    Y = data['Close'].tolist()
    V = data['Volume'].tolist()
    data_list = list(zip(X, Y, V))
    return jsonify(data_list)