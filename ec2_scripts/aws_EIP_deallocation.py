import boto3
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
#
# 3 file need to change. region, instance, text file to elastic ip current associate address eipassoc-57f30a76
#

def genSession(region_name=None):
    client = boto3.client('ec2')
    return client
    wpath = '/home/sumonta/aws_vpn_ip_replace_AllocationId.txt'

def release_address(client, wpath):
    try:
        print "Read ExistingPublicIp AllocationId from : " + wpath
        w = open(wpath, "r")
        oldAllocationId = w.read()
        w.close()
        oldAllocationId = oldAllocationId.strip('\n')
        response_release_address = client.release_address(
            AllocationId=oldAllocationId,
            )
        print response_release_address
    except Exception as e:
        print "release_address function error"
        pass



if __name__ == '__main__':
    region_name = 'ap-south-1'
   # InstanceId = 'i-0c82b030b4cf41cbb'

    client = genSession(region_name)
    release_address(client, wpath)


    """
    print "Write current AllocationId to : " + wpath

    w = open(wpath, "w")
    w.write(AllocationId)
    w.close()

    """