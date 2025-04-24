from typing import List
from pydantic import BaseModel

class Signal(BaseModel):
    symbol: str
    consensus: str
    confidence: float

class DashboardState:
    def __init__(self):
        self.signals: List[Signal] = []

    def update_signals(self, new_signals: List[Signal]):
        self.signals = new_signals

    def get_signals(self) -> List[Signal]:
        return self.signals

dashboard_state = DashboardState()
