import boto3
import ConfigParser
import os

conf_file = os.path.expanduser('~/.aws/credentials')

config = ConfigParser.ConfigParser()

config.read(conf_file)
aws_secret_access_key = config.get("default", "aws_secret_access_key")
aws_access_key_id = config.get("default", "aws_access_key_id")

region = "us-east-1"

client = boto3.client('ec2', region_name=region)

response = client.describe_snapshots(DryRun=False,
                                     MaxResults=1000)
i=0
while True:
    nextToken = response['NextToken']
    print nextToken
    for snapshot in response['Snapshots']:
        print "Snapshot ID: " + snapshot['SnapshotId']
        print "Volume ID: " + snapshot['VolumeId']
        print "State : " + snapshot['State']
        print "Volume Size :", snapshot['VolumeSize']
        print ""
        i+=1
    response = client.describe_snapshots(DryRun=False,
                                     MaxResults=1000,NextToken=nextToken)
    if "NextToken" not in response:
        break
print "total snapshots: ", i
