#!/usr/bin/env python
import boto3
import json
import urllib3

ec2 = boto3.resource('ec2')
ec2client = boto3.client('ec2')
splunk_server = 'foobar'
ingest_token = 'adfsasdfdsafdafssda'
headers = {'Authorization': 'Splunk  ' + ingest_token, 'Content-Type': 'application/json'}
url = "https://"+splunk_server+":8088/services/collector"

#-----Define Lambda function-----#
def lambda_handler(event, context):

#-----Check& filter Instances which  Instance State is running-----#
    instances = ec2client.describe_instances(
        Filters=[{
            'Name': 'instance-state-name',
            'Values': ['pending', 'running']
        }]
        )

#-----Define dictionary to store Tag Key & value------#
    #instance_ids = []
    instance_ids = {}


#-----Store Key & Value of Instance ------#
    for reservation in instances['Reservations']:
        x=0
        for instance in reservation['Instances']:
            #instance_ids.append(instance['InstanceId'])
            instance_ids.update({"instance_id": instance['InstanceId']})
            for tag in instance['Tags']:

                mykey = (tag['Key'])
                myvalue = (tag['Value'])
                
                instance_ids[mykey] = myvalue
                
    # Create request
    print (json.dumps(instance_ids))
    http = urllib3.PoolManager()

    response = http.request(
        'POST',
        url,
        body=json.dumps(instance_ids).encode('utf-8'),
        headers=headers,
        verify=False
        )

    try:
        return json.loads(response.data.decode('utf-8'))
    except:
        return {
            'errors': [
                {
                    'status': response.status,
                    'message': 'Failed to contact endpoint. Is "{}" the correct URL?'.format(self.url)
                }
            ]
        } 

    return json.dumps(instance_ids)
                
