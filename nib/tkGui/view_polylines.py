class ViewPolylines:

    def __init__(self, canvas):
        self.canvas = canvas

    def scale(self, scale):
        xscale, yscale = scale
        self.canvas.scale("polylines", 0, 0, xscale, yscale)

    def showPolylines(self, polylines, fill="green", width=1):
        for polyline in polylines:
            points = [ item for innerlist in polyline for item in innerlist ]
            self.canvas.create_line(points,
                                    fill=fill,
                                    width=width,
                                    tags="polylines")
