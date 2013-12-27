from model import Model, MapModel

from tkGui.view import View
from tkGui.view_polygons import ViewPolygons
from tkGui.view_polylines import ViewPolylines
from tkGui.view_editable_sites import ViewEditableSites

class Controller:
    MapRegion = [0,0,10,10]
    def __init__(self, root, options, projection="merc"):
        self.options = options
        self.model = Model(self.MapRegion)
        self.map_model = MapModel(projection, options)

        self.view = View(root, self.model.CanvasScale)
        self.view.canvas.bind('<ButtonPress-1>', self.Click)
        self.view.bind('<Key>', self.KeyPress)

        self.viewEditableSites = ViewEditableSites(self.view.canvas, self.model.Sites)
        self.model.CanvasScale.addCallback(self.viewEditableSites.scale)
        self.model.Sites.addCallback(self.viewEditableSites.showSites)

        self.viewPolylines = ViewPolylines(self.view.canvas)
        self.model.CanvasScale.addCallback(self.viewPolylines.scale)
        self.model.Polylines.addCallback(self.viewPolylines.showPolylines)

        self.viewPolygons = ViewPolygons(self.view.canvas)
        self.model.CanvasScale.addCallback(self.viewPolygons.scale)
        self.model.Polygons.addCallback(self.viewPolygons.showPolygons)

        self.map_model.editable_sites_lst.addCallback(self.SiteLst2EditableSite)


    def Click(self, event):
        x, y = event.x, event.y

        try:
            self.viewEditableSites.selectSite(x, y)
        except TypeError:
            self.viewEditableSites.unselect()
            self.viewEditableSites.addSite()
            self.model.addSite(x, y)

    def KeyPress(self, event):
        if event.keysym == "d":
            self.viewEditableSites.removeSite()
        if event.keysym == "p":
            print self.editable_sites.unparse()

    def add_polylines(self, polylines):
        canvas_width, canvas_height = self.view.get_canvas_size()
        polylines = [ self.map_model.doProj(polyline) for polyline in polylines ]
        polylines = [ self.map_model.scale_coords(polyline, canvas_width, canvas_height)
                                                               for polyline in polylines ]
        self.model.add_polylines(polylines)

    def add_polygons(self, polygons):
        canvas_width, canvas_height = self.view.get_canvas_size()
        polygons = [ self.map_model.doProj(polygon) for polygon in polygons ]
        polygons = [ self.map_model.scale_coords(polygon, canvas_width, canvas_height)
                                                               for polygon in polygons ]
        self.model.add_polygons(polygons)

    def add_sites2edit(self, sites):
        canvas_width, canvas_height = self.view.get_canvas_size()
        self.editable_sites = sites
        sites_lst = self.map_model.doProj(sites.aslist())
        sites_lst = self.map_model.scale_coords(sites_lst, canvas_width, canvas_height)
        print sites_lst
        #self.viewEditableSites.addEditableSites(sites_lst)
        print sites_lst
        for x, y in sites_lst:
            #self.viewEditableSites.unselect()
            self.viewEditableSites.addSite()
            self.model.addSite(x, y)

    def SiteLst2EditableSite(self, SiteLst):
        print "ss"
        for i, item in enumerate(SiteLst):
            # unproj item
            self.editable_sites[i] = item