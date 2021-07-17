from future import print_function
import boto3
import sys
s3client = boto3.client('s3')

#input format
#python3 [scriptname] 2017-11-15 2017-11-16 2017-11-17 2017-11-18

for i in sys.argv[1:]:
    target_bucket = "xx-comlinkdata-com"
    target_prefix = "mw01/date=" + i
    target_account_canonical_id = "xx"

    print("input is:", target_bucket, target_prefix)
    result = s3client.list_objects_v2(Bucket=target_bucket, Prefix=target_prefix)

    while True:
        objects = [object for object in result['Contents']]
        for object in objects:
            try:
                s3client.put_object_acl(ACL='bucket-owner-full-control', Bucket=target_bucket, Key=object['Key'])
                print(object['Key'])
            except:
                print("Error: permissions for object {} could not be set.".format(object['Key']))

        if 'NextContinuationToken' in result:
            result = s3client.list_objects_v2(Bucket=target_bucket, Prefix=target_prefix,
                                              ContinuationToken=result['NextContinuationToken'])
        else:
            break

