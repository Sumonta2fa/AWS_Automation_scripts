#!/usr/bin/env python
import os, sys
import ast
import logging
import socket

#---------Important Notes--------------
# ec2 user data should have installed the awscli and set authentication or role.
# ec2 instance should have the Name tag 

# ---------instance user-data---------
'''
#!/bin/bash
sudo apt-get install awscli -y
#Download Script from bucket
aws s3 cp s3://xxx/aws_scripts/aws_hostname_setup.py /root/
chmod +x /root/aws_hostname_setup.py

#Add Crontab
line="@reboot python /root/aws_hostname_setup.py" 
(crontab -l; echo "$line") | crontab -

#Executing First time
python /root/aws_hostname_setup.py 

'''

# create a logging format
logging.basicConfig(filename='/var/log/aws_hostname_setup.log',
                    level=logging.INFO,
                    #                    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                    format='[%(asctime)s] {%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S'
                    )


logger = logging.getLogger(__name__)
logger.info("----------------------------------------------------------------")
#Aws ec2 instance tag setup
cmd = "curl --silent http://169.254.169.254/latest/meta-data/instance-id"
id = os.popen(cmd)

cmd = 'curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone  | sed -e "s/.$//"'
az = os.popen(cmd)

cmd = 'aws ec2 describe-tags --region %s --filter "Name=resource-id,Values=%s"' %(az.read(),id.read())
logger.info("Executing command: {}".format(cmd))
name = os.popen(cmd)

name = ast.literal_eval(name.read())

if name['Tags'][0]['Key'] == "Name":
	hname = name['Tags'][0]['Value']
	logger.info("Hostname: {}".format(hname))
else:
	logger.error("No hostname: {}".format(hname))


#Executing hostname update
hostn = socket.gethostname()

if hostn != hname:
    logger.info("Fetching current Hostname: {}".format(hostn))

    # change hostname in /etc/hosts & /etc/hostname
    cmd = 'sudo sed -i "s/%s/%s/g" /etc/hostname' % (hostn, hname)
    logger.info("Executing command: {}".format(cmd))
    os.system(cmd)

    #checking for existing data in hosts file
    cmd = 'grep %s /etc/hosts' %(hname)
    p = os.popen(cmd)
    if_match = p.read()
    logger.info("checking for existing data in hosts file: {}".format(cmd))
    if not if_match:
        cmd = 'sed -i "s/127.0.0.1[[:space:]].\+localhost.\+/&\\n127.0.0.1\\t%s/g" /etc/hosts' % (hname)
        logger.info("Executing command: {}".format(cmd))
        os.system(cmd)
    else:
        logger.info("Already found hostname in hosts file: {}".format(hname))
    
    # Setup hostname Manually
    cmd = "hostname " + hname
    logger.info("Executing command: {}".format(cmd))
    os.system(cmd)
    newname = socket.gethostname()
    logger.info("Hostname Update: {} ".format(newname))

else:
    logger.info("Hostname Match: {} ".format(hostn))

