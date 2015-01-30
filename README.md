# cosmodrome  ``beta``
YAML backed metadata API to retrieve data for multiple infrastructure, build and runtime environments. 

*Abstracting Data from Stacks*
----------------------------
This project makes it easier to get non-secret environmental data for scripts, builds and deployments.  Making scripting easier removing logic for environmental awareness based on first two octets of an IP address.

**Sweet Benefits:**

- Agentless
- Registerless
- Reduce source lines of code
- Common and environmental data separated by one API
- Easier to build facts for your Configuration Management tools
- Easier to manage multiple environments in different Cloud Providers/VPCs

**This Is for You If You:**

- Have tons of infrastructure everywhere
- Constantly build new environments or proof-of-concepts
- Want one script to build all images for Cloud, Kickstart or Containers
- Think it would be nice to bring multiple dev/ops teams together with data
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
    

**Curl Examples:**

    bash$ curl https://cosmodrome/metadata/env
     'app_s3': 's3://s3.amazonaws.com/marshyskicom_dev/deploy.sh',
     'app_dev_branch': 'development',
     'app_git': 'https://github.com/marshyski/marshyski.com.git',
     'puppet': '192.168.1.15',
     'dns': '192.168.1.1'

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

    bash$ curl https://cosmodrome/metadata/build_img
    marshyski/centos

    bash$ curl https://cosmodrome/metadata/dns
    192.168.1.1
