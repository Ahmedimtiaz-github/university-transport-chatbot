# Use the official Rasa 1.10.2 image (includes compatible aiohttp/yarl/etc)
FROM rasa/rasa:1.10.2-full

WORKDIR /app

# copy only requirements first (cache friendly)
COPY requirements.txt /app/requirements.txt

# Install only the extras — do NOT reinstall rasa
RUN pip install --no-cache-dir -r /app/requirements.txt --ignore-installed rasa

# copy the rest of your application
COPY . /app

# Expose the port Render will use (Render provides $PORT at runtime)
ENV PORT=10000

# Start Rasa server (bind to $PORT). We set default PORT for local testing.
CMD ["sh", "-c", "rasa run --enable-api --cors \"*\" --port ${PORT}"]
