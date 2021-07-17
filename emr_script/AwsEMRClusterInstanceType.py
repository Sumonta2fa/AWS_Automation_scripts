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
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-1',
)
client = session.client('emr')

response = client.list_clusters(
    CreatedAfter=datetime.now() - timedelta(hours = 24),
    CreatedBefore=datetime.now(),
    ClusterStates=['STARTING','TERMINATED','RUNNING','WAITING','TERMINATED_WITH_ERRORS']
    )
#GMT
#UTC+8
# print response
def InfoPrint(response):
    info = []
    count = 0
    
   #os.remove("/home/ashish/script/data24.csv")
    # print("File Removed!")
    for list in (response['Clusters']):
        info = list['Status']
        Timeline = info['Timeline']
       # t8 = Timeline['ReadyDateTime']
        #t9 = Timeline['CreationDateTime']
#       t81 = Timeline['ReadyDateTime']
        t91 = Timeline['CreationDateTime']
        t9 = unicode(t91).partition('.')[0]
 #       t8 = unicode(t81).partition('.')[0]
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
        print('ClusterID:' ,t5)
        Cluser_response = client.list_instances(ClusterId=t5)
        clusterInstances = Cluser_response['Instances']
        print(Cluser_response)

        f = open('data_'+datestring+'.csv', 'a+')
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
os.remove('data_'+datestring+'.csv')
