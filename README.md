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

# Debug information
Some information for when you try to debug things

## manual read MQTT
For reading MQTT manually you can use the below mosquitto (mosquitto_sub) command. This will read all information published under smartmeter (and deeper)

mosquitto_sub -h 10.10.1.242 -p 1883 -d -t smartmeter/#

Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/consumption/total/tarrif1', ... (4 bytes))
3741
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/consumption/total/tarrif2', ... (4 bytes))
4535
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/consumption/total/total', ... (4 bytes))
8276
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/production/total/tarrif1', ... (3 bytes))
219
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/production/total/tarrif2', ... (3 bytes))
495
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/consumption/total/total', ... (4 bytes))
8276
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/consumption/current/tarrif1', ... (1 bytes))
0
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/consumption/current/tarrif2', ... (2 bytes))
57
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/production/current/tarrif1', ... (1 bytes))
0
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/production/current/tarrif2', ... (1 bytes))
0
Client mosqsub|7970-rbp0.inter received PUBLISH (d0, q0, r0, m0, 'smartmeter/energy/flow/current', ... (2 bytes))
57
