import boto3

#Region_name = 'ap-southeast-1a'
Region_name = 'us-east-1'
#Region_name = 'us-west-2'
id = 'i-11c344e6'
client  = boto3.client('ec2',
        aws_access_key_id='xxxx',
        aws_secret_access_key='xxx',
        region_name=Region_name)
id = 'i-5970e6b4'
us_gp2_price = 0.2
us_Stnd_price = 0.4
ap_gp2_price = 0.5
ap_Stnd_price = 0.7
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
             #   print InstanceId, VolumeId, State, Device
            VolumeType = instance['VolumeType']
            State = instance['State']
            Size = instance['Size']

            #print AvailabilityZone[0:2], VolumeType, State, Size
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
    return sum(p_list)

print volPrice(id)