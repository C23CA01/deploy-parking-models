# py3.9/3.10
FROM python:3.9

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /parking-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

# FROM python:3.9-slim-buster

# # Install dependencies for MySQL
# RUN apt-get update && \
#     apt-get install -y libmariadb-dev-compat libmariadb-dev && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /parking-app

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# ENV FLASK_APP=app.py
# ENV HOST 0.0.0.0

# EXPOSE 5000

# CMD ["flask", "run", "--host", "0.0.0.0"]
