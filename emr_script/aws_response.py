from boto3.session import Session
from datetime import datetime, timedelta
import csv
import os


#from collections import defaultdict
# Create the Boto3 Session
session = Session(
    aws_access_key_id='xxxx',
    aws_secret_access_key='xx',
    region_name='us-east-1',
)
client = session.client('emr')

response = client.list_clusters(
    CreatedAfter=datetime.now() - timedelta(hours = 14),
    CreatedBefore=datetime.now(),
    ClusterStates=['STARTING','TERMINATED','RUNNING','WAITING']
    )
#GMT
#UTC+8
print response
def InfoPrint(response):
    info = []
    count = 0
    os.remove("data1.csv")
    print("File Removed!")
    for list in (response['Clusters']):
        info = list['Status']
        Timeline = info['Timeline']
        t81 = Timeline['ReadyDateTime']
        t91 = Timeline['CreationDateTime']
        t9 = unicode(t91).partition('.')[0]
        t8 = unicode(t81).partition('.')[0]
        t10 = 'None'
        t7 = info['State']
        t6 = list['NormalizedInstanceHours']
        t5 = list['Id']
        t4 = list['Name']
        StateChangeReason = info['StateChangeReason']
        t3 = StateChangeReason['Message']

        if t7 == 'RUNNING':
            t10 = ''
            t2 = ''
        else:
            t101 = Timeline['EndDateTime']
            t2 = StateChangeReason['Code']
        f = open('data1.csv', "a+")
        fieldnames = ['Name', 'Id', 'State', 'Message', 'Code', 'CreationDateTime', 'EndDateTime', 'NormalizedInstanceHours', 'ReadyDateTime']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if count == 0:
            writer.writeheader()
            writer.writerow({'Name': t4, 'Id': t5, 'State': t7, 'Message': t3, 'Code': t2, 'CreationDateTime': t9, 'EndDateTime': t10, 'NormalizedInstanceHours': t6, 'ReadyDateTime':  t8})
        else:

            writer.writerow({'Name': t4, 'Id': t5, 'State': t7, 'Message': t3, 'Code': t2, 'CreationDateTime': t9, 'EndDateTime': t10, 'NormalizedInstanceHours': t6, 'ReadyDateTime': t8})
        count += 1
        f.close()

InfoPrint(response)

