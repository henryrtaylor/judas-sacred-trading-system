
from polygon_utils import get_polygon_price_data

def ai_solver(symbols):
    price_data = {}
    for symbol in symbols:
        try:
            df = get_polygon_price_data(symbol)
            price_data[symbol] = df
        except Exception as e:
            print(f"⚠️ {symbol} failed AI prediction: {e}")
            continue
    return price_data
