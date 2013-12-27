class ViewPolygons:

    def __init__(self, canvas):
        self.canvas = canvas

    def scale(self, scale):
        xscale, yscale = scale
        self.canvas.scale("polygons", 0, 0, xscale, yscale)

    def showPolygons(self, polygons, outline="black", fill="white", width=1):
        for polygon in polygons:
            points = [ item for innerlist in polygon for item in innerlist ]
            self.canvas.create_polygon(points,
                                       fill=fill,
                                       outline=outline,
                                       width=width,
                                       tags="polygons")
