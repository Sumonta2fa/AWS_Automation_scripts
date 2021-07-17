from boto3.session import Session
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def genSession(region_name=None):
    session = Session(
        aws_access_key_id='xxxxx',
        aws_secret_access_key='xxx/R4NFQ1d',
        region_name=region_name,
    )
    client = session.client('ec2')
    return client

def desc_ins(client, InstanceIds):
    response = client.describe_instances(
        InstanceIds=[InstanceIds],
    )
    InstanceId = response['Reservations'][0]['Instances'][0]['InstanceId']
    PublicIp = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicIp']
    NetworkInterfaces = response['Reservations'][0]['Instances'][0]['NetworkInterfaces']
    print InstanceId, PublicIp, NetworkInterfaces
    return PublicIp

def Allocatc_ElasticIp(client):
    response = client.allocate_address(
        Domain='vpc',
    )
    AllocationId = response['AllocationId']
    PublicIp = response['PublicIp']
    print AllocationId, PublicIp
    return AllocationId, PublicIp

def Associate_ip(client, AllocationId, InstanceId):
    response = client.associate_address(
        AllocationId=AllocationId,
        InstanceId=InstanceId,
    )
    print response
    return response['AssociationId']

def disassociate_ip(AssociationId):
    response = client.disassociate_address(
        AssociationId=AssociationId,
    )
    print(response)
def sent_mail(buf):
    msg = MIMEMultipart('mixed')
    msg['From'] = 'aws_details@xx.com'
    datestr = str(datetime.now())
    msg['Subject'] = 'VPN ip replace ' + datestr
    textPart = MIMEText(str(buf), 'html')
    msg.attach(textPart)
    receivers = ['engg_ops@xx.com']
    try:
        smtpObj = smtplib.SMTP('zimbra.xx.net', 25)
        smtpObj.sendmail('localhost', receivers, msg.as_string())
        print "Successfully sent email"
    except:
        print "Error: unable to send email", msg.as_string()


def ip_Addr_Chech(client, ExistingPublicIp, NewIP):
    response = client.describe_regions()
    for list in response["Regions"]:
        print "Ip Address checking: "+ list["RegionName"]
        cmd = "python aws_security_group_ip_replace.py %s/32 %s/32 %s" %(ExistingPublicIp, NewIP, list["RegionName"])
        os.system(cmd)


if __name__ == '__main__':
    region_name = 'us-east-1'
    InstanceId = 'i-06f751c8dc8fee343'
    data = []
    f = open('aws_vpn_ip_replace.txt', "r")
    AssociationId = f.read()
    f.close()
    AssociationId = AssociationId.strip('\n')
    client = genSession(region_name)
    ExistingPublicIp = desc_ins(client, InstanceId)
#    disassociate_ip(ExistingPublicIp)
    disassociate_ip(AssociationId)
    AllocationId, NewIP = Allocatc_ElasticIp(client)
    AssociationId = Associate_ip(client, AllocationId, InstanceId)
    ip_Addr_Chech(client, ExistingPublicIp, NewIP)
    log = 'InstanceId: '+ InstanceId,' ExistingPublicIp: '+ ExistingPublicIp,' AllocationId: '+ AllocationId,' NewIP: '+ NewIP,' AssociationId: '+ AssociationId
    data.append(str(log))
    print data
    f = open('aws_vpn_ip_replace.txt', "w")
    f.write(AssociationId)
    f.close()
    sent_mail(data)
