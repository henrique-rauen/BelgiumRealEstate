FROM ubuntu:latest
RUN apt-get update &&  apt-get install python3 pip -y
RUN mkdir app
COPY docker_requirements.txt app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
#RUN uvicorn app:app --reload
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "PORT", "--reload"]
