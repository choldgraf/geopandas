"""
Geocoding
=========

Geocoding with geopandas.

[TO BE COMPLETED]

.. note::
    This module requires `geopy`_.  Please consult the Terms of Service for the
    chosen provider.

.. _geopy: https://github.com/geopy/geopy
"""
import geopandas as gpd
import matplotlib.pyplot as plt

cities = ['San Francisco', 'New York City', 'Paris', 'Sydney', 'Mumbai']
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
geocoded_cities = gpd.tools.geocode(cities)

fig, ax = plt.subplots()
world.plot(ax=ax)
geocoded_cities.plot(ax=ax, markersize=150, color='r')

plt.show()
