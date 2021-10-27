FROM python:3.9-slim

RUN mkdir /Ride_sharing_service
WORKDIR /Ride_sharing_service

ADD requirements.txt /Ride_sharing_service/requirements.txt
RUN pip install -r /Ride_sharing_service/requirements.txt

ADD . /Ride_sharing_service

CMD ["python","-u","/Ride_sharing_service/ride_sharing_service.py"]