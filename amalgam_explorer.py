import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

app = FastAPI(title="Amalgam Blockchain Explorer")
templates = Jinja2Templates(directory="templates")

# Модели данных
class Transaction(BaseModel):
    tx_id: str
    from_addr: str
    to_addr: str
    arc_value: float
    details: str
    timestamp: str
    signatures: List[str]

class Content(BaseModel):
    content_id: str
    author: str
    type: str
    content_hash: str
    target: str
    weight: int
    timestamp: str

class User(BaseModel):
    address: str
    arc: float
    hrc: float
    transactions: List[str]
    role: str

# Симуляция блокчейна
blockchain: Dict[str, List] = {"users": [], "transactions": [], "content": []}

# Инициализация данных
def init_blockchain():
    users = [
        User(address="0xSIDR123", arc=302.2, hrc=10, transactions=[], role="cider_factory"),
        User(address="0xGARDENER456", arc=259, hrc=0, transactions=[], role="gardener"),
        User(address="0xSEEDSELLER123", arc=95, hrc=10, transactions=[], role="seed_seller"),
        User(address="0xBOTTLE789", arc=150, hrc=0, transactions=[], role="bottle_seller"),
        User(address="0xDESIGN901", arc=50, hrc=0, transactions=[], role="designer"),
        User(address="0xRESIDENT111", arc=47.8, hrc=0, transactions=[], role="resident"),
        User(address="0xBLOGGER789", arc=40, hrc=0, transactions=[], role="blogger"),
        User(address="0xRESIDENT222", arc=120, hrc=5, transactions=[], role="resident"),
        User(address="0xFARMER789", arc=180, hrc=0, transactions=[], role="farmer"),
    ]

    transactions = [
        # Сидр-завод
        Transaction(tx_id="TX1234", from_addr="0xGARDENER456", to_addr="0xSIDR123", arc_value=320, details="800 kg apples at 0.4 ARC/kg", timestamp="2025-03-16T12:00:00Z", signatures=["sig_gardener", "sig_sidr"]),
        Transaction(tx_id="TX5678", from_addr="0xBOTTLE789", to_addr="0xSIDR123", arc_value=100, details="200 bottles at 0.5 ARC/bottle", timestamp="2025-03-16T13:00:00Z", signatures=["sig_bottle", "sig_sidr"]),
        Transaction(tx_id="TX9012", from_addr="0xDESIGN901", to_addr="0xSIDR123", arc_value=50, details="label design, 5 hours", timestamp="2025-03-16T14:00:00Z", signatures=["sig_design", "sig_sidr"]),
        Transaction(tx_id="TX9999", from_addr="0xRESIDENT111", to_addr="0xSIDR123", arc_value=2.2, details="1 liter cider, negotiated from 2.5 ARC", timestamp="2025-03-16T15:00:00Z", signatures=["sig_resident", "sig_sidr"]),
        Transaction(tx_id="TX1000", from_addr="0xRESIDENT222", to_addr="0xSIDR123", arc_value=4.4, details="2 liters cider, negotiated from 5 ARC", timestamp="2025-03-17T09:00:00Z", signatures=["sig_resident2", "sig_sidr"]),
        
        # Садовник
        Transaction(tx_id="TX4321", from_addr="0xGARDENER456", to_addr="0xSEEDSELLER123", arc_value=50, details="50 seedlings purchased", timestamp="2025-03-15T10:00:00Z", signatures=["sig_gardener", "sig_seedseller"]),
        Transaction(tx_id="TX8765", from_addr="0xGARDENER456", to_addr="0xSEEDSELLER123", arc_value=5, details="Thanks for quality seedlings", timestamp="2025-03-17T12:00:00Z", signatures=["sig_gardener", "sig_seedseller"]),
        Transaction(tx_id="TX5000", from_addr="0xGARDENER456", to_addr="0xFARMER789", arc_value=20, details="Seeds exchange", timestamp="2025-03-18T08:00:00Z", signatures=["sig_gardener", "sig_farmer"]),
        
        # Продавец саженцев
        Transaction(tx_id="TX6000", from_addr="0xSEEDSELLER123", to_addr="0xFARMER789", arc_value=30, details="100 seedlings sold", timestamp="2025-03-16T11:00:00Z", signatures=["sig_seedseller", "sig_farmer"]),
        
        # Жители
        Transaction(tx_id="TX7000", from_addr="0xRESIDENT111", to_addr="0xBOTTLE789", arc_value=1, details="Returned 10 bottles", timestamp="2025-03-17T14:00:00Z", signatures=["sig_resident", "sig_bottle"]),
        Transaction(tx_id="TX8000", from_addr="0xRESIDENT222", to_addr="0xDESIGN901", arc_value=10, details="Custom label request", timestamp="2025-03-18T10:00:00Z", signatures=["sig_resident2", "sig_design"]),
    ]

    content = [
        Content(content_id="CONTENT5678", author="0xBLOGGER789", type="article", content_hash="ipfs://QmFakeNews123", target="0xSEEDSELLER123", weight=-6, timestamp="2025-03-16T10:00:00Z"),
        Content(content_id="CONTENT9000", author="0xRESIDENT111", type="review", content_hash="ipfs://QmGoodReview", target="0xSIDR123", weight=5, timestamp="2025-03-17T13:00:00Z"),
    ]

    for tx in transactions:
        for user in users:
            if user.address in [tx.from_addr, tx.to_addr]:
                user.transactions.append(tx.tx_id)

    blockchain["users"] = [u.dict() for u in users]
    blockchain["transactions"] = [t.dict() for t in transactions]
    blockchain["content"] = [c.dict() for c in content]

