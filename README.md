## Hyperledger Sawtooth Application - Hyperledger ARTiFACT

Application for storing Proof Of Existence and Proof Of Attributions
---
**NOTE**

This application is based on v1.0.5 of Hyperledger Sawtooth [v1.0.5 documentation](https://sawtooth.hyperledger.org/docs/core/releases/1.0.5/)

---

# 1. Hardware prerequisites

Hyperledger Sawtooth doesn’t provide any minimal system requirements, so hardware listed below will meet minimal system requirements since Hyperledger Sawtooth application has been tested on the same hardware by our team:

  - Intel CPU (any generation of Intel Core i* or appropriate Xeon CPU)
  - at least 4 GB RAM (8GB is recommended)
  - 100+ Gb HDD (separate HDD is recommended)
  - at least 100 Mbps of Internet connection
  - OS installation and setup

Hyperledger team recommends to use Ubuntu 16.04 GNU Linux distribution as an operating system. But since all the infrastructure will be deployed in Docker, you need to install any Linux distro based on 4.x kernel. 
Detailed information how to install Docker and Docker-compose you can find in next URLs:
  - docker: https://docs.docker.com/engine/installation/linux/ubuntulinux
  - docker-compose: https://docs.docker.com/compose/install/
 
Please keep in mind that neither Hyperledger Sawtooth nor Artifacts provides any operating system updates (like linux kernels, binary packages, etc).  

# 2. Sawtooth application installation

The Artifacts Sawtooth application code is stored on the github repository, so it requires git to be installed
```
root@host:~# apt-get -y install git
```
Create project directory:
```
root@host:~# mkdir -p /root/artifacts/ && cd /root/artifacts/
```
Clone repository:
```
root@host:~/artifacts# git clone https://github.com/artifactsofresearch/sawtooth.git
```
Change directory:
```
root@host:~/artifacts# cd sawtooth/
```

# 3. Configure application:

Copy default env variables config:
```
root@host:~/artifacts/sawtooth# cp .env.dist .env
```
Edit environment variables file and change corresponding values of variables
```
root@host:~/artifacts/sawtooth# nano .env
```
The .env file must be like this:
```bash
#usually - external ip of current validator
VALIDATOR_ENDPOINT=tcp://127.0.0.1:8800
#component bind
COMPONENT_IFACE=tcp://eth0:4004
#network bind
NETWORK_IFACE=tcp://eth0:8800
#peers list.  it is connection string to the master node
PEERS=tcp://bcnode.artifacts.ai:8800
```
Set VALIDATOR_ENDPOINT to your external ip instead of 127.0.0.1
  - _NOTE: Keep in mind that in case of NAT connection ports 4004 and 8800 must be forwarded to the target machine_

Build containers:
```
root@host:~/artifacts/sawtooth# docker-compose build --no-cache
```
You should not see any errors during building process

# 4. Sawtooth application launch

  - Start and run all Artifacts Sawtooth application stack
```
root@host:~/artifacts/sawtooth# docker-compose up -d
```
  - See list of runned containers (all containers must be in Up state as in the example below):
```
root@host:~/artifacts/sawtooth# docker-compose ps
```
```
       Name             Command                         State           Ports                     
--------------------------------------------------------------------------------------------------------------------
artifact-shell           bash -c                         Up      4004/tcp, 8008/tcp                            
                           if [ ! -f /root ...
artifact-tp              bash -c                         Up                                                    
                           sleep 1                                                                              
                                  artif ...                                                                            
identity-tp             identity-tp -vv -C tcp://v ...   Up      4004/tcp                                      
sawtooth-poet-vali...   poet-validator-registry-tp ...   Up      4004/tcp                                      
sawtooth-rest-api       sawtooth-rest-api -vv -C t ...   Up      4004/tcp, 0.0.0.0:8008->8008/tcp              
sawtooth-settings-tp    settings-tp -vv -C tcp://v ...   Up      4004/tcp                                      
sawtooth-validator      bash -c                          Up      0.0.0.0:4004->4004/tcp, 0.0.0.0:8800->8800/tcp
                          if [ -z $(ls -A ...                                                                  
```


  - See validator’s logs in real time:
```
root@host:~/artifacts/sawtooth# docker-compose logs validator -f
```
  - See full stack logs in real time:
```
root@host:~/artifacts/sawtooth# docker-compose logs -f
```

The network policies bases on validator keys. In order to get node connected to the network, you need to send validator’s PUBLIC key to the ARTiFACTS Support Team:

  - To get your validator’s public key run next command and copy the output (example key see below):
```
root@host:~/artifacts/sawtooth# docker-compose exec validator cat /etc/sawtooth/keys/validator.pub
```
```
038e883d98d698a********************f825629cc691bc7483994231f544bde
```

As soon as Your node will be whitelisted on the network, it can get access to the blockchain.

In case of successful join to the network you shall see in logs something like this:
```
sawtooth-validator            | [2018-10-05 14:34:39.267 DEBUG    gossip] Connection to aa2c914b37624067ea3001e2f4802bb6d2d6500d649b660319917e7fb5ea981be98e4328743a1926af834ddfa13765d3b3a535d78ca53e13fd903d434953b075 succeeded
sawtooth-validator            | [2018-10-05 14:34:39.267 DEBUG    handlers] Connection: aa2c914b37624067ea3001e2f4802bb6d2d6500d649b660319917e7fb5ea981be98e4328743a1926af834ddfa13765d3b3a535d78ca53e13fd903d434953b075 is approved
sawtooth-validator            | [2018-10-05 14:34:39.271 DEBUG    gossip] Peering request to aa2c914b37624067ea3001e2f4802bb6d2d6500d649b660319917e7fb5ea981be98e4328743a1926af834ddfa13765d3b3a535d78ca53e13fd903d434953b075 was successful
sawtooth-validator            | [2018-10-05 14:34:39.271 DEBUG    gossip] Added connection_id aa2c914b37624067ea3001e2f4802bb6d2d6500d649b660319917e7fb5ea981be98e4328743a1926af834ddfa13765d3b3a535d78ca53e13fd903d434953b075 with endpoint tcp://bcnode.artifacts.ai:8800, connected identities are now {'aa2c914b37624067ea3001e2f4802bb6d2d6500d649b660319917e7fb5ea981be98e4328743a1926af834ddfa13765d3b3a535d78ca53e13fd903d434953b075': 'tcp://bcnode.artifacts.ai:8800'}
```

  - Also you can check network batches by connecting to the REST-API using this URL:
```
http://your_node_ip_address:8008/batches
```
You will see JSON formatted info about batches, transactions etc.

### Useful commands:

Stop ARTiFACTS Sawtooth stack:
```
root@host:~/SAWTOOTH/REPO/sawtooth# docker-compose stop
```
Start ARTiFACTS Sawtooth stack:
```
root@host:~/SAWTOOTH/REPO/sawtooth# docker-compose start
```
Remove containers:
```
root@host:~/SAWTOOTH/REPO/sawtooth# docker-compose down
```

## Troubleshooting

  - docker-compose build --no-cache command fails
  
  The most common reason is either docker daemon is not running or something wrong with docker images in the Hyperledger repo. In case of docker daemon you can use systemctl status docker.service to start it. In case of images You should wait for Hyperledger’s fixes
  - docker-compose up -d command fails
  
  There can be a lot of reasons. As a rule, the program will throw a message what causes an error. Common fix can be pulling the new code from git repo, building and running it again
  -  If you see in logs something like this:
```
sawtooth-validator            | [2018-10-05 14:25:18.686 DEBUG    interconnect] Unable to complete Trust Authorization.
```
  it means that Your validator’s key has not been added, so access to the node is restricted.
  - For any other issues feel free to create an issue here: https://github.com/artifactsofresearch/sawtooth/issues 
