FROM rasa/rasa:1.10.2-full

WORKDIR /app
COPY . /app

# Rasa default port (Render will pass ); EXPOSE is informational.
EXPOSE 5005

# Use  if provided by Render, otherwise default to 5005.
CMD sh -c 'rasa run --enable-api --cors "*" --port '
