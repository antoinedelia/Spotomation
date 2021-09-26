FROM python:3.9

ADD spotomation .
ADD requirements.txt .
ADD env.list .

RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

CMD ["python", "./main.py"]