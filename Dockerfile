FROM rasa/rasa:3.6.21-full
WORKDIR /app
COPY . /app
ENV PORT=5005

# override base image entrypoint so shell can expand $PORT and run the command
ENTRYPOINT ["/bin/sh","-c"]

# Ensure port is exposed (helpful for Render)
EXPOSE 10000

# Start Rasa and bind to $PORT (Render provides $PORT). Fallback to 10000 locally.
CMD ["sh", "-c", "rasa run --enable-api --cors '*' --port ${PORT:-10000}"]
