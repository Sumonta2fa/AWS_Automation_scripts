import boto3
import os
import sys

##### Description ######
# This code is using aws-cli and bot03 sdk.
# It is used for replaceing single ip from bunch of security groups of a region.
# Need to configure the aws setting for aws cli and boto3 and make sure aws cli
# should change the REGION each time accordingly for search
# input old ip and new ip
# aws configure(set all)
# set AWS_ACCESS_KEY_ID=xxAKIAIOSFODNN7EXAMPLE
# set AWS_SECRET_ACCESS_KEY=xx
# set AWS_DEFAULT_REGION=us-west-2
#Error 'The security group 'sg-6c36a408' does not exist' Region set problem in cli
###### Sumonta #########
#
#command:
#python aws_security_group_ip_replace.py %s/32 %s/32 %s
#region='us-east-1'
#region='us-west-2'
#region='ap-southeast-1'

def func(region):
    client = boto3.client('ec2',
            aws_access_key_id='xxx',
            aws_secret_access_key='xxx/R4NFQ1d',
            region_name=region)

    IP =sys.argv[1]
    NEWIP = sys.argv[2]
    response = client.describe_security_groups(
        Filters=[{'Name': 'ip-permission.cidr', 'Values': [IP]}])
    f = open('newfile1.txt', 'w')
    #print response['SecurityGroups']
    for list in response['SecurityGroups']:
        GroupName = list['GroupName']
        GroupId = list['GroupId']
        for data in list['IpPermissions']:
            #print data
            try:
                FromPort = data['FromPort']
                ToPort = data['ToPort']
                IpProtocol = data['IpProtocol']
                IpRanges = data['IpRanges']
                for ip in IpRanges:
                  #  print ip['CidrIp']

                    if IP == ip['CidrIp']:
                        #Store data in file
    #                    print ('Found ip')
     #                   print (FromPort, ToPort, IpProtocol, IP, GroupName, GroupId)
                        output = str(FromPort)+':'+str(ToPort)+':'+str(IpProtocol)+':'+str(IP)+':'+GroupName+':'+str(GroupId)
                        f.write(output + '\n')
            except KeyError:
     #         print ('No data:')
               pass
    f.close()

    #output = subprocess.check_output("newfile.txt", shell=True)
    f = open("newfile1.txt", 'r')
    for row in f:
            row = row.rstrip('\n')
            FromPort = row.split(':')[0]
            ToPort = row.split(':')[1]
            IpProtocol = row.split(':')[2]
            IP = row.split(':')[3]
            GroupName = row.split(':')[4]
            GroupId = row.split(':')[5]
            print FromPort, ToPort, IpProtocol, IP, GroupName, GroupId
            try:
                    cmd = "aws ec2 revoke-security-group-ingress --region %s --group-id %s --port %s --protocol %s --cidr %s" %(region, GroupId, ToPort, IpProtocol, IP)
                    print 'IP revoke command:'+'\n'+cmd
                    os.system(cmd)
    #               print 'IP revoke command',cmd
            except Exception as e:
                    print 'Error:',e
                    break
    #aws ec2 revoke-security-group-ingress --group-id row[5] --port row[1] --protocol row[2] --cidr row[3]

            try:
                    cmd = "aws ec2 authorize-security-group-ingress --region %s --group-id %s --port %s --protocol %s --cidr %s" %(region,
GroupId, ToPort, IpProtocol, NEWIP)
                    print 'New IP insert command:'+'\n'+cmd
                    os.system(cmd)
            except Exception as e:
                    print 'Error:',e
                    break
    f.close()

if __name__ == '__main__':
    func(sys.argv[3])