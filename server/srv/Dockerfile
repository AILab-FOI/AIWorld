FROM python:3
RUN apt-get -y update
RUN pip uninstall -y python-socketio python-engineio
ADD requirements.txt ./
RUN python3 -m pip install -r requirements.txt
