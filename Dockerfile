# Use Python 3.8 (stable for Rasa)
FROM python:3.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system build deps often required by Rasa and DB clients
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python deps
COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install -r /app/requirements.txt

# Copy project
COPY . /app

# Expose the default Rasa port
EXPOSE 5005

# Default command to run Rasa server (Render will use the image's CMD)
CMD ["rasa","run","--enable-api","--port","5005","--cors","*"]
