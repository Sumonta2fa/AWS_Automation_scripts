import boto3
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

data_list = ['AlarmName', 'AlarmDescription', 'StateReason']

def sent_mail(buf):
    msg = MIMEMultipart('mixed')
    msg['From'] = 'aws_details@xxx.com'
    #    msg['To'] = 'engg_ops@xxx.com'
    datestr = str(datetime.now())
    msg['Subject'] = 'AWS Cloud Watch Alarm : '+ d['AlarmName'] + datestr
    textPart = MIMEText(str(buf), 'plain')
    msg.attach(textPart)
    receivers = ['sumonta@xxx.com']
    try:
        smtpObj = smtplib.SMTP('zimbra.xxx.net', 25)
        smtpObj.sendmail('localhost', receivers, msg.as_string())
        print("Successfully sent email")
    except:
        print("Error: unable to send email\n", msg.as_string())


if __name__ == '__main__':
    ignore_list = ['EstimatedChargesAlarm']
    d = {}

    # Create CloudWatch client
    client = boto3.client('cloudwatch')
    response = client.describe_alarms(StateValue='ALARM')
    print(response)
    for list in (response['MetricAlarms']):
        # print(list)
        d = {}
        if not list['AlarmName'] in ignore_list:
            for key, val in list.items():
                if key in data_list:
                    # print(key, val)
                    d[key] = list[key]
            print(d['AlarmName'])
            # sent_mail(d)
