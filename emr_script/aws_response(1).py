from boto3.session import Session
from datetime import datetime, timedelta
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders



#from collections import defaultdict
# Create the Boto3 Session
session = Session(
    aws_access_key_id='xxx',
    aws_secret_access_key='xx+x',
    region_name='us-east-1',
)
client = session.client('emr')

response = client.list_clusters(
    CreatedAfter=datetime.now() - timedelta(hours = 14),
    CreatedBefore=datetime.now(),
    ClusterStates=['STARTING','TERMINATED','RUNNING','WAITING','TERMINATED_WITH_ERRORS']
    )
#GMT
#UTC+8
print response
def InfoPrint(response):
    info = []
    count = 0
#    os.remove("/home/ashish/script/data1.csv")
    print("File Removed!")
    for list in (response['Clusters']):
        info = list['Status']
        Timeline = info['Timeline']
       # t8 = Timeline['ReadyDateTime']
        #t9 = Timeline['CreationDateTime']
#	t81 = Timeline['ReadyDateTime']
        t91 = Timeline['CreationDateTime']
        t9 = unicode(t91).partition('.')[0]
#        t8 = unicode(t81).partition('.')[0]	
        t10 = 'None'
        t7 = info['State']
        t6 = list['NormalizedInstanceHours']
        t5 = list['Id']
        t4 = list['Name']
        StateChangeReason = info['StateChangeReason']
        t3 = StateChangeReason['Message']

        if t7 == 'RUNNING':
            t10 = ''
            # t2 = ''
        elif t7 == 'WAITING':
            t10 = ''

        else:
            t101 = Timeline['EndDateTime']
            t10 = unicode(t101).partition('.')[0]
            #t2 = StateChangeReason['Code']
        f = open('data.csv', "a+")
        fieldnames = ['Name', 'Id', 'State', 'Message', 'CreationDateTime', 'EndDateTime', 'NormalizedInstanceHours']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if count == 0:
            writer.writeheader()
            writer.writerow({'Name': t4, 'Id': t5, 'State': t7, 'Message': t3, 'CreationDateTime': t9, 'EndDateTime': t10, 'NormalizedInstanceHours': t6})
        else:

            writer.writerow({'Name': t4, 'Id': t5, 'State': t7, 'Message': t3, 'CreationDateTime': t9, 'EndDateTime': t10, 'NormalizedInstanceHours': t6})
        count += 1
        f.close()

InfoPrint(response)

msg = MIMEMultipart()
msg['From'] = 'jump-xx-prod'
msg['To'] = 'sumonta@xxxx.com'
datestr = datetime.now()
datestring = str(unicode(datestr).partition('.')[0])
msg['Subject'] = 'EMR cluster details '+datestring
msg.attach(MIMEText("EMR cluster details"))
file = 'data.csv'
attachment = MIMEBase('application', 'octet-stream')
attachment.set_payload(open(file,'rb').read())
Encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
msg.attach(attachment)

#response = """From: localhost
#Subject: cluster details in csv format

#This is a test e-mail message.
#"""+(str(msg.attach(attachment)))

try:
   smtpObj = smtplib.SMTP('jump-server-prod',25)
   smtpObj.sendmail('localhost', 'sumonta@xxxx.com', msg.as_string())
   print "Successfully sent email"
except :
   print "Error: unable to send email"

