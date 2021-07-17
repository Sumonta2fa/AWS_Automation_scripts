from boto3.session import Session
import boto3
from datetime import datetime, timedelta
import csv
f = open("aws_instane_details.csv", 'rb')
reader = csv.reader(f)

l = []
for list in reader:
    l.append(list)
f.close()
print l

def getKey(item):
    return item[3]
k = sorted(l, key=getKey)
#open file
f = open('eggs.csv', 'wb')
f.truncate()
#create write object
wr = csv.writer(f, dialect='excel')

for list in k:
    print list
    wr.writerow(list)


'''
client = boto3.client('ec2',
        aws_access_key_id='xx',
        aws_secret_access_key='xx',
        region_name='us-west-2')



response = client.describe_reserved_instances(
    Filters=[{'Name': 'state', 'Values': ['active']}])

#print response
elements = []

i = 0
#Reserved confition check

def if_reserver( instance_type, platform, zone):

    print instance_type, platform, zone
    for j in range(i):
        #print elements[j][0]
        if platform == elements[j][0]:
            #print 'instance_type, elements[j][1]', instance_type, elements[j][1]
            if instance_type == elements[j][1]:
                #print 'elements[j][2]zone', zone, elements[j][2]
                if (zone == elements[j][2] or elements[j][2] == 'Region') and (elements[j][3] != 0):
                    int = elements[j][3]
             #       print 'int, elements[j][3]', int, elements[j][3]
                    elements[j][3] = int - 1
                    return 'Reserved'

                else:
                    pass
            else:
                pass

        else:
            pass
print response
for list in response['ReservedInstances']:
        ProductDescription = list['ProductDescription']
        InstanceType = list['InstanceType']
        State =  list['State']
        Duration = list['Duration']
        InstanceCount = list['InstanceCount']
        Scope = list['Scope']
        Scope = str(Scope)
        if Scope == 'Availability Zone':
            Scope = list['AvailabilityZone']
        else:
            AvailabilityZone = 'None'
        #print ProductDescription, InstanceType, State, Duration, Scope, InstanceCount
        global i
        elements.append([])
        elements[i].append(ProductDescription)
        elements[i].append(InstanceType)
        elements[i].append(Scope)
        elements[i].append(InstanceCount)

        i +=1



#print elements


#['Linux/UNIX (Amazon VPC)', 'c3.2xlarge', 'us-east-1c', 10]
# ProductDescription InstanceType Scope InstanceCount
#instance_type platform zone

#print elements
#print if_reserver( instance_type, platform, zone)
#print if_reserver( instance_type, platform, zone)
#print elements
'''
'''
#Import csv for instance price


#c3.2xlarge	Linux	0.42	0.157	us

def dump_price(instance_type, platform, zone, reserver):
    for list in your_list:
        if ((instance_type == 'Linux/UNIX (Amazon VPC)') or (instance_type == 'Linux/UNIX')):
            list[1].append('Linux')
        else:
            pass

        if (instance_type == list[0]):
            if (platform == list[1]):
                if (zone[:2] == list[4]):
                    if (reserver == 'Reserved'):
                        print list[2]
                        return list[2]
                    else:
                        print list[3]
                        return list[3]
                else:
                    pass
            else:
                pass
        else:
            pass

#m3.xlarge	Linux	0.392	0.147	as
#m1.xlarge	Linux	0.35	0.117	us


instance_type = 'm3.xlarge'
platform = 'Linux'
zone = 'ap-southeast'
reserver = 'Reserved'
with open('C:\Users\User\Downloads\AWS.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = map(tuple, reader)

#print your_list[1]
dump_price(instance_type, platform, zone, reserver)


'''









