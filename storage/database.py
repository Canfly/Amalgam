import os
import json
from typing import List, Dict, Any, Optional
import asyncpg
from asyncpg.pool import Pool

class DatabaseManager:
    def __init__(self):
        self.pool: Optional[Pool] = None
        self.connection_string = os.environ.get("DATABASE_URL")
        if not self.connection_string:
            raise ValueError("DATABASE_URL environment variable not set")

    async def initialize(self):
        self.pool = await asyncpg.create_pool(self.connection_string)
        await self._create_tables()

    async def close(self):
        if self.pool:
            await self.pool.close()
    
    async def _create_tables(self):
        """Create necessary tables if they don't exist."""
        async with self.pool.acquire() as conn:
            # Создаем таблицу для блоков
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS blocks (
                    id SERIAL PRIMARY KEY,
                    index INTEGER NOT NULL,
                    timestamp DOUBLE PRECISION NOT NULL,
                    proof INTEGER NOT NULL,
                    previous_hash TEXT NOT NULL,
                    block_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Создаем таблицу для транзакций
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    block_index INTEGER NOT NULL,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    data JSONB NOT NULL,
                    timestamp DOUBLE PRECISION NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (block_index) REFERENCES blocks(index)
                )
            ''')

    async def save_block(self, block: Dict[str, Any], block_hash: str) -> int:
        """Save a block to the database and return its index."""
        async with self.pool.acquire() as conn:
            block_id = await conn.fetchval('''
                INSERT INTO blocks (index, timestamp, proof, previous_hash, block_hash)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING index
            ''', block['index'], block['timestamp'], block['proof'], 
                block['previous_hash'], block_hash)
            
            # Сохраняем все транзакции блока
            for tx in block['transactions']:
                await conn.execute('''
                    INSERT INTO transactions 
                    (block_index, sender, recipient, data, timestamp)
                    VALUES ($1, $2, $3, $4, $5)
                ''', block['index'], tx['sender'], tx['recipient'], 
                    json.dumps(tx['data']), tx['timestamp'])
            
            return block_id

    async def get_full_chain(self) -> List[Dict[str, Any]]:
        """Get the entire blockchain from the database."""
        async with self.pool.acquire() as conn:
            blocks = await conn.fetch('''
                SELECT * FROM blocks ORDER BY index ASC
            ''')
            
            chain = []
            for block in blocks:
                # Получаем транзакции для блока
                transactions = await conn.fetch('''
                    SELECT * FROM transactions WHERE block_index = $1
                ''', block['index'])
                
                tx_list = []
                for tx in transactions:
                    tx_list.append({
                        'sender': tx['sender'],
                        'recipient': tx['recipient'],
                        'data': json.loads(tx['data']),
                        'timestamp': tx['timestamp']
                    })
                
                chain.append({
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'transactions': tx_list,
                    'proof': block['proof'],
                    'previous_hash': block['previous_hash']
                })
            
            return chain
    
    async def get_block(self, index: int) -> Optional[Dict[str, Any]]:
        """Get a specific block by index."""
        async with self.pool.acquire() as conn:
            block = await conn.fetchrow('''
                SELECT * FROM blocks WHERE index = $1
            ''', index)
            
            if not block:
                return None
            
            # Получаем транзакции для блока
            transactions = await conn.fetch('''
                SELECT * FROM transactions WHERE block_index = $1
            ''', block['index'])
            
            tx_list = []
            for tx in transactions:
                tx_list.append({
                    'sender': tx['sender'],
                    'recipient': tx['recipient'],
                    'data': json.loads(tx['data']),
                    'timestamp': tx['timestamp']
                })
            
            return {
                'index': block['index'],
                'timestamp': block['timestamp'],
                'transactions': tx_list,
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
            }
