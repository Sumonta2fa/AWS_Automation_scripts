import boto3



def filter_file():
    f = open(r'C:\Users\Sumonta\Desktop\sg_wildcard_entry', 'r')
    for list in f.readlines():
        print(list.split(',')[5])


def desc_sg_instance(sg_id):
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'instance.group-name',
                'Values': sg_id
            }])
    # print(response)
    for list in response['Reservations']:

        print(list['Instances'][0]['InstanceId'])
        print(list['Instances'][0]['Tags'])
        print (list['Instances'][0]['Tags'][0]['Value'])
        print (list['Instances'][0]['SecurityGroups'][0]['GroupName'])

if __name__ == '__main__':
    client = boto3.client('ec2', region_name='ap-south-1')
    sg_id = ['launch-wizard-1',
'launch-wizard-5',
'launch-wizard-4',
'launch-wizard-6',
'launch-wizard-3',
'launch-wizard-2']
    # filter_file()
    desc_sg_instance(sg_id)
