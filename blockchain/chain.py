import hashlib
import json
from time import time
from typing import List, Dict, Any, Optional

from blockchain.block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # Создание генезис-блока
        self.create_block(previous_hash="1", proof=100)
    
    def create_block(self, proof: int, previous_hash: str) -> Dict[str, Any]:
        """Создает новый блок в блокчейне"""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        
        # Сбрасываем текущий список транзакций
        self.current_transactions = []
        
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender: str, recipient: str, data: Dict[str, Any]) -> int:
        """
        Добавляет новую транзакцию в список транзакций
        
        :param sender: Адрес отправителя
        :param recipient: Адрес получателя
        :param data: Данные транзакции
        :return: Индекс блока, в который будет добавлена транзакция
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'data': data,
            'timestamp': time(),
        })
        
        return self.last_block['index'] + 1
    
    @property
    def last_block(self) -> Dict[str, Any]:
        """Возвращает последний блок в цепочке"""
        return self.chain[-1]
    
    def proof_of_work(self, last_proof: int) -> int:
        """
        Простой алгоритм Proof of Work:
        - Найти число p', такое что hash(pp') содержит 4 ведущих нуля
        - p - предыдущий proof, p' - новый proof
        
        :param last_proof: Последний proof
        :return: Новый proof
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof
    
    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Проверяет, содержит ли hash(last_proof, proof) 4 ведущих нуля
        
        :param last_proof: Предыдущий proof
        :param proof: Текущий proof
        :return: True, если корректно, иначе False
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
    def mine_block(self) -> Dict[str, Any]:
        """
        Майнит новый блок
        
        :return: Новый блок
        """
        # Запускаем алгоритм Proof of Work для нахождения нового proof
        last_block = self.last_block
        last_proof = last_block['proof']
        proof = self.proof_of_work(last_proof)
        
        # Вознаграждение за proof of work
        # Отправитель "0" означает, что этот узел добыл новую монету
        self.add_transaction(
            sender="0",
            recipient="node",
            data={"message": "Новый блок создан"},
        )
        
        # Создаем новый блок путем добавления его в цепочку
        previous_hash = self.hash(last_block)
        block = self.create_block(proof, previous_hash)
        
        return block
    
    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        """
        Создает SHA-256 хеш блока
        
        :param block: Блок для хеширования
        :return: Хеш
        """
        # Необходимо убедиться, что словарь упорядочен, иначе будут непоследовательные хеши
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def is_chain_valid(self) -> bool:
        """
        Проверяет, является ли текущая цепочка валидной
        
        :return: True, если цепочка валидна, иначе False
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Проверяем, что хеш блока корректный
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            
            # Проверяем, что proof of work корректный
            if not self.valid_proof(previous_block['proof'], current_block['proof']):
                return False
        
        return True
    
    def get_chain(self) -> List[Dict[str, Any]]:
        """Возвращает текущую цепочку блоков"""
        return self.chain
