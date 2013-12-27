import Tkinter as tk

class View(tk.Toplevel):

    settings = {'bgcolor' : '#%02x%02x%02x' % (64, 204, 208)}

    def __init__(self, master, CanvasScale):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.bind("<Configure>", self.__resize)

        self.canvas = tk.Canvas(self, background=self.settings['bgcolor'])
        self.canvas.place(in_=self, anchor="c", relx=.5, rely=.5)

        self.CanvasScale = CanvasScale
        self.xscale = 1.0
        self.yscale = 1.0
        self.map_ratio = 1.0

    def __resize(self, event):
        """
        Resising of a canvas.
        cnv_width/cnv_height ratio should be equal to map_ratio.
        First we get Window ratio. Then we scale canvas.
        And after that we find xyscale coeff to scale all items in canvas

        """
        width = self.winfo_width()
        height = self.winfo_height()
        ratio = 1.0 * width / height

        if ratio < self.map_ratio:
            self.canvas.config(width=width, height=width / self.map_ratio)
        else:
            self.canvas.config(width=height * self.map_ratio, height=height)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        xscale = canvas_width / self.xscale
        yscale = canvas_height / self.yscale

        self.CanvasScale.set([xscale, yscale])

        self.xscale = canvas_width * 1.
        self.yscale = canvas_height * 1.

    def get_canvas_size(self):
        return self.canvas.winfo_width(), self.canvas.winfo_height()

