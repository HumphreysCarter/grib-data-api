import ftplib
from pathlib import Path
from datetime import datetime

class Ingest:

    def __init__(self, date, downloadPath, filter=None, overwrite=False):
        """
        Initializes ingest from ECMWF WMO Essential FTP server.
        """
        # Set instance variables
        self.basePath = downloadPath
        self.vtime = date
        self.filter = filter
        self.overwrite = overwrite

    def start(self):
        """
        Starts ingest from FTP server
        """
        # Login to FTP server with WMO essential credentials
        self.ftp = ftplib.FTP('dissemination.ecmwf.int')
        self.ftp.login('wmo', 'essential')

        # Navigate to directory for desired run
        self.ftp.cwd(f'/{self.vtime:%Y%m%d%H%M%S}/')

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
        path = f'{self.basePath}/ecmwf.{self.vtime:%Y%m%d}/{self.vtime:%H}/'
        Path(path).mkdir(parents=True, exist_ok=True)

        # Get files
        for file in self.files:

            # Check if file exists already
            filepath = f'{path}/{file}'
            if self.overwrite == True or Path(filepath).exists() == False:

                # Download file over FTP
                print(f'Downloading {file} from ECMWF FTP Server ...')
                self.ftp.retrbinary("RETR " + file, open(filepath, 'wb').write)

                # Add to file list
                self.file_list.append(filepath)
