#!/usr/bin/python
from boto3.session import Session
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
"""
arguments like

python aws_instance_count.py -w 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 -c 10,10,10,10,10,10,10,10,10,10,10,10,10,10,10

command[aws_instance_count]=/usr/lib/nagios/plugins/aws_instance_count.py -w 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 -c 10,10,10,10,10,10,10,10,10,10,10,10,10,10,10

"""
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
    datestr = str(datetime.now())
    msg['Subject'] = 'all regions current instance count ' + datestr
    textPart = MIMEText(str(buf), 'html')
    msg.attach(textPart)
#    receivers = ['sumonta@xx.com']
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
def found_diff():
    warning = []
    critical = []
    for list in sys.argv[2].split(','):
        warning.append(list)
    for list in sys.argv[4].split(','):
        critical.append(list)
    return warning, critical
def get_regioins(warning, critical):
    session = genSession()
    client = session.client('ec2')
    response = client.describe_regions()
    buf = []
    vpc_val = []
    a = 0
    alert = []
    for list in response["Regions"]:
        count, emr = list_instance(list["RegionName"])
        vpc_inst = count-emr
        ll = list["RegionName"] +"||Running instance="+ str(count)+"||EMR instance="+ str(emr)+"||VPC instanace="+ str(vpc_inst)
        buf.append(ll)
        #print list, type(vpc_inst), type(critical[a]), vpc_inst, critical[a]
        c = int(critical[a])
        w = int(warning[a])
        if vpc_inst > c:
            alert.append('2')
        elif vpc_inst <= c and vpc_inst > w:
            alert.append('1')
        elif vpc_inst <= w:
            alert.append('0')
        else:
            alert.append('3')
        a += 1
        vpc_val.append(vpc_inst)
    st = ''''''
    for list in buf:
        # print list
        st = st + list + '\n'
    #print st
    #sent_mail(st)
    nrpe_alert(alert, vpc_val)

def nrpe_alert(alert, vpc_val):
    st = 'instance launched:'
    alert.sort(reverse=True)
    #print 'nrpe_alert', alert, vpc_val
    diff = alert[0]
    #print type(diff), diff
    if diff == "0":
        print "OK - %s" % st, vpc_val
        sys.exit(0)
    elif diff == "1":
        print "WARNING - %s" % st, vpc_val
        sys.exit(1)
    elif diff == "2":
        print "CRITICAL - %s" % st, vpc_val
        sys.exit(2)
    else:
        print "UKNOWN - %s" % st, vpc_val
        sys.exit(3)

if __name__ == '__main__':
    warning, critical = found_diff()
    #print warning, critical
    get_regioins(warning, critical)
