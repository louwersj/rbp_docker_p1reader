# Pull base image
FROM resin/rpi-raspbian:wheezy

# Install dependencies & pull p1reader script
RUN echo && \
    echo "deb http://raspbian.raspberrypi.org/raspbian stretch main contrib non-free rpi" > etc/apt/sources.list && \
    apt-get update && \
    apt-get install python && \
    apt-get install python-pip && \
    pip install setuptools && \
    pip install pyserial && \
    pip install paho-mqtt && \
    curl https://raw.githubusercontent.com/louwersj/rbp_docker_p1reader/master/app/p1reader.py --output /tmp/p1reader.py && \
    rm -rf /var/lib/apt/lists/*


# Define working directory
WORKDIR /data

# Define default command
CMD ["python", "/tmp/p1reader.py"]
