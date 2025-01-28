from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Position(BaseModel):
    id: int
    symbol: str
    volume: float
    price: float
    type: str  # 'bullish' or 'bearish'
    status: str  # 'opened' or 'closed'
    timestamp: Optional[datetime] = None

class PositionCreate(BaseModel):
    symbol: str
    volume: float
    price: float
    type: str
    status: str = "opened"
