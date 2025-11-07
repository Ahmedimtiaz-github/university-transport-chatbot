FROM rasa/rasa:1.10.2-full

WORKDIR /app

# copy only requirements first for layer caching
COPY requirements.txt /app/requirements.txt

# install other python deps but don't re-install rasa itself
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt --ignore-installed rasa

# copy the rest of the project
COPY . /app

# expose the HTTP port that Render expects
EXPOSE 8080

# default CMD; Render override (Docker Command) will still work if you set it
CMD ["sh","-c","rasa run --enable-api --cors \"*\" --port $PORT"]
