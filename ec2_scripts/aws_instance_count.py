from boto3.session import Session
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def genSession(region_name=None):
    session = Session(
        aws_access_key_id='xxx',
        aws_secret_access_key='xxx/R4NFQ1d',
        region_name=region_name,
    )
    return session


def sent_mail(buf):
    msg = MIMEMultipart('mixed')
    msg['From'] = 'aws_details@xx.com'
#    msg['To'] = 'engg_ops@xx.com'
    datestr = str(datetime.now())
    msg['Subject'] = 'all regions current instance count ' + datestr
    textPart = MIMEText(str(buf), 'plain')
    msg.attach(textPart)
   receivers = ['sumonta@xx.com']
    try:
        smtpObj = smtplib.SMTP('zimbra.xx.net', 25)
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
    #print region_name
    #print(response)
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            #print(instance)
            #print(instance["InstanceId"])
            #print(instance["Tags"])
            i += 1
            for instance in instance["SecurityGroups"]:
                GroupName = instance["GroupName"]
                #print GroupName[0:16]
                if GroupName[0:16]=='ElasticMapReduce':
                    j +=1
    #print i, j
    return i, j

def get_regioins():
    session = genSession()
    client = session.client('ec2')
    response = client.describe_regions()
    buf = []
   # print('Regions:', response['Regions'])
    for list in response["Regions"]:
        #print list["RegionName"]
        count, emr = list_instance(list["RegionName"])
        #print(list["RegionName"], count)
        ll = list["RegionName"] +"||Running instance="+ str(count)+"||EMR instance="+ str(emr)+"||VPC instanace="+ str(count-emr)
        buf.append(ll)
    #print buf
    st = ''''''
    for list in buf:
        # print list
        st = st + list + '\n'
    print st
    sent_mail(st)

if __name__ == '__main__':
    get_regioins()

