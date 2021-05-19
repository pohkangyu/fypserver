# syntax=docker/dockerfile:1

FROM python:3.7

RUN set -e; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        software-properties-common \
    ; \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9; \
    apt-add-repository 'deb http://repos.azulsystems.com/debian stable main'; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        zulu-11 \
    ; \
    apt-get clean; \
    rm -rf /var/tmp/* /tmp/* /var/lib/apt/lists/*

WORKDIR /app
RUN pip3 install git+https://github.com/pwollstadt/IDTxl.git
RUN pip3 install flask==2.0.0
RUN pip3 install pandas==1.1.4
RUN pip3 install statsmodels==0.12.2
RUN pip3 install h5py==3.2.1
RUN pip3 install networkx==2.5.1
RUN pip3 install matplotlib==3.4.2
RUN pip3 install JPype1==1.2.1

EXPOSE 5000

WORKDIR /fypserver
ADD . /fypserver
CMD ["python", "server.py"]

#docker system prune -a
#docker build --tag python-docker .
#docker run -p 5000:5000 python-docker:latest
