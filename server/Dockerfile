FROM python:3.9-slim

WORKDIR /app

COPY server.py /app/server.py
COPY scenes.json /app/scenes.json

EXPOSE 5000

CMD ["python", "server.py"]
