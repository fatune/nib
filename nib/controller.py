

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

        self._editable_del_idx = [-1] # index of a site i delete. make as list couse it acts like a pointer in C
        self.viewEditableSites = ViewEditableSites(self.view.canvas, self.model.Sites, self._editable_del_idx)
        self.model.CanvasScale.addCallback(self.viewEditableSites.scale)
        self.model.Sites.addCallback(self.viewEditableSites.showSites)

        self.viewPolylines = ViewPolylines(self.view.canvas)
        self.model.CanvasScale.addCallback(self.viewPolylines.scale)
        self.model.Polylines.addCallback(self.viewPolylines.showPolylines)

        self.viewPolygons = ViewPolygons(self.view.canvas)
        self.model.CanvasScale.addCallback(self.viewPolygons.scale)
        self.model.Polygons.addCallback(self.viewPolygons.showPolygons)

        self.map_model.editable_sites_lst.addCallback(self.editable_sites_lst2editable_site)
        self.model.Sites.addCallback(self.editable_sites_lst2editable_site)

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
            lines = "\n".join(self.sites2edit.unparse())
            f = open("%s" % self.sites2edit_name, 'w')
            f.writelines(lines)
            f.close()
        if event.keysym == "l":
            for l in self.sites2edit.unparse(): print l

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

    def add_sites2edit(self, sites, name):
        self.sites2edit_name = name
        self.sites2edit = sites

        canvas_width, canvas_height = self.view.get_canvas_size()
        if len(sites.aslist())>0:
            sites_lst = self.map_model.doProj(sites.aslist())
            sites_lst = self.map_model.scale_coords(sites_lst, canvas_width, canvas_height)
        else:
            sites_lst = []

        self.map_model.add_editable_sites_lst(sites_lst)
        for x, y in sites_lst:
            self.viewEditableSites.addSite()
            self.model.addSite(x, y)

    def editable_sites_lst2editable_site(self, SiteLst):
        canvas_width, canvas_height = self.view.get_canvas_size()

        if not self._editable_del_idx[0] == -1:
            self.sites2edit.remove(self._editable_del_idx[0])
            self._editable_del_idx[0] = -1

        for i, (x, y) in enumerate(SiteLst):
            [[x, y]] = self.map_model.unscale_coords([[x, y]], canvas_width, canvas_height)
            [[x, y]] = self.map_model.doUnproj([[x,y]])
            try:
                self.sites2edit[i][0] = x
                self.sites2edit[i][1] = y
            except IndexError:
                self.sites2edit.append([x, y])
