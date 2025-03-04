from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from blockchain.chain import Blockchain
from api.models import Transaction, Block, ChainResponse

router = APIRouter(tags=["blockchain"])

# Функция для получения экземпляра блокчейна
def get_blockchain():
    # В реальном приложении здесь можно было бы использовать зависимость для получения блокчейна
    from api.main import blockchain
    return blockchain

@router.get("/chain", response_model=ChainResponse)
async def get_chain(blockchain: Blockchain = Depends(get_blockchain)):
    """Получить всю цепочку блоков"""
    chain = blockchain.get_chain()
    return {"chain": chain, "length": len(chain)}

@router.get("/block/{index}", response_model=Block)
async def get_block(index: int, blockchain: Blockchain = Depends(get_blockchain)):
    """Получить блок по индексу"""
    chain = blockchain.get_chain()
    if 0 <= index < len(chain):
        return chain[index]
    raise HTTPException(status_code=404, detail="Блок не найден")

@router.post("/transactions/new", response_model=Dict[str, str])
async def new_transaction(transaction: Transaction, blockchain: Blockchain = Depends(get_blockchain)):
    """Добавить новую транзакцию"""
    # Добавляем транзакцию в блокчейн
    index = blockchain.add_transaction(
        sender=transaction.sender,
        recipient=transaction.recipient,
        data=transaction.data
    )
    return {"message": f"Транзакция будет добавлена в блок {index}"}

@router.post("/mine", response_model=Block)
async def mine_block(blockchain: Blockchain = Depends(get_blockchain)):
    """Создать новый блок (майнинг)"""
    # Майним новый блок
    block = blockchain.mine_block()
    return block

@router.get("/validate", response_model=Dict[str, bool])
async def validate_chain(blockchain: Blockchain = Depends(get_blockchain)):
    """Проверить валидность цепочки блоков"""
    valid = blockchain.is_chain_valid()
    return {"valid": valid}
