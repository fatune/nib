import sys

from nib_optionparser import NibOptionParser
from tknib import TkNib
from load_data import load_data, load_sites


def main():
    optparser = NibOptionParser()
    options, polylines, polygons, sites, args = optparser.parse(sys.argv[1:])

    master = TkNib(options)

    if polygons:
        for polygon in polygons:
            lines = load_data(polygon)
            master.add_polygons(lines)

    if polylines:
        for polyline in polylines:
            lines = load_data(polyline)
            master.add_polylines(lines)

    if sites:
        for site in sites:
            sites = load_sites(site)
            master.add_sites(sites)

    master.mainloop()


if __name__ == "__main__":
    main()
