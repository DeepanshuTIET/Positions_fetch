from flask import Flask, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import MetaTrader5 as mt5
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import time
import logging
import threading

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

def init_mt5():
    """Initialize MT5 connection"""
    try:
        logger.info("Checking MT5 terminal status...")
        terminal_info = mt5.terminal_info()
        if terminal_info is not None:
            logger.info(f"MT5 terminal info: Connected={terminal_info.connected}, Trade_allowed={terminal_info.trade_allowed}")
        else:
            logger.warning("Could not get terminal info")

        # Check if MT5 is already initialized
        if mt5.initialize():
            logger.info("MT5 was already initialized")
            
            # Verify login status
            account_info = mt5.account_info()
            if account_info is not None:
                logger.info(f"Already logged in as: Server={account_info.server}, Login={account_info.login}")
                return True
            else:
                logger.warning("Not logged in despite MT5 being initialized")
        
        logger.info("Initializing MT5...")
        if not mt5.initialize():
            error_code = mt5.last_error()
            error_desc = mt5.last_error_str()
            logger.error(f"MT5 initialization failed! Error code: {error_code}, Description: {error_desc}")
            return False
        
        # MT5 login credentials
        login = int(os.getenv('MT5_LOGIN'))
        password = os.getenv('MT5_PASSWORD')
        server = os.getenv('MT5_SERVER')
        
        logger.info(f"Attempting to login to MT5... Server: {server}, Login: {login}")
        
        # Enable trading
        mt5.terminal_info_integer(mt5.TERMINAL_TRADE_ALLOWED)
        
        # Attempt to login
        if not mt5.login(login=login, password=password, server=server):
            error_code = mt5.last_error()
            error_desc = mt5.last_error_str()
            logger.error(f"MT5 login failed! Error code: {error_code}, Description: {error_desc}")
            return False
        
        account_info = mt5.account_info()
        if account_info is not None:
            logger.info(f"MT5 initialized and logged in successfully! Account: {account_info.login}@{account_info.server}")
        else:
            logger.warning("MT5 initialized but couldn't get account info")
        
        return True
    except Exception as e:
        logger.error(f"Error in init_mt5: {str(e)}")
        return False

# Initialize MT5
init_mt5()

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

@app.route('/positions/')
@app.route('/positions')
def get_positions():
    """Get all opened positions from MT5"""
    try:
        logger.info("Fetching positions...")
        
        # Check MT5 connection status
        terminal_info = mt5.terminal_info()
        if terminal_info is None or not terminal_info.connected:
            logger.warning("MT5 terminal not connected. Attempting to reinitialize...")
            if not init_mt5():
                logger.error("Failed to reinitialize MT5")
                return jsonify({"error": "MT5 terminal not connected"}), 500

        # Get positions with retry
        max_retries = 3
        positions = None
        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1} to fetch positions...")
                positions = mt5.positions_get()
                
                if positions is not None:
                    logger.info(f"Successfully fetched {len(positions)} positions")
                    break
                    
                last_error = mt5.last_error()
                error_desc = mt5.last_error_str()
                logger.warning(f"Attempt {attempt + 1} failed. Error code: {last_error}, Description: {error_desc}")
                
                # Check account info
                account_info = mt5.account_info()
                if account_info is None:
                    logger.warning("Lost connection to account. Attempting to reconnect...")
                    init_mt5()
                
                time.sleep(1)  # Wait before retry
                
            except Exception as e:
                last_error = str(e)
                logger.error(f"Error in attempt {attempt + 1}: {last_error}")
                time.sleep(1)
        
        if positions is None:
            if last_error:
                logger.error(f"Failed to fetch positions after {max_retries} attempts. Last error: {last_error}")
                return jsonify({"error": f"Failed to fetch positions: {last_error}"}), 500
            logger.info("No positions found")
            return jsonify([])

        # Format positions
        formatted_positions = []
        for pos in positions:
            try:
                formatted_positions.append({
                    'symbol': pos.symbol,
                    'volume': pos.volume,
                    'price': pos.price_open,
                    'type': "bullish" if pos.type == mt5.POSITION_TYPE_BUY else "bearish",
                    'ticket': pos.ticket,
                    'time': datetime.fromtimestamp(pos.time).isoformat()
                })
            except Exception as e:
                logger.error(f"Error formatting position {pos}: {str(e)}")
                continue
            
        logger.info(f"Returning {len(formatted_positions)} formatted positions")
        return jsonify(formatted_positions)
    
    except Exception as e:
        logger.error(f"Error in get_positions: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Global variable to store the latest BTC price
latest_btc_price = None
price_lock = threading.Lock()

def fetch_btc_price_continuously():
    """Background task to continuously fetch BTC price"""
    global latest_btc_price
    while True:
        try:
            response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
            if response.status_code == 200:
                with price_lock:
                    latest_btc_price = float(response.json()['price'])
                logger.debug(f"Updated BTC price: {latest_btc_price}")
        except Exception as e:
            logger.error(f"Error fetching BTC price: {e}")
        time.sleep(0.1)  # 100ms delay between requests

@app.route('/btc-price')
def get_btc_price():
    """Get the latest BTC price"""
    with price_lock:
        if latest_btc_price is None:
            return jsonify({'error': 'BTC price not available yet'}), 503
        return jsonify({'price': latest_btc_price})

# Start the background thread for BTC price updates
btc_price_thread = threading.Thread(target=fetch_btc_price_continuously, daemon=True)
btc_price_thread.start()

# Cleanup MT5 connection when the application exits
import atexit

@atexit.register
def cleanup():
    logger.info("Shutting down MT5...")
    mt5.shutdown()

if __name__ == '__main__':
    app.run(debug=True)
