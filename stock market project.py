import requests
import os
import logging
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# Load environment variables from .env file
load_dotenv()

# Set up API base URL and keys from environment variables
API_BASE_URL = os.getenv("APCA_API_BASE_URL")
API_KEY_ID = os.getenv("APCA_API_KEY_ID")
API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# Verify environment variables
if not all([API_KEY_ID, API_SECRET_KEY, POLYGON_API_KEY]):
    print("Error: Missing one or more required environment variables.")
    print("API_KEY_ID:", API_KEY_ID)
    print("API_SECRET_KEY:", API_SECRET_KEY)
    print("POLYGON_API_KEY:", POLYGON_API_KEY)
    exit(1)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the Alpaca client
alpaca_client = TradingClient(API_KEY_ID, API_SECRET_KEY, paper=True)

# List of popular soda companies
soda_stocks = ["KO", "PEP", "DAN", "COT", "SBUX"]

def get_stock_data(stock):
    """Fetch the latest stock data from Polygon.io."""
    url = f'https://api.polygon.io/v2/aggs/ticker/{stock}/prev?apiKey={POLYGON_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]
        else:
            logging.warning(f"No results found for {stock}.")
            return None
    else:
        logging.error(f"Error fetching data for {stock}: {response.status_code} - {response.text}")
        return None

def trade_soda_stocks(stocks):
    for stock in stocks:
        stock_data = get_stock_data(stock)

        if stock_data:
            last_price = stock_data['c']
            logging.info(f"Last price for {stock}: ${last_price}")

            market_order_data = MarketOrderRequest(
                symbol=stock,
                qty=1,  # Adjust quantity as needed
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )

            try:
                market_order = alpaca_client.submit_order(order_data=market_order_data)
                logging.info(f"Successfully bought 1 share of {stock}. Order ID: {market_order.id}")
            except Exception as e:
                logging.error(f"Error buying {stock}: {e}")

def main():
    logging.info(f"Attempting to buy soda stocks: {soda_stocks}")
    trade_soda_stocks(soda_stocks)

if __name__ == "__main__":
    main()
