FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y ffmpeg libpq-dev gcc

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "init_db.py", "&&", "python", "script.py"]