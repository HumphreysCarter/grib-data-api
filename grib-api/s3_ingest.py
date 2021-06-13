import boto3
import botocore
from botocore.client import Config
from pathlib import Path
from datetime import datetime

# Connect to AWS s3 resource
s3 = boto3.resource('s3', config=Config(signature_version=botocore.UNSIGNED, user_agent_extra='Resource'))
bucket = s3.Bucket('noaa-gfs-bdp-pds')


basePath = '/home/cjh/workspace/grib-model-plots/data/'

# Build request
vtime   = datetime(2021, 6, 10, 12, 0)
request = f'gfs.{vtime:%Y%m%d}/{vtime:%H}/atmos/gfs.t{vtime:%H}z.pgrb2.0p25.f'

# Get files in S3 bucket based on request
files = [file.key for file in bucket.objects.filter(Prefix=request)]
files = files[:10]

# Build path from request
path = f'{basePath}/{request[:request.rfind("/")]}'
Path(path).mkdir(parents=True, exist_ok=True)
print(path)

# Get files
for bucket_file in files:
    # Donwload file if it doesn't already exist
    filepath = f'{basePath}/{bucket_file}'
    if Path(filepath).exists() == True:
        print(f'Downloading {bucket_file} from AWS Bucket ...')
        bucket.download_file(bucket_file, filepath)
