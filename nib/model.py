from observable import Observable

import coords

class Model:
    def __init__(self, MapRegion):
        self.Sites = Observable([])
        self.CanvasScale = Observable([1, 1])
        self.MapRegion = Observable(MapRegion)
        self.Polylines = Observable([])
        self.Polygons = Observable([])

    def addSite(self, x, y):
        self.Sites.set(self.Sites.get() + [[x,y]])

    def removeSite(self, x, y):
        idx = self.Sites.get().index([x,y])
        self.Sites.get().pop(idx)
        self.Sites.docallbacks()

    def resize(self, xscale, yscale):
        self.CanvasScale.set([xscale, yscale])

    def add_polylines(self, polylines):
        self.Polylines.set(self.Polylines.get() + polylines)
    def add_polygons(self, polygons):
        self.Polygons.set(self.Polygons.get() + polygons)

class MapModel:

    projections = ["merc", "xy"]

    def __init__(self, projection, options):
        if projection not in self.projections:
            raise ValueError 

        if projection == "merc":
            self.doProj = coords.latlong2merc
            self.doUnproj = coords.merc2latlong
        if projection == "xy":
            self.doProj = coords.xy2xy

        self.options = options

        map_x0 = options['y0']
        map_x1 = options['y1']
        map_y0 = options['x0']
        map_y1 = options['x1']
        self.map_region_unproj = [map_x0, map_x1, map_y0, map_y1]

        [[map_x0, map_y0], [map_x1, map_y1]] = self.doProj([[map_x0, map_y0],
                                                          [map_x1, map_y1]])

        self.map_region_proj = [map_x0, map_x1, map_y0, map_y1]

        delta_x = map_x1 - map_x0
        delta_y = map_y1 - map_y0
        ratio = delta_x / delta_y
        self.map_ratio = ratio
        self.map_delta = (delta_x, delta_y)

        self.editable_sites_lst = Observable(None)

    def scale_coords(self, points, canvas_width, canvas_height):
        x0, x1, y0, y1 = self.map_region_proj
        delta_x, delta_y = self.map_delta

        xscale = canvas_width / delta_x
        yscale = canvas_height / delta_y
        #print x0, x1, y0, y1
        return [ [(x - x0)*xscale, canvas_height-(y - y0)*yscale] for x, y in points ]

    def unscale_coords(self, points, canvas_width, canvas_height):
        x0, x1, y0, y1 = self.map_region_proj
        delta_x, delta_y = self.map_delta

        xscale = canvas_width / delta_x
        yscale = canvas_height / delta_y
        return [ [x/xscale+x0, (canvas_height-y)/yscale+y0] for x, y in points ]



