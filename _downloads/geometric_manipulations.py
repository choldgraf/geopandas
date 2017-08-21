"""
Geometric Manipulations
=======================

*geopandas* makes available all the tools for geometric manipulations in the
`*shapely* library <http://toblerity.org/shapely/manual.html>`_.

Note that documentation for all set-theoretic tools for creating new shapes
using the relationship between two different spatial datasets -- like creating
intersections, or differences -- can be found on the
:doc:`set operations <set_operations>` page.

Constructive Methods
~~~~~~~~~~~~~~~~~~~~

.. method:: GeoSeries.buffer(distance, resolution=16)

  Returns a ``GeoSeries`` of geometries representing all points within a
  given ``distance`` of each geometric object.

.. attribute:: GeoSeries.boundary

  Returns a ``GeoSeries`` of lower dimensional objects representing
  each geometries's set-theoretic `boundary`.

.. attribute:: GeoSeries.centroid

  Returns a ``GeoSeries`` of points for each geometric centroid.

.. attribute:: GeoSeries.convex_hull

  Returns a ``GeoSeries`` of geometries representing the smallest
  convex `Polygon` containing all the points in each object unless the
  number of points in the object is less than three. For two points,
  the convex hull collapses to a `LineString`; for 1, a `Point`.

.. attribute:: GeoSeries.envelope

  Returns a ``GeoSeries`` of geometries representing the point or
  smallest rectangular polygon (with sides parallel to the coordinate
  axes) that contains each object.

.. method:: GeoSeries.simplify(tolerance, preserve_topology=True)

  Returns a ``GeoSeries`` containing a simplified representation of
  each object.

.. attribute:: GeoSeries.unary_union

  Return a geometry containing the union of all geometries in the ``GeoSeries``.


Affine transformations
~~~~~~~~~~~~~~~~~~~~~~~~

.. method:: GeoSeries.rotate(self, angle, origin='center', use_radians=False)

  Rotate the coordinates of the GeoSeries.

.. method:: GeoSeries.scale(self, xfact=1.0, yfact=1.0, zfact=1.0, origin='center')

 Scale the geometries of the GeoSeries along each (x, y, z) dimensio.

.. method:: GeoSeries.skew(self, angle, origin='center', use_radians=False)

  Shear/Skew the geometries of the GeoSeries by angles along x and y dimensions.

.. method:: GeoSeries.translate(self, angle, origin='center', use_radians=False)

  Shift the coordinates of the GeoSeries.


Examples of Geometric Manipulations
------------------------------------
"""
# sphinx_gallery_thumbnail_number = 5
import numpy as np
from shapely.geometry import Polygon
from geopandas import GeoSeries, GeoDataFrame

p1 = Polygon([(0, 0), (1, 0), (1, 1)])
p2 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
p3 = Polygon([(2, 0), (3, 0), (3, 1), (2, 1)])
g = GeoSeries([p1, p2, p3])
print(g)

g.plot()

###############################################################################
# Some geographic operations return normal pandas object.  The ``area``
# property of a ``GeoSeries`` will return a ``pandas.Series`` containing
# the area of each item in the ``GeoSeries``:

print(g.area)

###############################################################################
# Other operations return GeoPandas objects:


print(g.buffer(0.5))
g.buffer(0.5).plot()

###############################################################################
# GeoPandas objects also know how to plot themselves.  GeoPandas uses
# `descartes`_ to generate a `matplotlib`_ plot. To generate a plot
# of our GeoSeries, use:

g.plot()

###############################################################################
# GeoPandas also implements alternate constructors that can read any data
# format recognized by `fiona`_.  To read a `file containing the boroughs
# of New York City`_:

boros = GeoDataFrame.from_file('data/nybb_16a/nybb.shp')
boros.set_index('BoroCode', inplace=True)
boros = boros.sort_index()
print(boros)
boros.plot()

###############################################################################
print(boros['geometry'].convex_hull)
boros['geometry'].convex_hull.plot()

###############################################################################
# To demonstrate a more complex operation, we'll generate a
# ``GeoSeries`` containing 2000 random points:

from shapely.geometry import Point
xmin, xmax, ymin, ymax = 900000, 1080000, 120000, 280000
xc = (xmax - xmin) * np.random.random(2000) + xmin
yc = (ymax - ymin) * np.random.random(2000) + ymin
pts = GeoSeries([Point(x, y) for x, y in zip(xc, yc)])

###############################################################################
# Now draw a circle with fixed radius around each point:

circles = pts.buffer(2000)

###############################################################################
# We can collapse these circles into a single shapely MultiPolygon
# geometry with:

mp = circles.unary_union

###############################################################################
# To extract the part of this geometry contained in each borough, we can
# just use:

holes = boros['geometry'].intersection(mp)
holes.plot()

###############################################################################
# and to get the area outside of the holes:

boros_with_holes = boros['geometry'].difference(mp)
boros_with_holes.plot()

###############################################################################
# Note that this can be simplified a bit, since ``geometry`` is
# available as an attribute on a ``GeoDataFrame``, and the
# ``intersection`` and ``difference`` methods are implemented with the
# "&" and "-" operators, respectively.  For example, the latter could
# have been expressed simply as ``boros.geometry - mp``.
#
# It's easy to do things like calculate the fractional area in each
# borough that are in the holes:

print(holes.area / boros.geometry.area)

###############################################################################
# .. _Descartes: https://pypi.python.org/pypi/descartes
# .. _matplotlib: http://matplotlib.org
# .. _fiona: http://toblerity.github.io/fiona
# .. _geopy: https://github.com/geopy/geopy
# .. _geo_interface: https://gist.github.com/sgillies/2217756
# .. _file containing the boroughs of New York City: http://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nybb_16a.zip
