FROM python:3.9-slim

RUN mkdir /Communication_service
WORKDIR /Communication_service

ADD requirements.txt /Communication_service/requirements.txt
RUN pip install -r /Communication_service/requirements.txt

ADD . /Communication_service

#EXPOSE 8003

CMD ["python","-u","/Communication_service/communication_service.py"]