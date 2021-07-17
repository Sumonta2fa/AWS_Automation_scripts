#!/usr/bin/env python
from boto3.session import Session
import sys
##### Description ######
# This code is collecting IP check information from given zone all security groups
#aws_security_group_ip_check.py  106.203.141.144
# It shows mached ip ruls eg:
#Found ip
#9000 9000 tcp 106.203.141.144/32 security-group sg-2242
#Manually need to provide the IP and select the searching zone.
##### Sumonta #########

st = ''''''
buf = []
def genSession(region_name=None):
    session = Session(
        aws_access_key_id='xxx',
        aws_secret_access_key='xx',
        region_name=region_name,
    )
    return session
def  ip_check(region_name, IP ):
    session = genSession(region_name)
    client = session.client('ec2')
    response = client.describe_security_groups(
        Filters=[{'Name': 'ip-permission.cidr', 'Values': [IP]}])
#    print response['SecurityGroups']
    for list in response['SecurityGroups']:
        GroupName = list['GroupName']
        GroupId = list['GroupId']
        for data in list['IpPermissions']:
 #           print data
            try:
                FromPort = data['FromPort']
                ToPort = data['ToPort']
                IpProtocol = data['IpProtocol']
                IpRanges = data['IpRanges']
                for ip in IpRanges:
                    #  print ip['CidrIp']

                    if IP == ip['CidrIp']:
#                        print FromPort, ToPort, IpProtocol, IP, GroupName, GroupId
			ll = region_name, FromPort, ToPort, IpProtocol, IP, GroupName, GroupId
                        buf.append(ll)
            except KeyError, e:
                print e, data 
    return buf

def get_regioins(IP):
    session = genSession()
    client = session.client('ec2')
    response = client.describe_regions()
    for list in response["Regions"]:
        print "IP checking in region "+list["RegionName"]
        buf = ip_check(list["RegionName"], IP)
	st = ''''''
    for list in buf:
        st = st + str(list) + '\n'
    return st

if __name__ == '__main__':
    
    IP = sys.argv[1]+'/32'
#    IP = sys.argv[1]
    string = get_regioins(IP)
    print 'Found IPs:', '\n', string


