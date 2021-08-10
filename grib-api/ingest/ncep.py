import ftplib
from datetime import datetime, timedelta

class Ingest:

    def __init__(self, model, date, downloadPath, server='ftpprd.ncep.noaa.gov', filter=None, include_idx=True, overwrite=False):
        """
        Initializes ingest from an AWS S3 bucket for a given bucket and path, to a specified path.
        """
        # Set instance variables
        self.basePath = downloadPath
        self.vtime = date
        self.model = model
        self.server = server
        self.serverPath = self.get_server_path()
        self.filter = filter
        self.idx = include_idx
        self.overwrite = overwrite

    def get_server_path(self):
        """
        Gets an NCEP FTP path name for a given model
        """
        key = {'GFS':f'/pub/data/nccf/com/gfs/prod/gfs.{self.vtime:%Y%m%d}/{self.vtime:%H}/',
               'NAM':f'/pub/data/nccf/com/nam/prod/nam.{self.vtime:%Y%m%d}/',
               'HRRR':f'/pub/data/nccf/com/hrrr/prod/hrrr.{self.vtime:%Y%m%d}/conus/'}

        try:
            return key[self.model.upper()]
        except:
             raise KeyError('Input model is unsupported. Supported models are GFS, NAM, and HRRR.')

    def start(self):
        """
        Starts ingest from FTP server
        """
        # Login to FTP server with anonymous credentials
        self.ftp = ftplib.FTP(self.server)
        self.ftp.login('anonymous', 'password')

        # Navigate to directory for desired run
        self.ftp.cwd(self.serverPath)

        # Get list of files
        self.files = self.ftp.nlst()

        # Filter based on file filter
        self.filterList()

        # Download files
        self.downloadFiles()

        # Close the FTP connection
        self.ftp.close()

    def filterList(self):
        """
        Filters file list based on keywords
        """
        # Convert single string filter to single item list
        if isinstance(self.filter, str):
            self.filter = [self.filter]

        # Check that each keyword is in each file
        for keyword in self.filter:
            self.files = [file for file in self.files if keyword in file]

    def downloadFiles(self):
        """
        Downloads files from the FTP server
        """
        # Create empty list to store local paths
        self.file_list = []

        # Build file path
        path = f'{self.basePath}/{self.model}.{self.vtime:%Y%m%d}/{self.vtime:%H}/'
        Path(path).mkdir(parents=True, exist_ok=True)

        # Get files
        for file in self.files:

            # Check if file exists already
            filepath = f'{path}/{file}'
            if self.overwrite == True or Path(filepath).exists() == False:

                # Download file over FTP
                print(f'Downloading {file} from NCEP FTP Server ...')
                self.ftp.retrbinary("RETR " + file, open(filepath, 'wb').write)

                # Add to file list
                self.file_list.append(filepath)
