FROM python:latest
ADD . /code
WORKDIR /code
ADD Eau_Potable_Barnier.csv code/
RUN pip install -r requirements.txt
CMD ["python", "MQTTPublisher.py"]