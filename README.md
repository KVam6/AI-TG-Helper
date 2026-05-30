# 🤖 Telegram AI Assistant Bot

Telegram-бот с AI-ответами на базе OpenRouter/OpenAI-compatible API.

Поддерживает:

* ⚡ **Быстрый режим** — короткие ответы без лишнего текста
* 🧠 **Подробный режим** — развёрнутые объяснения
* 💬 **Контекст диалога** отдельно для каждого пользователя
* 🎛️ Переключение режимов через Telegram-кнопки
* 🌍 Стабильное подключение к Telegram API через **Cloudflare Worker**
* 🔧 Возможность использовать встроенный Worker или подключить свой

---

## ✨ Возможности

### ⚡ Быстрый режим

Короткие ответы без лишней воды.

Подходит для:

* быстрых вопросов
* фактов
* коротких уточнений

---

### 🧠 Подробный режим

Развёрнутые ответы с пояснениями.

Подходит для:

* обучения
* разбора тем
* сложных вопросов

---

### 💬 Контекст диалога

Для каждого пользователя сохраняется отдельная история сообщений.

Бот умеет:

* помнить предыдущие вопросы
* учитывать контекст
* продолжать диалог
* хранить выбранный режим

---

### 🎛️ Удобный интерфейс

Telegram-кнопки:

* ⚡ Быстрый ответ
* 🧠 Подробное объяснение

Во время генерации ответа бот показывает статус **«печатает…»**.

---

## 🌍 Подключение к Telegram API (Cloudflare Worker)

По умолчанию бот уже использует встроенный Cloudflare Worker.

Это помогает стабильно подключаться к Telegram API, особенно если прямое соединение работает нестабильно.

В коде используется резервный Worker.

Если нужно — его легко заменить на свой через `.env`.

---

### Использовать как есть

Ничего дополнительно настраивать не нужно.

Просто создайте `.env` по примеру ниже.

---

### Использовать свой Worker

Если хотите подключить собственный Cloudflare Worker:

раскомментируйте строку `WORKER_URL` и вставьте свой адрес.

Пример:

```env id="v3e8qw"
BOT_TOKEN = 'COPY_TOKEN_FROM_BOTFATHER_HERE'
OPENROUTER_KEY = 'COPY_TOKEN_FROM_OPENROUTER_HERE'
WORKER_URL = 'https://my-own-worker.workers.dev'
```

Если строка закомментирована — бот использует встроенный Worker.

---

### Зачем это нужно

Cloudflare Worker помогает:

✅ стабилизировать подключение к Telegram API
✅ уменьшить ошибки соединения
✅ запускать бота без VPN
✅ быстро переключиться на свой endpoint

---

## 🛠️ Стек

* Python 3.11+
* aiogram 3
* asyncio
* OpenRouter API
* OpenAI API
* Cloudflare Workers
* python-dotenv

---

## 🚀 Установка

### 1. Клонировать репозиторий

```bash id="f8r1uq"
git clone https://github.com/KVam6/AI-TG-Helper.git
cd telegram-ai-bot
```

---

### 2. Установить зависимости

```bash id="q2m9pd"
pip install -r requirements.txt
```

---

### 3. Создать `.env`

Скопируйте `.env.example`

```bash id="x7k4tn"
cp .env.example .env
```

или создайте вручную:

```env id="n4c7ws"
BOT_TOKEN = 'COPY_TOKEN_FROM_BOTFATHER_HERE'
OPENROUTER_KEY = 'COPY_TOKEN_FROM_OPENROUTER_HERE'
#WORKER_URL = 'PASTE_YOUR_CLOUDFLARE_URL_HERE_IF_YOU_WISH' # Find more info in config.py

#Don't forget to change the extension to .env
```

---

### 4. Запустить

```bash id="u5y8re"
python run.py
```

---

### Можно запустить через докер

```bash
docker build -t telegram-ai-bot .
docker run --env-file .env telegram-ai-bot
```

---

## ⚙️ Настройка режимов

Файл `config.py`

```python id="a8h2wy"
PROMPTS = {
    "FastMode": "Отвечай кратко и по делу...",
    "DetailedMode": "Отвечай подробно и понятно...",
}
```

Легко можно поменять системные промпты.

---

## 🧠 История сообщений

Пример структуры:

```python id="k6z4mv"
user_history = {
    user_id: [
        {"role": "user", "content": "Что мы используем для обходов блокировок?"},
        {"role": "assistant", "content": "Привет! Мы используем zapret-dis.."}
    ]
}
```

История отдельная для каждого пользователя.

---

## 📌 Планы

* [ ] Очистка истории
* [ ] Хранение в базе данных
* [ ] Голосовые сообщения
* [ ] Генерация изображений
* [ ] Новые режимы

---

## 📄 License

MIT

---

## ⭐ Поддержка

Если проект оказался полезным —

**поставьте звезду на GitHub ⭐**
