FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install Docker CLI
RUN apt-get update && apt-get install -y docker.io

COPY . .
