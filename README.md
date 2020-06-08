# rbp_docker_p1reader
Raspberry Pi compatible Docker image for reading P1 smartmeter datagrams 


# Reading from ttyUSB0
To ensure the p1reader.py script is able to read from /dev/ttyUSB0 you need to ensure you take the devide flag into account. as an example for this you can look at the below:
docker run -i --device=/dev/ttyUSB0 0a3777e609da
