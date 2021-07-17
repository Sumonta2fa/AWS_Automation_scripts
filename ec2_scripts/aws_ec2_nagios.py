import boto3
import csv

client = boto3.client('ec2')
response = client.describe_instances(
    Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
        ],
)
f = open('instance_info_nagios.csv', 'w')
columns = ['hostgroup','instance_name','PrivateIpAddress','PublicIpAddress']

writer = csv.DictWriter(f, fieldnames=columns)

for host in response['Reservations']:
    try:
        for Instances in host['Instances']:
            print(Instances)
            print(Instances['PublicIpAddress'], Instances['PrivateIpAddress'])
            instance_name = 0
            hostgroup = 0
            for tags in Instances['Tags']:
                print(tags)
                if tags['Key'] == 'Name':
                    instance_name = tags['Value']
                if tags['Key'] == 'nagios_hostgroups':
                    hostgroup = tags['Value']

            try:
                print(instance_name, hostgroup)
                if instance_name and hostgroup:
                    writer.writerow({'hostgroup': hostgroup, 'instance_name': instance_name, 'PrivateIpAddress': Instances['PrivateIpAddress']})
            except:
                pass
    except Exception as e:
        print('Error: ',e)

f.close()
