import boto3
import yaml
from datetime import datetime
import math

import platform;

"""

list_clusters
Pricing for Amazon EMR and Amazon EC2 (On-Demand) or Amazon EC2 (Spot Instance)
When you run one instance for 10 minutes, stop the instance, and then start the instance again, you are billed for two instance-hours.
"""

def fetch_cost(hr, ins_type):
    ec2_cost = my_dict['prices'][ins_type]['ec2']
    emr_cost = my_dict['prices'][ins_type]['emr']
    return (ec2_cost + emr_cost) *hr


def fetch_inst(client, CreatedAfter, CreatedBefore):
    id = []
    response = client.list_clusters(
        CreatedAfter=CreatedAfter,
        CreatedBefore=CreatedBefore,
        ClusterStates=[
            'TERMINATED'
        ],
    )
    # print(response)
    for inst_id in response['Clusters']:
        # print(inst_id['Id'])
        id.append(inst_id['Id'])
    # print(id)
    return id

def hour_round(sec):
    hr = 0
    if sec > 0 and sec <3600:
        hr = 1
    else:
        hr = math.ceil(sec / 3600)
    return hr

def describe_cluster(instances):
    total_cost = 0
    for inst in instances:
        cost = 0
        inst_list = []
        info = client.list_instances(ClusterId=inst)
        for list in info['Instances']:
            print(list)
            for k, v in list.items():
                # print(k, v)
                if k == 'InstanceType':
                    InstanceType = v
                if k == 'Market':
                    Market = v
                if k == 'EbsVolumes':
                    EbsVolumes = v
                if  k == 'Status':
                    date_diff = v['Timeline']['EndDateTime'] - v['Timeline']['CreationDateTime']
                    hr = hour_round(date_diff.seconds)
                    # print(type(date_diff), date_diff.seconds, hr)
                if k == 'Status':
                    status =  v
            inst_list.append(hr)
            inst_list.append(InstanceType)
            inst_list.append(Market)
            inst_list.append(EbsVolumes)
            cost += fetch_cost(hr, InstanceType)
        print('Cluster ID: {} Cost: {}'.format(inst, cost))
        total_cost += cost
    print('\nTotal EMR instance Cost: {}'.format(total_cost))
if __name__ == '__main__':
    # CreatedAfter = datetime(2018, 8, 15)
    # CreatedBefore = datetime(2018, 8, 15)
    # instance = []
    # print(platform.sys.version);
    my_dict = yaml.load(open('cost.yml'))
    client = boto3.client('emr')
    # instance = fetch_inst(client, CreatedAfter, CreatedBefore)
    # instance.append('j-2KTWWVDYMQK8O')
    instance = ['j-1EAKJFZ61421P']
    describe_cluster(instance)

