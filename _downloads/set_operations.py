"""
Set-Operations with Overlay
===========================

When working with multiple spatial datasets -- especially multiple *polygon* or
*line* datasets -- users often wish to create new shapes based on places where
those datasets overlap (or don't overlap). These manipulations are often
referred using the language of sets -- intersections, unions, and differences.
These types of operations are made available in the *geopandas* library through
the ``overlay`` function.

The basic idea is demonstrated by the graphic below but keep in mind that
overlays operate at the DataFrame level, not on individual geometries, and the
properties from both are retained. In effect, for every shape in the first
GeoDataFrame, this operation is executed against every other shape in the other
GeoDataFrame:

.. image:: ../_static/overlay_operations.png

**Source: QGIS Documentation**

(Note to users familiar with the *shapely* library: ``overlay`` can be thought
of as offering versions of the standard *shapely* set-operations that deal with
the complexities of applying set operations to two *GeoSeries*. The standard
*shapely* set-operations are also available as ``GeoSeries`` methods.)


The different Overlay operations
--------------------------------

First, we create some example data:
"""

import geopandas as gpd
from shapely.geometry import Polygon
polys1 = gpd.GeoSeries([Polygon([(0,0), (2,0), (2,2), (0,2)]),
                        Polygon([(2,2), (4,2), (4,4), (2,4)])])
polys2 = gpd.GeoSeries([Polygon([(1,1), (3,1), (3,3), (1,3)]),
                        Polygon([(3,3), (5,3), (5,5), (3,5)])])

df1 = gpd.GeoDataFrame({'geometry': polys1, 'df1':[1,2]})
df2 = gpd.GeoDataFrame({'geometry': polys2, 'df2':[1,2]})

################################################################################
# These two GeoDataFrames have some overlapping areas:

ax = df1.plot(color='red');
df2.plot(ax=ax, color='green')

################################################################################
# We illustrate the different overlay modes with the above example.
# The ``overlay`` function will determine the set of all individual geometries
# from overlaying the two input GeoDataFrames. This result covers the area covered
# by the two input GeoDataFrames, and also preserves all unique regions defined by
# the combined boundaries of the two GeoDataFrames.
#
# When using ``how='union'``, all those possible geometries are returned:

res_union = gpd.overlay(df1, df2, how='union')
res_union

ax = res_union.plot()
df1.plot(ax=ax, facecolor='none')
df2.plot(ax=ax, facecolor='none')

################################################################################
# The other ``how`` operations will return different subsets of those geometries.
# With ``how='intersection'``, it returns only those geometries that are contained
# by both GeoDataFrames:

res_intersection = gpd.overlay(df1, df2, how='intersection')
print(res_intersection)

ax = res_intersection.plot()
df1.plot(ax=ax, facecolor='none')
df2.plot(ax=ax, facecolor='none')

################################################################################
# ``how='symmetric_difference'`` is the opposite of ``'intersection'`` and returns
# the geometries that are only part of one of the GeoDataFrames but not of both:

res_symdiff = gpd.overlay(df1, df2, how='symmetric_difference')
print(res_symdiff)

ax = res_symdiff.plot()
df1.plot(ax=ax, facecolor='none');
df2.plot(ax=ax, facecolor='none');

################################################################################
# To obtain the geometries that are part of ``df1`` but are not contained in
# ``df2``, you can use ``how='difference'``:

res_difference = gpd.overlay(df1, df2, how='difference')
print(res_difference)

ax = res_difference.plot()
df1.plot(ax=ax, facecolor='none');
df2.plot(ax=ax, facecolor='none');

################################################################################
# Finally, with ``how='identity'``, the result consists of the surface of
# ``df1``, but with the geometries obtained from overlaying ``df1`` with ``df2``

res_identity = gpd.overlay(df1, df2, how='identity')
print(res_identity)

ax = res_identity.plot()
df1.plot(ax=ax, facecolor='none');
df2.plot(ax=ax, facecolor='none');

################################################################################
# Overlay Countries Example
# -------------------------
#
# First, we load the countries and cities example datasets and select :

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
capitals = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

# Select South Amarica and some columns
countries = world[world['continent'] == "South America"]
countries = countries[['geometry', 'name']]

# Project to crs that uses meters as distance measure
countries = countries.to_crs('+init=epsg:3395')
capitals = capitals.to_crs('+init=epsg:3395')

################################################################################
# To illustrate the ``overlay`` function, consider the following case in which one
# wishes to identify the "core" portion of each country -- defined as areas within
# 500km of a capital -- using a ``GeoDataFrame`` of countries and a
# ``GeoDataFrame`` of capitals.

# Look at countries:
countries.plot()

# Now buffer cities to find area within 500km.
# Check CRS -- World Mercator, units of meters.
print(capitals.crs)

# make 500km buffer
capitals['geometry']= capitals.buffer(500000)
capitals.plot()

################################################################################
# To select only the portion of countries within 500km of a capital, we specify
# the ``how`` option to be "intersect", which creates a new set of polygons where
# these two layers overlap:


country_cores = gpd.overlay(countries, capitals, how='intersection')
country_cores.plot()

################################################################################
# Changing the "how" option allows for different types of overlay operations.
# For example, if we were interested in the portions of countries *far* from
# capitals (the peripheries), we would compute the difference of the two.

country_peripheries = gpd.overlay(countries, capitals, how='difference')
country_peripheries.plot()

################################################################################
# More Examples
# -------------
#
# A larger set of examples of the use of ``overlay`` can be found
# `here <http://nbviewer.jupyter.org/github/geopandas/geopandas/blob/master/examples/overlays.ipynb>`_
