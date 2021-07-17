from boto3.session import Session
from datetime import datetime
import csv
import json


#from collections import defaultdict
from dateutil import parser
# Create the Boto3 Session
session = Session(
    aws_access_key_id='xx',
    aws_secret_access_key='xx',
    region_name='us-east-1',
)
client = session.client('emr')

response = client.list_clusters(
    CreatedAfter=datetime(2016, 12, 23, 0),
    CreatedBefore=datetime(2016, 12, 23, 12),
    ClusterStates=['STARTING','TERMINATED','RUNNING','WAITING',]
    )
print (response)
def InfoPrint(response):
    info = []
    count = 0
    for list in (response['Clusters']):
        info = list['Status']
        Timeline = info['Timeline']
        t8 = Timeline['ReadyDateTime']
        t9 = Timeline['CreationDateTime']
        t10 = Timeline['EndDateTime']
        t7 = info['State']
        t6 = list['NormalizedInstanceHours']
        t5 = list['Id']
        t4 = list['Name']
        StateChangeReason = info['StateChangeReason']
        t3 = StateChangeReason['Message']
        t2 = StateChangeReason['Code']
        var = t2 +'\t'+ t3 + ' ' + t4
        print (var)
        f = open('data1.csv', "a+")

        fieldnames = ['Name', 'Id', 'State', 'Message', 'Code', 'CreationDateTime',  'EndDateTime', 'NormalizedInstanceHours', 'ReadyDateTime']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if count == 0:
            writer.writeheader()
            writer.writerow({'Name': t4, 'Id': t5, 'State': t7, 'Message': t3, 'Code': t2, 'CreationDateTime': t9, 'EndDateTime': t10, 'NormalizedInstanceHours': t6, 'ReadyDateTime':  t8})
        else:

            writer.writerow({'Name': t4, 'Id': t5, 'State': t7, 'Message': t3, 'Code': t2, 'CreationDateTime': t9,
                             'EndDateTime': t10, 'NormalizedInstanceHours': t6, 'ReadyDateTime': t8})
        count += 1
        #f.write('\n')
        f.close()

InfoPrint(response)