init_blockchain()

@app.get("/address/{address}")
async def get_address(request: Request, address: str):
    user = next((u for u in blockchain["users"] if u["address"] == address), None)
    if not user:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Address not found"})

    incoming_txs = [tx for tx in blockchain["transactions"] if tx["to_addr"] == address]
    outgoing_txs = [tx for tx in blockchain["transactions"] if tx["from_addr"] == address]
    related_content = [c for c in blockchain["content"] if c["target"] == address or c["author"] == address]

    # Специфичные данные для сидр-завода
    supply_chain = {"apples": {}, "bottles": {}, "design": {}} if address != "0xSIDR123" else {
        "apples": {"supplier": "0xGARDENER456", "quantity": "800 kg", "arc_cost": 320, "details": "Negotiated at 0.4 ARC/kg"},
        "bottles": {"supplier": "0xBOTTLE789", "quantity": "200 bottles", "arc_cost": 100, "details": "0.5 ARC/bottle"},
        "design": {"supplier": "0xDESIGN901", "service": "Label design", "arc_cost": 50, "details": "5 hours work"}
    }

    sales = {} if address != "0xSIDR123" else {
        "resident": {"buyer": "0xRESIDENT111", "quantity": "1 liter", "arc_received": 2.2, "details": "Negotiated from 2.5 ARC"}
    }

    neural_insights = {
        "demand_trend": "High demand for cider (+30% transactions last week)" if address == "0xSIDR123" else "Stable demand",
        "diversity_factor": 20 if address == "0xSIDR123" else 10,
        "anomaly_check": "No suspicious patterns detected",
        "recommendation": "Consider producing pear cider, demand up by 15%" if address == "0xSIDR123" else "Diversify products"
    }

    return templates.TemplateResponse("address.html", {
        "request": request,
        "address": user["address"],
        "arc": user["arc"],
        "hrc": user["hrc"],
        "role": user["role"],
        "supply_chain": supply_chain,
        "sales": sales,
        "incoming_txs": incoming_txs,
        "outgoing_txs": outgoing_txs,
        "content": related_content,
        "neural_insights": neural_insights
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)