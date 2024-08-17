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

# May need later, so keep in Docker file
#
#ADD requirements.txt requirements.txt
#RUN pip install -r requirements.txt

COPY ./omni-client /opt/omni-client

#
#  Add the compressed release of the Omniverse connect SDK sample
#  Then uncompress, and build the SDK
WORKDIR /opt/omni-client
RUN tar -xvf connect-samples-205.0.0.tar.gz
WORKDIR /opt/omni-client/connect-samples-205.0.0
RUN ./build.sh


COPY ./app /app

ENTRYPOINT ["/app/startup.sh"]
