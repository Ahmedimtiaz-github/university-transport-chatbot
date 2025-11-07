FROM rasa/rasa:1.10.2-full

WORKDIR /app

# copy requirements early for layer caching
COPY requirements.txt /app/requirements.txt

# become root to safely upgrade pip and install additional dependencies
USER root

RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt --ignore-installed rasa

# switch back to non-root user (Rasa images use uid 1001)
USER 1001

# copy the rest of the project
COPY . /app

EXPOSE 8080

CMD ["sh","-c","rasa run --enable-api --cors \"*\" --port $PORT"]
