from typing import List, Dict, Any
from time import time

class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict[str, Any]], 
                 proof: int, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует блок в словарь"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash,
        }
