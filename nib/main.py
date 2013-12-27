import sys

from nib_optionparser import NibOptionParser
from tknib import TkNib
from load_data import load_data, load_sites, load_sites2edit

import Tkinter as tk
from controller import Controller


def main():
    optparser = NibOptionParser()
    options, polylines, polygons, sites, edit_sites, args = optparser.parse(sys.argv[1:])

    root = tk.Tk()
    root.withdraw()
    app = Controller(root, options)

    if polygons:
        for polygon in polygons:
            lines = load_data(polygon)
            app.add_polygons(lines)

    if polylines:
        for polyline in polylines:
            lines = load_data(polyline)
            app.add_polylines(lines)

    #if sites:
    #    for site in sites:
    #        sites = load_sites(site)
    #        app.add_sites(sites)

    if edit_sites:
        sites2edit = load_sites2edit(edit_sites)
        sites2edit.parse(["float", "float"])
        app.add_sites2edit(sites2edit, edit_sites)

    root.mainloop()


if __name__ == "__main__":
    main()
