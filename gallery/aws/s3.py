import logging
import boto3
import os
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def put_object(bucket_name, key, value):
    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, ContentDisposition='inline', ContentType='image/png', Key=key, Body=value)
    except ClientError as e:
        logging.error(e)
        return False
    return True

#def download_object(bucket, filepath, download_to):
#    try:
#        if not os.path.isdir(download_to):
#            os.makedirs(download_to)
#        s3 = boto3.resource('s3')
#        response = s3.meta.client.download_file(bucket, filepath, download_to +  "/" +  filepath.split("/")[1])
#    except ClientError as e:
#        logging.error(e)
#        return None
#    return response

def get_object(bucket_name, key):
    try:
        s3_client = boto3.client('s3')
        result = s3_client.get_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        logging.error(e)
        return None
    return result

def delete_object(bucket_name, key):
    try:
        s3_client = boto3.client('s3')
        response = s3_client.delete_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        logging.error(e)
        return None
    return response

#def main():
#    #create_bucket('edu.au.cc.image-gallery','us-east-2')
#    put_object('edu.au.cc.image-gallery', 'banana', 'green')
#    print(get_object('edu.au.cc.image-gallery', 'banana')['Body'].read())

#if __name__ == '__main__':
#    main()

