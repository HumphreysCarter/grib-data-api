# GRIB Data API
A collection of scripts for downloading and interacting with model GRIB data.

## GRIB2 Model Data via AWS S3

### GFS
https://registry.opendata.aws/noaa-gfs-bdp-pds/

s3://noaa-gfs-bdp-pds

### GEFS
https://registry.opendata.aws/noaa-gefs/

s3://noaa-gefs

### HRRR
https://registry.opendata.aws/noaa-hrrr-pds/

s3://noaa-hrrr-pds

### RAP
https://registry.opendata.aws/noaa-rap/

s3://noaa-rap-pds

### NBM
https://registry.opendata.aws/noaa-nbm/

s3://noaa-nbm-grib2-pds

## GRIB2 Model Data via NCEP FTP

ftp.ncep.noaa.gov, ftpprd.ncep.noaa.gov,
tgftp.nws.noaa.gov

### HRRR
Res: 3km

Cycles: 00Z, 06Z, 12Z, 18Z

Steps: Hourly, 00-48 HRS

Product description:
https://www.nco.ncep.noaa.gov/pmb/products/hrrr/


Data path:
ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/hrrr/prod/hrrr.20210209/conus/

### NAM NEST
Res: 3km

Cycles: 00Z, 06Z, 12Z, 18Z

Steps: Hourly, 00-60 HRS

Product description: https://www.nco.ncep.noaa.gov/pmb/products/nam/

Data path: ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/nam/prod/nam.20210209/nam.t00z.conusnest.hiresf12.tm00.grib2

### NAM
Res: 12km

Cycles: 00Z, 06Z, 12Z, 18Z

Steps: 3-Hourly, 00-84 HRS

Product description: https://www.nco.ncep.noaa.gov/pmb/products/nam/

Data path:
ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/nam/prod/nam.20210209/nam.t00z.awphys12.tm00.grib2

### GFS
Res: 0.25 deg

Cycles: 00Z, 06Z, 12Z, 18Z

Steps: 3-Hourly, 000-384 HRS

Product description: https://www.nco.ncep.noaa.gov/pmb/products/gfs/

Data path: ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20210209/00/gfs.t00z.pgrb2.0p25.f000
