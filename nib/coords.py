from numpy import log, tan, pi, array, radians, degrees, arctan, exp


def latlong2merc(points):
    """
    Project data to spherical Mercator.
    x = LAT
    y = ln[ tan( pi/4 + LON/2) ]
    stackoverflow.com/questions/14329691/covert-latitude-longitude-point-to-a-pixels-x-y-on-mercator-projection

    """
    points = array(points,dtype=float)
    points[:, 1] = degrees(log(tan(radians(points[:, 1] / 2) + pi / 4)))
    return points.tolist()

def merc2latlong(points):
    points = array(points)
    points[:, 1] = degrees( 2 * arctan(exp(radians(points[:, 1]))) - pi / 2 )
    return points.tolist()

def xy2xy(points):
    return points


def normalize_coords(points, x0, x1, y0, y1):
    delta_x = x1 - x0
    delta_y = y1 - y0
    return [ [(y - y0) / delta_y, 1 - (x - x0) / delta_x] for y, x in points ]

def scale(points, xscale, yscale):
    return [ [y * yscale, x * xscale] for y, x in points ]
