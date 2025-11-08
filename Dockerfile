FROM rasa/rasa:1.10.2-full
WORKDIR /app
COPY . /app
ENV PORT=5005

# override base image entrypoint so shell can expand $PORT and run the command
ENTRYPOINT ["/bin/sh","-c"]

# run rasa using the PORT env var Render provides
CMD ["rasa run --enable-api --cors \"*\" --port $PORT"]
