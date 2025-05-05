FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY load.py ./load.py
RUN python3 ./load.py

COPY . .

ENTRYPOINT ["python", "main.py"]