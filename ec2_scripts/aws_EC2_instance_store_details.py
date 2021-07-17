import boto3, csv

def KeyChcek(status):
    return status.keys()


def genSession(region_name=None):
    ec2_client = boto3.client('ec2', region_name=region_name)
    res = ec2_client.describe_instances()
    c = 0
    AvailabilityZone = ''
    InstanceType = ''
    InstanceId = ''
    Tags = ''
    BlockDeviceMappings = ''
    RootDeviceName = ''
    RootDeviceType = ''
    f = open('aws_EC2_instance_store_details.csv', "a+")
    fieldnames = {'AvailabilityZone', 'InstanceId', 'InstanceType', 'Tags', 'BlockDeviceMappings', 'RootDeviceName',
                  'RootDeviceType'}
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    try:
        for Response in res['Reservations']:
            # print Response
            for status in Response['Instances']:
                print status
                if status['SecurityGroups'][0]['GroupName'][0:16] == 'ElasticMapReduce' or status['State']['Name'] != 'running':
                    print "Found EMR instance or Not  Running"
                    break
                else:
                    for list_len in KeyChcek(status):
                        list_len = str(list_len.encode('UTF-8'))
                        if list_len == 'Placement':
                            AvailabilityZone = status['Placement']['AvailabilityZone']
                            print AvailabilityZone
                        elif list_len == "InstanceType":
                            InstanceType = status['InstanceType']
                            print InstanceType
                        elif list_len == "InstanceId":
                            InstanceId = status['InstanceId']
                            print InstanceId
                        elif list_len == "Tags" and len(status['Tags']) != 0:
                            Tags = str(status['Tags'][0]['Value'])
                            print Tags
                        elif list_len == "BlockDeviceMappings" and len(status['BlockDeviceMappings']) != 0:
                            BlockDeviceMappings = str(status['BlockDeviceMappings'][0]['DeviceName'])
                        elif list_len == 'RootDeviceName':
                            RootDeviceName = str(status['RootDeviceName'])
                        elif list_len == "RootDeviceType":
                            RootDeviceType = str(status['RootDeviceType'])
                        else:
                            pass
                    if c == len(f.read()):
                        writer.writeheader()
                    writer.writerow({'AvailabilityZone': AvailabilityZone, 'InstanceId': InstanceId, 'InstanceType': InstanceType, 'Tags': Tags, 'BlockDeviceMappings': BlockDeviceMappings, 'RootDeviceName': RootDeviceName, 'RootDeviceType': RootDeviceType})
                c += 1
                print "\n"
                print c
    except Exception as e:
        print e
        pass
    f.close()


if __name__ == '__main__':
    region = ['us-east-1', 'us-west-2', 'ap-southeast-1']
    for region_name in region:
        genSession(region_name)
    # genSession('us-east-1')
