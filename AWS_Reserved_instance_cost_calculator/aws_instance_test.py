import boto3
import csv
import os
# AWS Reserved instance cost counter,
# Requirment an CSV instance price list
# Calculate Volume price also

#Region_name = 'ap-southeast-1'
#Region_name = 'us-west-2'
Region = []
Region.append('us-east-1')
Region.append('us-west-2')
Region.append('ap-southeast-1')

for Region_name in Region:
    count = 0
    #Define unit volume price
    us_gp2_price = 0.10
    us_Stnd_price = 0.05
    ap_gp2_price = 0.12
    ap_Stnd_price = 0.08
    #Make file name
    fName = 'aws_instane_price_'+Region_name+'.csv'
    Value = 0
    reserver = 'None'
    platform = 0
    instance_type = 0
    zone = 0
    i = 0
    your_list = ()
    client = boto3.resource('ec2',
            aws_access_key_id='xx',
            aws_secret_access_key='xx',
            region_name=Region_name)

    instances = client.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    #create CSV file
    try:
        os.remove(fName)   # Remove old file to clear file
    except Exception as e:
                print 'Warning:', e
    f = open(fName, 'a+')
    fieldnames = ['Region Name','Instance Name', 'Instance Id', 'Instance Type', 'VPC Id','Block Device Name', 'Platform', 'State', 'Availability Zone','Reserved/On-demand', 'Instance Price/hour', 'Instance Price/month', 'Instance Price/year', 'Volume Price/year', 'Total Price/year']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    #Reserved confition check
    def if_reserver( instance_type, platform, zone):
       # print instance_type, platform, zone
        for j in range(i):
           # print elements[j][0]
            if platform == elements[j][0]:
         #       print 'instance_type, elements[j][1]', instance_type, elements[j][1]
                if instance_type == elements[j][1]:
                   # print 'elements[j][2]zone', zone, elements[j][2]
                    if (zone == elements[j][2] or elements[j][2] == 'Region') and (elements[j][3] != 0):
                        int = elements[j][3]
                        #print 'int, elements[j][3]', int, elements[j][3]
                        elements[j][3] = int - 1
                      #  print 'Reserved'
                        return 'Reserved'
                    elif (zone == elements[j][2] or elements[j][2] == 'Region') and (elements[j][3] == 0):
                     #   print 'On-demand'
                        return 'On-demand'
                    else:
                        pass
                else:
                    pass

            else:
                pass
    #=================================================
    #Append Price list
    def dump_price(instance_type, platform, zone, reserver):
        #print 'dump_price', instance_type, platform, zone, reserver
        for list in your_list:
            if ((platform == 'Linux/UNIX (Amazon VPC)') or (platform == 'Linux/UNIX')):
                platform = 'Linux'
            else:
                pass
         #   print 'instance_type == list[0]', instance_type, list[0]
            if (instance_type == list[0]):
          #      print 'platform == list[1]', platform, list[1]
                if (platform == list[1]):
           #         print 'zone[:2]', zone[:2],'list[4]', list[4]
                    if (zone[:2] == list[4]):
                        if (reserver == 'Reserved'):
                        #    print list[2]
                            return list[2]
                        elif (reserver == 'On-demand'):
                        #    print list[3]
                            return list[3]
                    else:
                        pass
                else:
                    pass
            else:
                pass

    #Collect Price list
    with open('AWS_inatance_price_list.csv', 'rb') as f:
        reader = csv.reader(f)
        #global your_list
        your_list = map(tuple, reader)
    #====================================================
    #Reserve instance details collection and put it in array

    client = boto3.client('ec2',
            aws_access_key_id='xx',
            aws_secret_access_key='xx',
            region_name=Region_name)

    response = client.describe_reserved_instances(
        Filters=[{'Name': 'state', 'Values': ['active']}])

    #print response
    elements = []
    i = 0

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

        #    print ProductDescription, InstanceType, State, Duration, Scope, InstanceCount
            elements.append([])
           # global i
            elements[i].append(ProductDescription)
            elements[i].append(InstanceType)
            elements[i].append(Scope)
            elements[i].append(InstanceCount)
            i +=1
    #=================================================================
    #Describe Volumn price
    #
    def volPrice(id):
        p_list = []
        #Define instance Size
        instances = client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['in-use']}, {'Name': 'attachment.instance-id', 'Values': [id]}])

        #print instances['Volumes']
        #Loop for collecting Vol information
        for instance in instances['Volumes']:
            try:
                AvailabilityZone = instance['AvailabilityZone']
                for list in instance['Attachments']:
                    InstanceId = list['InstanceId']
                    VolumeId = list['VolumeId']
                    State = list['State']
                    Device = list['Device']
                    print InstanceId, VolumeId, State, Device
                VolumeType = instance['VolumeType']
                State = instance['State']
                Size = instance['Size']

                print AvailabilityZone[0:2], VolumeType, State, Size
                if AvailabilityZone[0:2] == 'us' and VolumeType == 'gp2':
                    p_list.append(Size * us_gp2_price )
                elif AvailabilityZone[0:2] == 'us' and VolumeType == 'standard':
                    p_list.append(Size * us_Stnd_price)
                elif AvailabilityZone[0:2] == 'ap' and VolumeType == 'gp2':
                    p_list.append(Size * ap_gp2_price)
                elif AvailabilityZone[0:2] == 'ap' and VolumeType == 'standard':
                    p_list.append(Size * ap_Stnd_price)

            except Exception as e:
                print 'Error:', e
       # print sum(p_list)
        return (sum(p_list) * 12 )

    #print elements
    #==================================
    for instance in instances:
        DeviceName = []
        q = instance.state
        p = instance.block_device_mappings
        for data in p:
            DeviceName.append(data['DeviceName'])
        if not DeviceName:
            DeviceName = 'Instance Store'

        val = instance.tags
        for list in val:
            Value = list['Value']
        place = instance.placement
        zone = place['AvailabilityZone']
      #  print DeviceName, Value
    #instance platform recheck
        platform = str(instance.platform)
        vpc_id = str(instance.vpc_id)
       # print zone, instance.instance_type
        if platform == 'windows':
            platform = 'Windows'
        else:
            pass
        if (vpc_id=='None' and platform=='None'):
            platform = 'Linux/UNIX'
        elif(vpc_id!='None' and platform == 'None'):
            platform = 'Linux/UNIX (Amazon VPC)'
        else:
            pass
        #Reserved check define here
        reserver = if_reserver( instance.instance_type, platform, zone )
        reserver = str(reserver)
        if reserver == 'None':
            reserver = 'On-demand'
        else:
            pass

        # price calculate
        price = dump_price(instance.instance_type, platform, zone, reserver)

       # print(instance.id, instance.instance_type, vpc_id, platform, zone, reserver, price )
        ppm = float(price) * 720
        ppy = float(price) * 8760
        # Set Volume price
        print volPrice(instance.id)
        vPrice = volPrice(instance.id)
        totPrice = ppy + vPrice
        print totPrice
    #Storing Data in CSV file
        if count == 0:
            writer.writeheader()
            writer.writerow({'Region Name': Region_name, 'Instance Name': Value, 'Instance Id': instance.id, 'Instance Type': instance.instance_type, 'VPC Id': vpc_id,'Block Device Name': DeviceName, 'Platform': platform, 'State': q['Name'], 'Availability Zone': zone, 'Reserved/On-demand': reserver, 'Instance Price/hour': price, 'Instance Price/month': ppm, 'Instance Price/year': ppy, 'Volume Price/year': vPrice, 'Total Price/year': totPrice})
        else:
            writer.writerow({'Region Name': Region_name, 'Instance Name': Value, 'Instance Id': instance.id, 'Instance Type': instance.instance_type, 'VPC Id': vpc_id,'Block Device Name': DeviceName, 'Platform': platform, 'State': q['Name'], 'Availability Zone': zone, 'Reserved/On-demand': reserver, 'Instance Price/hour': price, 'Instance Price/month': ppm, 'Instance Price/year': ppy, 'Volume Price/year': vPrice, \
    'Total Price/year': totPrice})
        count += 1

    f.close()
'''
#CSV Short by instance type

f = open("aws_instane_details_singapore.csv", 'rb')
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
f = open('aws_instane_details_final.csv', 'wb')
#create write object
wr = csv.writer(f, dialect='excel')

for list in k:
    print list
    wr.writerow(list)
'''
