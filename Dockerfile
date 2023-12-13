FROM python:3.9-slim-buster

# Install dependencies for MySQL
RUN apt-get update && \
    apt-get install -y libmariadb-dev-compat libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /parking-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV HOST 0.0.0.0

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
