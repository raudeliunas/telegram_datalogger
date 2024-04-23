FROM python:3.9-alpine

# Instalar o Bash
RUN apk update && apk add bash

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
