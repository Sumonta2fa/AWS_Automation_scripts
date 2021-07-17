from boto3.session import Session
from datetime import datetime, timedelta
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders



session = Session(
    aws_access_key_id='XXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXXX',
    region_name='us-east-1',
)
client = session.client('emr')

response = client.list_clusters(
    CreatedAfter=datetime.now() - timedelta(hours = 1),
    CreatedBefore=datetime.now(),
    ClusterStates=['TERMINATED_WITH_ERRORS']
    )
print response

def testCluserCheck(CId):
  print("CId", CId)
    response = client.describe_cluster(ClusterId=CId)
    print("response['Cluster']", var)
    for var in response['Cluster']:
      print("var['Tags']", tags)
      for tags in var['Tags']:
        print("tags", tags)
        if tags[“Key”] == ‘Name’:
          if tags[“Value”] == 'Test':
            print('This is a test Instance, Ignored.')
            return False
    return True

def InfoPrint(response):
    info = []
    count = 0
    
    print("File Removed!")
    for list in (response['Clusters']):
        info = list['Status']
        Timeline = info['Timeline']
        t91 = Timeline['CreationDateTime']
        t9 = unicode(t91).partition('.')[0]
        t10 = 'None'
        t7 = info['State']
        t6 = list['NormalizedInstanceHours']
        t5 = list['Id']
        t4 = list['Name']
        StateChangeReason = info['StateChangeReason']
        t3 = StateChangeReason['Message']

        if t7 == 'RUNNING':
            t10 = ''
        elif t7 == 'WAITING':
            t10 = ''
        else:
            t101 = Timeline['EndDateTime']
            t10 = unicode(t101).partition('.')[0]
        datestring = datetime.strftime(datetime.now(), '%Y-%m-%d')
        
        if testCluserCheck(t5):
          f = open('error_'+datestring+'.csv', 'a+')
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
msg['To'] = 'xx@xx.com'
datestr = str(datetime.now().date())
msg['Subject'] = 'EMR cluster "TERMINATED_WITH_ERROR" '+datestr
msg.attach(MIMEText("EMR cluster TERMINATED_WITH_ERROR"))
datestring = datetime.strftime(datetime.now(), '%Y-%m-%d')
file = 'error_'+datestring+'.csv'
attachment = MIMEBase('application', 'octet-stream')
attachment.set_payload(open(file,'rb').read())
Encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
msg.attach(attachment)


try:
   smtpObj = smtplib.SMTP('jump-xx-prod',25)
   smtpObj.sendmail('localhost', 'dongni@xxxxx.com', msg.as_string())
   print "Successfully sent email"
except :
   print "Error: unable to send email"

os.remove('error_'+datestring+'.csv')

