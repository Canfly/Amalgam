from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
from datetime import datetime
import json

from blockchain.chain import Blockchain
from api.routes import router

blockchain = Blockchain()

# Создаем экземпляр шаблонизатора до создания FastAPI приложения
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "explorer" / "templates")

# Регистрируем фильтры сразу
def datetime_filter(timestamp):
    if isinstance(timestamp, (int, float)):
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%d.%m.%Y %H:%M:%S")
    return timestamp

def json_filter(obj, **kwargs):
    return json.dumps(obj, ensure_ascii=False, **kwargs)

templates.env.filters["datetime"] = datetime_filter
templates.env.filters["tojson"] = json_filter

app = FastAPI(
    title="Canfly Amalgam",
    description="API для взаимодействия с Amalgam",
    version="0.11.1"
)

app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent / "explorer" / "static"), name="static")

# Убираем регистрацию фильтров из startup_event
@app.on_event("startup")
async def startup_event():
    pass

# ...остальной код остается без изменений...

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    chain_data = blockchain.get_chain()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "chain": chain_data, "chain_length": len(chain_data)}
    )

@app.get("/block/{block_index}", response_class=HTMLResponse)
async def get_block_page(request: Request, block_index: int):
    chain = blockchain.get_chain()
    if 0 <= block_index < len(chain):
        block = chain[block_index]
        return templates.TemplateResponse(
            "block.html",
            {"request": request, "block": block, "block_index": block_index}
        )
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "message": "Блок не найден"}
    )

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)