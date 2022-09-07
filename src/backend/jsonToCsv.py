def candles_to_csv(array):
    array = np.array(array)
    df = pd.DataFrame(array)
    df.rename(columns={0: 'Date', 1: 'Open', 2: 'High', 3:'Low', 4: 'Close', 5: 'Volume'}, inplace=True)
    df.to_csv('reliance.csv')

def jsonToCsv(filename):
    candle = []
    data = json.loads(data)
    if data["status"] == "success":
        for candle in data["data"]["candles"]:
            # time, open_price, open_high, open_low, close_price, volume, _ = candle
            candles.append(candle)
    return candle

if __name__ == "__main__":
    jsonToCsv('../../data/sbin-')