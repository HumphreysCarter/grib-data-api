import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.colors as col
import scipy.ndimage as ndimage
from metpy.plots import USCOUNTIES

class GeoMap:

	def __init__(self, bbox=[-125, -65, 20, 55], width=14, height=12):
		"""
		"""
		# Set map projection
		central_lon = bbox[0]-((bbox[0]-bbox[1])/2.0)
		central_lat = bbox[2]+((bbox[3]-bbox[2])/2.0)
		mapcrs = ccrs.LambertConformal(central_longitude=central_lon, central_latitude=central_lat, standard_parallels=(30, 60))
	
		# Set projection of the data
		self.datacrs = ccrs.PlateCarree()
		
		# Start figure and limit the graphical area extent
		self.fig = plt.figure(1, figsize=(width, height))
		self.ax = plt.subplot(111, projection=mapcrs)
		self.ax.set_extent(bbox, ccrs.PlateCarree())
	
	def add_geographic_features(self):
		"""
		"""
		self.ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='black', linewidth=1.0)
		self.ax.add_feature(USCOUNTIES.with_scale('5m'), edgecolor='black', linewidth=0.1)
	
	def plot_fill_data(self, lons, lats, data, vmin=None, vmax=None, cmap=None, norm=None, colorbar=True, cbar_label=None, smooth=False, smooth_sigma=3, smooth_order=0):
		"""
		"""
		# Smooth data with gaussian filter
		if smooth:
			ndimage.gaussian_filter(data, sigma=smooth_sigma, order=smooth_order)
			
		if vmin != None and vmax != None:
			norm = col.Normalize(vmin=vmin, vmax=vmax)
		
		# Plot fill data
		cf = self.ax.pcolormesh(lons, lats, data, cmap=cmap, norm=norm, transform=self.datacrs)
		
		# Plot color bar
		if colorbar:
			cb = plt.colorbar(cf, orientation='horizontal', pad=0.02, aspect=50)
			cb.set_label(cbar_label)
			
	def plot_contour_data(self, lons, lats, data, vmin, vmax, vint=1, colors='k', width=2, label_contour=True):
		"""
		"""
		# Generate lebel interval
		clev = np.arange(vmin, vmax, vint)
		
		# Plot contours
		cs = self.ax.contour(lons, lats, data, clev, colors=colors, linewidths=width, transform=self.datacrs)
		
		# Plot contour labels
		if label_contour:
			plt.clabel(cs, fontsize=10, inline=1, inline_spacing=10, fmt='%i', rightside_up=True, use_clabeltext=True)
	
	def export(self, path, dpi=100):
		"""
		"""
		plt.savefig(path, bbox_inches='tight', dpi=dpi)