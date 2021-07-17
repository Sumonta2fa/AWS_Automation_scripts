from boto3.session import Session
import urllib2
from bs4 import BeautifulSoup

def genSession(region_name=None):
    session = Session(
        aws_access_key_id='xxx',
        aws_secret_access_key='xxx/xx',
        region_name=region_name,
    )
    client = session.client('ec2')
    response = client.describe_security_groups()
    f.write(region_name)
    for i in response['SecurityGroups']:
        GroupName = i['GroupName']
        GroupId = i['GroupId']
        SGNAME =  '**' + GroupName+'\t'+GroupId+'\n'
        f.write(SGNAME)
        for ips in i['IpPermissions']:
            for list in ips['IpRanges']:
                txt = ''
                if list['CidrIp'] != "0.0.0.0/0":
                    txt = ISPlookup(list['CidrIp'][:-3])
                    print list['CidrIp'], txt
                    IPDetails = str(list['CidrIp']) + '\t' + str(txt) + '\n'
                    f.write(IPDetails)


def ISPlookup(ip):
    url ='https://www.whoismyisp.org/ip/'
    url = url+ip
    try :
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html5lib")
        th_all = soup.find_all("p", class_="isp", text=True)
        th_all1 = soup.find_all("p", class_="aka")
        result = []
        for th in th_all:
            result.extend(th.find_all(text=True))
        for th in th_all1:
            result.extend(th.find_all(text=True))
        return result
    except Exception as e:
        return e

if __name__ == '__main__':
    f = open('aws_SG_IP_Desc.txt', "w")
    genSession('ap-south-1')
    f.close()
