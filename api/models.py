from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class Transaction(BaseModel):
    sender: str
    recipient: str
    data: Dict[str, Any]
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class Block(BaseModel):
    index: int
    timestamp: datetime
    transactions: List[Transaction]
    proof: int
    previous_hash: str

class ChainResponse(BaseModel):
    chain: List[Block]
    length: int
