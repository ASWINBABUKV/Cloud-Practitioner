
# AWS S3 - Simple Storage Service 

S3 solves the problem of storage. For example, if we use a mobile phone, we run out of memory. S3 lets you store and retrieve any amount of data, at any time, from anywhere on the web.

Benefits and Advantages
- Available and Durable -> S3 is designed for 99.999999999% (11 nines) durability, meaning that your data is highly resilient to failures.
- Scalability
- Security
- Cost Effective
- Performance

1. Buckets: Act like a folder where you can store files (called objects)
2. Objects: Files that you store in S3. It can be videos, images, text files, backups, etc. Objects in S3 are globally accessible using a HTTPS protocol.
3. Access Control: S3 provides various mechanisms to control access to your data, including bucket policies, access control lists (ACLs), and Identity and Access Management (IAM) policies.




## Creating a Flask Application with AWS S3 Integration

1. Creating S3 Buckets

- Go to the AWS Management Console and open the Amazon S3 service.
- Click on "Create bucket".
- Enter a globally unique name for your bucket, select the region, and click "Create".
- S3 buckets are scoped in a region but the content is accessible globally.
- Try uploading anything from the device using the <upload> option.

2. Integrate the application with S3 using the access key and bucket name

- Modify the following code and add it to the Python file (app1.py)
```bash
# Configure Boto3 S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id='<access_key_id',
    aws_secret_access_key='<access_key_password>'
)
bucket_name = '<bucket_name>'
```

3. Run the application using the command 
```bash
python app1.py
```



