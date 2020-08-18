FROM        ubuntu:20.10
MAINTAINER  "rodobre"

RUN         apt-get update && apt-get install -y build-essential gnupg python3 python3-setuptools python3-pip
COPY        ./requirements.txt /app/requirements.txt
WORKDIR     /app

RUN         python3 -m pip install -r requirements.txt
COPY        [^docker]* /app/

ENV         LC_ALL C.UTF-8
ENV         LANG C.UTF-8

EXPOSE      80
ENTRYPOINT  ["python3"]
CMD         ["app.py"]