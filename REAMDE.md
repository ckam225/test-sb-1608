### Test apps

- React
- FastAPI
- Telegram Bot

### create python virtual environment

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Set telegram bot token in settings

open file `api/core/settings.py`

```python
...

TELEGRAM_BOT_TOKEN=your_bot_token

...

```

### Run api

```bash
cd api && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Go to http://localhost:8000/docs

### Run telegram bot

```bash
cd api && python bot.py
```

### Run admin web app

```bash
cd admin &&  yarn && yarn dev
```

Go to http://localhost:3000
