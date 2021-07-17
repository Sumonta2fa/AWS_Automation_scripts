from boto3.session import Session
from datetime import datetime, timedelta

session = Session(
    aws_access_key_id='xxx',
    aws_secret_access_key='xxx',
    region_name='us-east-1',
)
client = session.client('emr')

response = client.list_clusters(
    CreatedAfter=datetime.now()- timedelta(hours = 19),
    CreatedBefore=datetime.now(),
    ClusterStates=['WAITING', ]
    )

print response

for list in (response['Clusters']):
    info = list['Status']
    Timeline = info['Timeline']
    t91 = Timeline['CreationDateTime']
    t92 = unicode(t91).partition('.')[0]
    t5 = list['Id']
    t4 = list['Name']
    bucket_id.append(t5)
    bucket_time.append(t92)
    s = 1
    bucket = bucket_id + bucket_time
print bucket
if (s == 1):
    dataSend(bucket)
else:
    pass

