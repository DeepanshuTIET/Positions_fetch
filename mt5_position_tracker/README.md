# MT5 Position Tracker

A full-stack application that tracks and displays opened positions from MetaTrader 5 using Flask, SQLite, and a modern UI.

## Features

- Real-time position tracking from MT5
- Position history tracking
- Auto-refresh functionality
- Position type categorization
- Detailed position information display
- Current BTC price tracking from Binance

## Prerequisites

- Python 3.8+
- MetaTrader 5 installed and configured
- pip (Python package manager)

## Installation

1. Clone this repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your MT5 credentials:
```
MT5_LOGIN=your_login
MT5_PASSWORD=your_password
MT5_SERVER=your_server
```

## Running the Application

1. Make sure MetaTrader 5 is running and you're logged in
2. Start the Flask server:
```bash
python -m app.main
```

3. Open your browser and navigate to `http://localhost:5000`

## API Endpoints

- `GET /`: Main application interface
- `GET /positions`: Get all currently opened positions
- `GET /btc-price`: Get current BTC price from Binance

## Tech Stack

- Backend: Flask
- Database: SQLite
- External APIs: MetaTrader5, Binance
- Dependencies: See requirements.txt for full list

## Environment Variables

- `MT5_LOGIN`: Your MetaTrader 5 account login
- `MT5_PASSWORD`: Your MetaTrader 5 account password
- `MT5_SERVER`: Your MetaTrader 5 server name
