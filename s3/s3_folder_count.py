import boto3
s3client = boto3.client('s3')

response = s3client.head_object(Bucket='com.xx.rtb.avro.device.id.prod',Key='20180101/GB/00094c7b-fb73-423e-a402-f0348a2eb109.avro')

print(response['ResponseMetadata']['HTTPHeaders']['x-amz-restore'])
print(response['ResponseMetadata']['HTTPHeaders']['x-amz-storage-class'])
