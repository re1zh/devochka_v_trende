# Discord-бот для проигрывания аудиофайлов по нажатию клавиши

Этот проект был придуман одним декабрьским вечером двумя друзьями, которые любят игру `Dota 2`.

## Установка

1. Скачайте или клонируйте проект:
```bash
git clone https://github.com/re1zh/devochka_v_trende.git
```

2. Настройте бота:
    - Скачайте `ffmpeg` с [официального сайта](https://ffmpeg.org/download.html#build-windows).
    - Откройте `config.json`
    - Вставьте ваш Discord-токен и URL вебхука:
    ```json
    {
      "DISCORD_TOKEN": "your_discord_token",
      "WEBHOOK_URL": "your_webhook_url"
    }
    ```
   - Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
   
3. Запустите бота:
```bash
python script.py
```

## Требования

- Python 3.8+
- Discord-бот, зарегистрированный в [Discord Developer Portal](https://discord.com/developers/applications).

## Использование

- `!join` - подключение бота к голосовому каналу.
- `!play **audiofile**` - проигрывание аудиофайла в формате `mp3` из директории `sounds`.
- `!leave` - отключение бота от голосового канала.

## Источники

https://www.youtube.com/watch?v=uwNp2lE_2uk