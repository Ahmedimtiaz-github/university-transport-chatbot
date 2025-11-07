FROM rasa/rasa:1.10.2-full

# Temporarily switch to root so we can upgrade pip and install requirements
USER root

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt --ignore-installed rasa

# Switch back to non-root user used by the base image (common for rasa images).
# If this causes "unknown user" during build, remove this USER line.
USER 1001


# copy the rest of the project
COPY . /app

EXPOSE 8080

CMD ["sh","-c","rasa run --enable-api --cors \"*\" --port $PORT"]
