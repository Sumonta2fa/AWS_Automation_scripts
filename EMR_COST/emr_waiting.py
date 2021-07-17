from boto3.session import Session
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

bucket = []
s = 0

session = Session(
    aws_access_key_id='xxx',
    aws_secret_access_key='xxx',
    region_name='us-east-1',
)
client = session.client('emr')

response = client.list_clusters(
    CreatedAfter=datetime.now()- timedelta(hours = 14),
    CreatedBefore=datetime.now(),
    ClusterStates=['WAITING']
    )

def dataSend(body):
    msg = MIMEMultipart('mixed')
    msg['From'] = 'zimbra.xxx.net'
    msg['To'] = 'engg@xxx.com'
    msg['Subject'] = 'AWS instance in waiting state'
    msg.attach(MIMEText("Instance Waiting State: "))
    textPart = MIMEText(str(body), 'plain')
    msg.attach(textPart)#    receivers = ['sumonta@xxx.com']  # Please change the line
    print msg.as_string()

    try:
        smtpObj = smtplib.SMTP('zimbra.xxx.net', 25)
        smtpObj.sendmail('localhost', receivers, msg.as_string())
        print "Successfully sent email"
    except:
        print "Error: unable to send email"



#print response

for list in (response['Clusters']):
    info = list['Status']
    Timeline = info['Timeline']
    t91 = Timeline['CreationDateTime']
    t92 = unicode(t91).partition('.')[0]
    t5 = list['Id']
    t4 = list['Name']
    bucket_name = t4
    bucket_id = t5


    s = 1
    data = bucket_name +' '+bucket_id
    bucket.append(data)

print bucket
if (s == 1):
    dataSend(bucket)
else:
    pass

