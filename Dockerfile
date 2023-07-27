FROM ubuntu:latest
RUN apt-get update &&  apt-get install python3 -y
RUN mkdir app
COPY ../requirements.txt app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT uvicorn app:app --reload
