# MT5 Position Tracker

A full-stack application that tracks and displays opened positions from MetaTrader 5 using FastAPI, SQLite, and a modern UI built with Tailwind CSS and DaisyUI.

## Features

- Real-time position tracking from MT5
- Beautiful and responsive UI
- Position history tracking
- Auto-refresh functionality
- Position type categorization (bullish/bearish)
- Detailed position information display

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

## Running the Application

1. Make sure MetaTrader 5 is running and you're logged in
2. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

3. Open your browser and navigate to `http://localhost:8000`

## API Endpoints

- `GET /`: Main application interface
- `GET /positions/`: Get all currently opened positions
- `GET /positions/history`: Get position history (including closed positions)

## Tech Stack

- Backend: FastAPI
- Database: SQLite
- Frontend: HTML, Tailwind CSS, DaisyUI
- Trading Platform Integration: MetaTrader 5 Python package

## License

MIT
