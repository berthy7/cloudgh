FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "/app/run_server.py"]