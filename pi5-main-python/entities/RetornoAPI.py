from dataclasses import dataclass
from typing import List

@dataclass
class HistoricalDataPrice:
    data: int
    close: float
    open: float
    high: float
    low: float

@dataclass
class Result:
    longName: str
    symbol: str
    logourl: str
    historicalDataPrice: List[HistoricalDataPrice]

@dataclass
class RetornoAPI:
    results: List[Result]
