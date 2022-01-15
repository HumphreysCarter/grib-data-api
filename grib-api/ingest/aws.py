import boto3
import botocore
from botocore.client import Config
from pathlib import Path
from datetime import datetime

class Ingest:

    def __init__(self, model, date, downloadPath, filter=None, include_idx=True, overwrite=False):
        """
        Initializes ingest from an AWS S3 bucket for a given bucket and path, to a specified path.
        """
        # Set instance variables
        self.basePath = downloadPath
        self.vtime = date
        self.bucketName = self.get_bucket_name(model)
        self.filter = filter
        self.idx = include_idx
        self.overwrite = overwrite

    def get_bucket_name(self, model):
        """
        Gets an AWS S3 bucket name for a given model
        """
        key = {'GFS':'noaa-gfs-bdp-pds', 'GEFS':'noaa-gefs-pds', 'HRRR':'noaa-hrrr-bdp-pds', 'NBM':'noaa-nbm-grib2-pds'}

        try:
            return key[model.upper()]
        except:
             raise KeyError('Input model is unsupported. Supported models are GFS, GEFS, HRRR, and NBM.')

    def start(self):
        """
        Starts the ingest of files from the AWS S3 bucket
        """
        # Make connection to S3
        self.__connect_to_s3()

        # Make the request string
        self.__build_request()

        # Get files in request
        self.__get_s3_bucket_listing()

        # Remove .idx files if desired
        if self.idx == False:
            self.files = [file for file in self.files if '.idx' not in file]

        # Filter based on desired files
        self.__filter_files()

        # Download all files within the s3 bucket
        self.__download_s3_bucket()

        return self.file_list

    def __connect_to_s3(self):
        """
        Makes a conection to AWS S3 bucket using boto3 package
        """
        # Connect to AWS s3 resource
        s3 = boto3.resource('s3', config=Config(signature_version=botocore.UNSIGNED, user_agent_extra='Resource'))
        self.bucket = s3.Bucket(self.bucketName)

    def __build_request(self):
        """
        Generates an S3 request based on date and time
        """
        # Build request for noaa-gfs-bdp-pds
        if self.bucketName == 'noaa-gfs-bdp-pds':
            self.request = f'gfs.{self.vtime:%Y%m%d}/{self.vtime:%H}/atmos/gfs.t{self.vtime:%H}z.'

        # Build request for noaa-hrrr-pds
        elif self.bucketName == 'noaa-gefs-pds':
            self.request = f'gefs.{self.vtime:%Y%m%d}/{self.vtime:%H}/atmos/'

        # Build request for noaa-hrrr-pds
        elif self.bucketName == 'noaa-hrrr-bdp-pds':
            self.request = f'hrrr.{self.vtime:%Y%m%d}/conus/hrrr.t{self.vtime:%H}z.'

        # Build request for noaa-hrrr-pds
        elif self.bucketName == 'noaa-nbm-grib2-pds':
            self.request = f'blend.{self.vtime:%Y%m%d}/{self.vtime:%H}/core/blend.t{self.vtime:%H}z.'

    def __get_s3_bucket_listing(self):
        """
        Gets file listing of S3 bucket for a given request
        """
        # Get files in S3 bucket based on request
        self.files = [file.key for file in self.bucket.objects.filter(Prefix=self.request)]

    def __filter_files(self):
        """
        Filters files return from S3 bucket request based on keywords
        """
        # Convert single string filter to single item list
        if isinstance(self.filter, str):
            self.filter = [self.filter]

        # Check that each file contain a keyword
        updatedList = []
        for file in self.files:
            if [keyword for keyword in self.filter if(keyword in file)]:
                updatedList.append(file)

        # Update file list
        self.files = updatedList

    def __download_s3_bucket(self):
        """
        Downloads file listing from S3 bucket to local path
        """
        # Create empty list to store local paths
        self.file_list = []

        # Build path from request
        path = f'{self.basePath}/{self.files[0][:self.files[0].rfind("/")]}'
        Path(path).mkdir(parents=True, exist_ok=True)

        # Get files
        for bucket_file in self.files:

            # Check if file exists already
            filepath = f'{self.basePath}/{bucket_file}'
            if self.overwrite == True or Path(filepath).exists() == False:

                # Download the file
                print(f'Downloading {bucket_file} from AWS Bucket ...')
                self.bucket.download_file(bucket_file, filepath)

                # Add to file list
                self.file_list.append(filepath)
