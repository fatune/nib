class ViewEditableSites:

    settings = {"site_fill" : "blue" , "tolerance" : 15 ,
                "site_radius" : 3 ,
                "selected_fill" : "red"}
    canvas_sites = []

    def __init__(self, canvas, sites):
        self.sites = sites
        self.canvas = canvas
        self.canvas.tag_bind("site_", '<B1-Motion>', self.Move)

    def returnWidget(self, x, y):
        tolerance = self.settings['tolerance']
        widgets = self.canvas.find_enclosed(x+tolerance, y+tolerance, x-tolerance, y-tolerance)

        widget = None
        for widget in widgets:
            if 'site_' in self.canvas.itemcget(widget, 'tags'):
                return widget
        return widget 

    def selectSite(self, x, y):
        fill = self.settings['site_fill']
        self.canvas.itemconfig("selected", fill = fill)
        self.canvas.dtag("site_", "selected") 
        widget = self.returnWidget(x, y)
        if not widget:
            raise TypeError
            return
        self.canvas.itemconfig(widget, tags = ("site_", "selected"))
        fill = self.settings['selected_fill']
        self.canvas.itemconfig("selected", fill = fill)


    def unselect(self):
        fill = self.settings['site_fill']
        self.canvas.itemconfig("selected", fill = fill)
        self.canvas.dtag("site_", "selected")

    def removeSite(self):
        widget = self.canvas.find_withtag("selected")
        if not len(widget)>0:
            return

        idx = self.canvas_sites.index(widget[0])
        sites = self.sites.get()
        del sites[idx]
        self.sites.set(sites)

        self.canvas.delete(self.canvas_sites[-1])
        del self.canvas_sites[-1]

        self.unselect()


    def addSite(self):
        fill = self.settings['site_fill']
        canvas_site = self.canvas.create_oval([0,0,1,1],fill=fill, tags = ("site_"))
        self.canvas_sites.append(canvas_site)

    #def add_editable_sites(self, site_lst):
    #    self.canvas_sites = site_lst


    def showSites(self, sites):
        r = self.settings['site_radius']
        for i, (x,y) in enumerate(self.sites.get()):
            canvas_site = self.canvas_sites[i]
            x0, y0, x1, y1 = x+r, y+r, x-r, y-r
            self.canvas.coords(canvas_site, x0, y0, x1, y1)

    def return_coords_of_clicked_site(self, x, y):
        widget = self.returnWidget(x, y)

        coords = None
        if widget:
            (x0,y0,x1,y1) = self.canvas.coords(widget)
            coords = x0+(x1-x0)/2.0, y0+(y1-y0)/2

        return coords

    def scale(self, scale):
        r = self.settings['site_radius']
        xscale, yscale = scale
        if not self.sites:
            return
        sites = self.sites.get()
        for i, (x, y) in enumerate(sites):
            sites[i] = [x * xscale, y * yscale] 

        self.sites.set(sites)

    def Move(self, event):
        x, y = event.x, event.y
        widget = self.canvas.find_withtag("selected")[0]
        idx = self.canvas_sites.index(widget)
        sites = self.sites.get()
        sites[idx] = [x, y]
        self.sites.set(sites)

