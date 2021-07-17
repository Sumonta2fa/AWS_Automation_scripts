import boto3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

statuses = []

def inst_name(ec2_client, id):
    try:
        instance_name = ec2_client.describe_instances(InstanceIds=[id])
        for id, ints_data in enumerate(instance_name['Reservations']):
            # print(id,ints_data )
            for id, data in enumerate(instance_name['Reservations'][id]['Instances'][0]['Tags']):
                if data['Key'] == 'Name':
                    return data['Value']
    except Exception as e:
        print('Error: ',e)


def get_inst(region_name):
    ec2_client = boto3.client('ec2', region_name=region_name)
    res = ec2_client.describe_instance_status()
    st = ''
    for status in res['InstanceStatuses']:
        try:
            ins = "InstanceId: " + status['InstanceId']
            if not status['Events'][0]['Description'].startswith('[Completed]'):
                events_code = "Events Code: " + status['Events'][0]['Code']
                events_description = "Events Description: " + status['Events'][0]['Description']
                events_notbefore = status['Events'][0]['NotBefore']
                events_notbefore = "Events Not Before: " + datetime.strftime(events_notbefore, '%Y-%m-%d %H:%M:%S')
                events_notafter = status['Events'][0]['NotAfter']
                events_notafter = "Events Not After: " + datetime.strftime(events_notafter, '%Y-%m-%d %H:%M:%S')
                st += 'Name: '+inst_name(ec2_client, status['InstanceId'])+'\n'
                st +=  ins+'\n'
                st += events_code+'\n'
                st += events_description+'\n'
                st += events_notbefore+'\n'
                st += events_notafter+'\n\n'
        except Exception as e:
            pass
    # print(st, len(st))
    return st

# def sent_mail(buf):
#     msg = MIMEMultipart('mixed')
#     msg['From'] = 'aws_details@xxx.com'
#     #    msg['To'] = 'engg_ops@xxx.com'
#     datestr = str(datetime.now())
#     msg['Subject'] = 'AWS EC2 Events ' + datestr
#     textPart = MIMEText(buf, 'plain')
#     msg.attach(textPart)
#     receivers = ['sumonta@xxx.com']
#     try:
#         smtpObj = smtplib.SMTP('zimbra.xxx.net', 25)
#         smtpObj.sendmail('localhost', receivers, msg.as_string())
#         print("Successfully sent email")
#     except:
#         print("Error: unable to send email\n", msg.as_string())



if __name__ == '__main__':
    client = boto3.client('ec2')
    response = client.describe_regions()
    statuses = ''
    for region in response['Regions']:
        o = get_inst(region['RegionName'])
        if o:
            statuses += "\nRegion: {0}\n-----------------\n".format(region['RegionName'])
            statuses += o
    print(statuses)
    if statuses:
        sent_mail(statuses)


