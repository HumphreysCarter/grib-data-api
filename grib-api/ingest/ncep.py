
import ftplib
from datetime import datetime, timedelta

# Get current cycle time
rtime = datetime(2021, 2, 19, 0)

# Servers
nomads = 'ftp.ncep.noaa.gov'
ftpprd = 'ftpprd.ncep.noaa.gov'

# Model Paths
hrrr = f'/pub/data/nccf/com/hrrr/prod/hrrr.{rtime:%Y%m%d}/conus/'
nam  = f'/pub/data/nccf/com/nam/prod/nam.{rtime:%Y%m%d}/'
gfs  = f'/pub/data/nccf/com/gfs/prod/gfs.{rtime:%Y%m%d}/{rtime:%H}/'

# File Filter
filter = f'hrrr.t{rtime:%H}z.wrfprsf'

# Login to FTP server with anonymous credentials
ftp = ftplib.FTP(ftpprd)
ftp.login('anonymous', 'password')

# Navigate to model directory
ftp.cwd(hrrr)

#

for file in ftp.nlst():
    if filter in file and 'idx' not in file:
        ftp.retrbinary("RETR " + file, open(f'data/{file}', 'wb').write)
        print(file)
        break


ftp.quit()
