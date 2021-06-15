import xarray as xr

class Data:

    def __init__(self, path, typeOfLevel=None, stepType=None):
        """
        Read in GRIB file into xarray dataset
        """
        # Create empty dictionary for key filters
        keys = {}

        # Set type of level
        self.typeOfLevel = typeOfLevel
        if typeOfLevel != None:
            keys['typeOfLevel'] = typeOfLevel

        # Set step type
        self.stepType = stepType
        if stepType != None:
            keys['stepType'] = stepType

        # Read in dataset as xarray dataset with cfgrib engine
        self.dataset = xr.open_dataset(path, filter_by_keys=keys, engine='cfgrib')

    def get_grid_data(self, var, extent=None, level=None):
        """
        Returns grid data for plan view
        """
        # Get only desired variables
        ds = self.dataset[var]

        # Get grid points with in extent
        if extent != None:
            minLon, maxLon, minLat, maxLat = extent
            ds = ds.sel(longitude=slice(minLon, maxLon), latitude=slice(maxLat, minLat))

        # Get values at level, if specified
        if level != None:
            args = {self.typeOfLevel:level}
            ds = ds.sel(**args)

        return ds

    def get_profile(self, var, lat, lon, bottom=None, top=None, method='nearest'):
        """
        Returns a profile at a given latitude and longitude point
        """
        # Get only desired variables
        ds = self.dataset[var]

        # Get values at grid point for the lat/lon pair
        ds = ds.sel(latitude=lat, longitude=lon, method=method)

        # Get values for desired layer, if bottom or top are set
        if bottom != None or top != None:
            args = {self.typeOfLevel:slice(bottom, top)}
            ds = ds.sel(**args)

        return ds

    def get_point_value(self, var, lat, lon, level=None, method='nearest'):
        """
        Returns a point value for given latitude, longitude, and level (if not surface)
        """
        # Get only desired variables
        ds = self.dataset[var]

        # Get values at grid point for the lat/lon pair
        ds = ds.sel(latitude=lat, longitude=lon, method=method)

        # Get values at level, if specified
        if level != None:
            args = {self.typeOfLevel:level}
            ds = ds.sel(**args)

        return ds
