import boto3
import ConfigParser
import os
import json
import time

maxResults = '50000'
page = '1000'
ownerId = boto3.client('iam').get_user()['User']['Arn'].split(':')[4]
region = "us-east-1"

conf_file = os.path.expanduser('~/.aws/credentials')
config = ConfigParser.ConfigParser()
config.read(conf_file)
aws_secret_access_key = config.get("default", "aws_secret_access_key")
aws_access_key_id = config.get("default", "aws_access_key_id")

client = boto3.client('ec2', region_name=region)
paginator = client.get_paginator('describe_snapshots')
origin_time = time.time()
response_iterator = paginator.paginate(DryRun=False,OwnerIds=[ownerId],
                                      PaginationConfig={'MaxItems': maxResults, 'PageSize': page})
#add this back later: OwnerIds=[ownerId]
stopwatch = time.time() - origin_time
print "time for first response:", stopwatch

j = 0
for responseIndex,line in enumerate(response_iterator):
  print line['ResponseMetadata']
  for snap in line['Snapshots']:
    print json.dumps(snap,sort_keys=True, indent=2, default=str)
    j+=1
  print "snapshots in paginated response:", j
  if j >= maxResults:
    break

totSnapTime = time.time() - origin_time
print "total time to process snapshots:", totSnapTime
print "total snapshots: ", j
