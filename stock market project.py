import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# Initialize the Alpaca client with your API keys
alpaca_client = TradingClient('PKTM9MMWZ6W4JYXC0WDF', '1KXn0xbDyHebxc8mvzjNmTNvkIbOofzSav8o11fH', paper=True)

# List of popular soda companies
soda_stocks = ["KO", "PEP", "DAN", "COT", "SBUX"]

def get_stock_data(stock):
    """Fetch the latest stock data from Polygon.io."""
    url = f'https://api.polygon.io/v2/aggs/ticker/{stock}/prev?apiKey=js1m5p3WRvg9VkO5M3pbQNXQYQRVvDTO
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]  # Return the latest data
        else:
            print(f"No results found for {stock}.")
            return None
    else:
        print(f"Error fetching data for {stock}: {response.status_code} - {response.text}")
        return None

def trade_soda_stocks(stocks):
    for stock in stocks:
        stock_data = get_stock_data(stock)

        if stock_data:
            
            last_price = stock_data['c']  # Get the last closing price
            print(f"Last price for {stock}: ${last_price}")

            # Prepare the market order to buy the stock
            market_order_data = MarketOrderRequest(
                symbol=stock,
                qty=1,  # Buy 1 share; adjust as needed
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )

            try:
                # Submit the market order
                market_order = alpaca_client.submit_order(order_data=market_order_data)
                print(f"Successfully bought 1 share of {stock}. Order ID: {market_order.id}")
            except Exception as e:
                print(f"Error buying {stock}: {e}")

def main():
    print(f"Attempting to buy soda stocks: {soda_stocks}")
    trade_soda_stocks(soda_stocks)

if __name__ == "__main__":
    main()
