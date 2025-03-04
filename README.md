# Amalgam: Blockchain Explorer & API 🚀

Amalgam - это блокчейн-платформа с веб-интерфейсом для просмотра и взаимодействия с блоками через REST API. Проект реализован на FastAPI и обеспечивает простой доступ к данным блокчейна.

## Основные особенности 🌟

- FastAPI REST API для взаимодействия с блокчейном
- Blockchain Explorer с веб-интерфейсом
- Поддержка JSON транзакций
- Proof of Work консенсус
- Валидация цепочки блоков

## Технологический стек 🛠

- Python 3.12
- FastAPI
- Jinja2 Templates
- Bootstrap 5

## API Endpoints 📡

- `GET /` - Blockchain Explorer интерфейс
- `GET /api/chain` - Получить всю цепочку блоков  
- `GET /api/block/{index}` - Получить блок по индексу
- `POST /api/transactions/new` - Создать новую транзакцию
- `POST /api/mine` - Добыть новый блок
- `GET /api/validate` - Проверить валидность цепочки

## Установка и запуск 🚀

```bash
# Клонировать репозиторий
git clone https://github.com/Canfly/Amalgam.git

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
python -m api.main