import boto3

client = boto3.client('emr')

response = client.list_clusters(ClusterStates=['RUNNING'])

print(response)