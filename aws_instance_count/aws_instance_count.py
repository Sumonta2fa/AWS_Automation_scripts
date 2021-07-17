from boto3.session import Session
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def genSession(region_name=None):
    session = Session(
        aws_access_key_id='xxx',
        aws_secret_access_key='xxx`/R4NFQ1d',
        region_name=region_name,
    )
    return session


def sent_mail(buf):
    msg = MIMEMultipart('mixed')
    msg['From'] = 'aws_details@xxxx.com'
#    msg['To'] = 'engg_ops@xxxx.com'
    datestr = str(datetime.now())
    msg['Subject'] = 'all regions current instance count ' + datestr
    textPart = MIMEText(str(buf), 'plain')
    msg.attach(textPart)
    receivers = ['sumonta@xxx.com']
    try:
        smtpObj = smtplib.SMTP('zimbra.xxxx.net', 25)
        smtpObj.sendmail('localhost', receivers, msg.as_string())
        print "Successfully sent email"
    except:
        print "Error: unable to send email", msg.as_string()


def list_instance(region_name):
    session = genSession(region_name)
    client = session.client('ec2')
    response = client.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    i = 0
    j = 0
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            i += 1
            for instance in instance["SecurityGroups"]:
                GroupName = instance["GroupName"]
                if GroupName[0:16]=='ElasticMapReduce':
                    j +=1
    return i, j

def get_regioins():
    session = genSession()
    client = session.client('ec2')
    response = client.describe_regions()
    file = open(filepath, 'w')
    for l in response["Regions"]:
        count, emr = list_instance(l["RegionName"])
        ll = l["RegionName"] +"||Running instance="+ str(count)+"||EMR instance="+ str(emr)+"||VPC instanace="+ str(count-emr)
        file.writelines(ll)
    file.close()

if __name__ == '__main__':
    filepath = '/tmp/aws_instance_count.txt'
    get_regioins(filepath)

    sent_mail(filepath)



