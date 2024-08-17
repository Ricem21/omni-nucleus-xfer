FROM ubuntu:22.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        wget \
	vim \
	net-tools \
        build-essential \
        xdg-utils \
    && apt-get -y autoremove \
    && apt-get clean autoclean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb --no-check-certificate
RUN apt update
RUN apt install ./google-chrome-stable_current_amd64.deb -y
RUN rm google-chrome-stable_current_amd64.deb


#RUN apt-get install -y python-dev python-pip libffi-dev libssl-dev
#ADD requirements.txt requirements.txt
#RUN pip install -r requirements.txt

COPY ./omni-client /opt/omni-client
COPY ./omni-other /opt/omni-other

WORKDIR /opt/omni-client
RUN tar -xvf connect-samples-205.0.0.tar.gz
WORKDIR /opt/omni-client/connect-samples-205.0.0
RUN ./build.sh

#ENV SCRIPT_DIR=/opt/omni-client/connect-samples-205.0.0
#ENV USD_LIB_DIR=${SCRIPT_DIR}/_build/linux-x86_64/release
#ENV LD_LIBRARY_PATH=${USD_LIB_DIR}
#ENV PYTHONPATH=/app:${USD_LIB_DIR}/python:${USD_LIB_DIR}/bindings-python

#RUN apt update
#RUN apt-get install xdg-utils -y

#COPY ./data /tmp
COPY ./app /app

ENTRYPOINT ["/app/startup.sh"]
