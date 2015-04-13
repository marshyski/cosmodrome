# cosmodrome  ``beta``
YAML backed metadata/tag API to retrieve data for multiple infrastructure, servers, build and runtime environments.


*Abstracting Data from Stacks*
----------------------------
This project makes it easier to get non-secret environmental/common metadata, or host tags for scripts, builds and deployments.  Making scripting easier removing logic for environmental awareness based on first two/three IP octets, hostname and closest match of a hostname.

Example lookup:

    IP: 192.168.1.20
    Hostname: aws-lx-web-team-001

    Logically will look for key/value data in this order:

    aws-lx-web-team-001.yaml
    192.168.1.yaml
    192.168.yaml
    common.yaml
    aws-lx-web-team.yaml


**Sweet Benefits:**

- Agentless
- Registerless
- Reduce source lines of code
- Common, environmental and host data separated by one API
- Desiring a cloud-like tagging method for servers
- Easier to build facts for your Configuration Management tools
- Easier to manage multiple environments in different datacenters, Cloud Providers/VPCs

**This Is for You If You:**

- Have tons of infrastructure everywhere
- Constantly build new environments or proof-of-concepts
- Want one script to build all images for Cloud, Kickstart or Containers
- Want a way to tag baremetal or any server for that matter
- Want to use multiple Configurations Management tools by centralizing data in one place

**YAML Examples:**

*data/192.168.yaml*  **DEV** or **Cloud A**

    puppet: 192.168.1.15
    dns: 192.168.1.1
    app_git: https://github.com/marshyski/marshyski.com.git
    app_dev_branch: development
    app_s3: s3://s3.amazonaws.com/marshyskicom_dev/deploy.sh
    
*data/10.142.yaml*  **QA** or **Cloud B**

    puppet: 10.142.1.15
    dns: 10.142.1.1
    app_git: https://github.com/marshyski/marshyski.com.git
    app_dev_branch: qa
    app_s3: s3://s3.amazonaws.com/marshyskicom_qa/deploy.sh
    
*data/10.142.5.yaml*  **QA subnet** or **Isolated environment within QA**

*data/common.yaml*  **Common Everywhere**

    amieast: ami-cffr455
    amiwest: ami-u77d3rt
    softlayer_os: REDHAT_LATEST_65
    softlayer_dc: wdc01
    support: marshyski@gmail.com
    maven_ver: 3.2.5
    python_ver: 2.7.8
    docker_gold: centos7.0.1406
    docker_build: marshyski/centos
    docker_test: marshyski/test
    current_rel: 1.0.0
    next_rel: 1.0.1
    
*data/aws-lx-web-team.yaml* **for host grouping or one host** *data/aws-lx-web-team-001.yaml*

    purpose: web
    role: nginx
    profile: basic_server
    app_name: team

**Curl Examples:**

    #from DEV server
    bash$ curl https://cosmodrome/metadata/env
     'app_s3': 's3://s3.amazonaws.com/marshyskicom_dev/deploy.sh',
     'app_dev_branch': 'development',
     'app_git': 'https://github.com/marshyski/marshyski.com.git',
     'puppet': '192.168.1.15',
     'dns': '192.168.1.1'
    
    #from any server
    bash$ curl https://cosmodrome/metadata/common
     'python_ver': '2.7.8',
     'softlayer_os': 'REDHAT_LATEST_65',
     'amieast': 'ami-cffr455',
     'docker_test': 'marshyski/test',
     'support': 'marshyski@gmail.com',
     'maven_ver': '3.2.5',
     'amiwest': 'ami-u77d3rt',
     'next_rel': '1.0.1',
     'current_rel': '1.0.0',
     'softlayer_dc': 'wdc01',
     'docker_build': 'marshyski/centos',
     'docker_gold': 'centos7.0.1406'

    #from any server
    bash$ curl https://cosmodrome/metadata/docker_build
    marshyski/centos

    #from DEV server
    bash$ curl https://cosmodrome/metadata/dns
    192.168.1.1

    #from QA server
    bash$ curl https://cosmodrome/metadata/dns
    10.142.1.1
    
    
**Bash Script Example:**

    #from client server
    #!/bin/bash
    # GET values by hostname
    HOSTNAME=`hostname`
    PURPOSE=`curl -sf https://cosmodrome/metadata/$HOSTNAME/role`
    APPNAME=`curl -sf https://cosmodrome/metadata/$HOSTNAME/appname`
    # GET S3 target from common.yaml
    S3=`curl -sf https://cosmodrome/metadata/app_s3`

    yum install -y $ROLE
    curl -O $S3 | tar -zxvf
    mv -rf $APPNAME* /opt/
    service $PURPOSE restart

**Setup:**

*Generating a SSL cert is optional, but recommended as your data is important.*

Generate a self-signed SSL cert and key (dev/test purposes only):

    openssl req -subj '/CN=cosmodrome.com/O=cosmodrome/C=US' -new -newkey rsa:2048 -days 365 -nodes -sha256 -keyout cosmodrome.key -out cosmodrome.cert

config.yaml:

 - port (define port you want cosmodrome to run as) 
 - cert (define your SSL cert file location) 
 - key (define your SSL key file location)

Defaults:

 - API rate limit is set globally for all endpoints for requests from remote addresses 2880 per day, 120 per hour

**Generate your environment YAML files in the data directory.**
