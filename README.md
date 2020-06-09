# rbp_docker_p1reader
Raspberry Pi compatible Docker image for reading P1 smartmeter datagrams 

# Docker container version
Some hints and tips on working with the p1reader in docker container context. 

## Building the container
docker build - < Dockerfile -t terminalcult/p1reader:latest

## Reading from ttyUSB0
To ensure the p1reader.py script is able to read from /dev/ttyUSB0 you need to ensure you take the devide flag into account. as an example for this you can look at the below:

docker run -i --device=/dev/ttyUSB0 terminalcult/p1reader

## ensuring restart
docker run -d --restart always --device=/dev/ttyUSB0 terminalcult/p1reader
