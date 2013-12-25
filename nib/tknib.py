from Tkinter import Tk, Canvas

import coords 

class TkNib(Tk):

    projections = ["merc", "xy"]
    sites = []
    __editable_sites = []
    __editable_canvas_sites = []
    radius = 2
    editable_radius = 4

    def __init__(self, options, projection="merc", *args, **kwargs):

        if projection not in self.projections:
            raise ValueError 

        if projection == "merc":
            self.proj = coords.latlong2merc
            self.unproj = coords.merc2latlong
        if projection == "xy":
            self.proj = coords.xy2xy

        map_x0 = options['y0']
        map_x1 = options['y1']
        map_y0 = options['x0']
        map_y1 = options['x1']
        [[map_x0, map_y0], [map_x1, map_y1]] = self.proj([[map_x0, map_y0],
                                                          [map_x1, map_y1]])
        delta_x = map_x1 - map_x0
        delta_y = map_y1 - map_y0
        ratio = delta_x / delta_y
        self.map_ratio = ratio
        self.map_region = (map_x0, map_x1, map_y0, map_y1)
        self.map_delta = (delta_x, delta_y)

        Tk.__init__(self, *args, **kwargs)
        self.bind("<Configure>", self.__resize)
        self.canvas = Canvas(self)
        self.canvas.place(in_=self, anchor="c", relx=.5, rely=.5)
        self.canvas.bind('<ButtonPress-1>', self.__onCanvasClick)
        self.canvas.tag_bind("selectable", '<B1-Motion>', self.__obj_select)

        self.xscale = 1.0
        self.yscale = 1.0

        self.__resize(None)

    def __obj_select(self, event):
        x, y = event.x, event.y
        r = self.radius
        x0, y0 ,x1, y1 = x-r,y-r,x+r,y+r
        widget = self.canvas.find_closest(event.x, event.y)
        self.canvas.coords(widget, x0, y0, x1, y1) 

    def __onCanvasClick(self, event):
        [[x, y]] = self.__unscale_coords([[event.x, event.y]])
        [[lat, lng]] = self.unproj([[x, y]])

    def __resize(self, event):
        # resize canvas 
        width = self.winfo_width()
        height = self.winfo_height()
        ratio = 1.0 * width / height
        if ratio < self.map_ratio:
            self.canvas.config(width=width, height=width / self.map_ratio)
        else:
            self.canvas.config(width=height * self.map_ratio, height=height)

        # rescale lines 
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        xscale = canvas_width / self.xscale
        yscale = canvas_height / self.yscale
        self.canvas.scale("lines", 0, 0, xscale, yscale)

        # rescale sites
        radius = self.radius
        for i in range(len(self.sites)):
            self.sites[i] = [ [x * xscale, y * yscale] for x, y in self.sites[i] ]
            site = [ [x - radius, y - radius, x + radius, y + radius] 
                                                    for x, y in self.sites[i] ]
            for idx2, (x0, y0, x1, y1) in enumerate(site):
                self.canvas.coords("sites%i-%i" %(i + 1, idx2), x0, y0, x1, y1) 

        # rescale editable sites
        radius = self.editable_radius
        for i, canvas_site in enumerate(self.__editable_canvas_sites):
            x, y = self.__editable_sites[i]
            self.__editable_sites[i] = [x * xscale, y * yscale] 
            x0, y0, x1, y1 = x - radius, y - radius, x + radius, y + radius 
            self.canvas.coords(canvas_site, x0, y0, x1, y1)

        self.xscale = canvas_width * 1.
        self.yscale = canvas_height * 1.

    def add_sites(self, sites, outline="red", fill="white", width=1):
        r = self.radius
        sites = self.proj(sites)
        sites = self.__scale_coords(sites)
        self.sites.append(sites)
        idx1 = len(self.sites)

        sites = [ [x-r, y-r, x+r, y+r] for x, y in sites]
        for idx2, points in enumerate(sites):
            self.canvas.create_oval(points, 
                                    outline=outline, 
                                    fill=fill, 
                                    width=width, 
                                    tags=("sites%i-%s" % (idx1, idx2),
                                          "selectable"))

    def add_polylines(self, polylines, fill="blue", width=1):
        polylines = [ self.proj(polyline) for polyline in polylines ]
        polylines = [ self.__scale_coords(polyline) for polyline in polylines]
        for polyline in polylines:
            points = [ item for innerlist in polyline for item in innerlist ]
            self.canvas.create_line(points, 
                                    fill=fill, 
                                    width=width, 
                                    tags="lines")

    def add_polygons(self, polygons, outline="black", fill="yellow", width=1):
        polygons = [ self.proj(polygon) for polygon in polygons ]
        polygons = [ self.__scale_coords(polygon) for polygon in polygons]
        for polygon in polygons:
            points = [ item for innerlist in polygon for item in innerlist ]
            self.canvas.create_polygon(points,
                                       outline=outline,
                                       fill=fill,
                                       width=width,
                                       tags="lines")

    def add_sites2edit(self, sites):
        r = self.editable_radius
        sites_lst = self.proj(sites.aslist())
        for i, [x, y] in enumerate(sites_lst):
            sites[i][0] = x
            sites[i][1] = y
        sites = self.__scale_coords(sites)
        self.__editable_sites = sites

        sites = [ [x-r, y-r, x+r, y+r] for x, y in sites]
        for points in sites:
            self.__editable_canvas_sites.append( self.canvas.create_oval(points,
                                                                         outline="red", 
                                                                         fill="green"))

    def __scale_coords(self, points):
        x0, x1, y0, y1 = self.map_region
        delta_x, delta_y = self.map_delta
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        xscale = canvas_width / delta_x
        yscale = canvas_height / delta_y
        return [ [(x - x0)*xscale, canvas_height-(y - y0)*yscale] for x, y in points ]
    def __unscale_coords(self, points):
        x0, x1, y0, y1 = self.map_region
        delta_x, delta_y = self.map_delta
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        xscale = canvas_width / delta_x
        yscale = canvas_height / delta_y
        return [ [x/xscale+x0, (canvas_height-y)/yscale+y0] for x, y in points ]

