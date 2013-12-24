import sys
from optparse import OptionParser

class NibOptionParser():
    def __init__(self):
        self.parser = OptionParser()
        self.parser.add_option('-r', '--region', dest='region',
                             help = 'region of a map in format y0,y1,x0,x1')
        self.parser.add_option('-p', '--polygons', dest='polygons',
                             help = 'comma separeted string of filenames of polygons to plot')
        self.parser.add_option('-l', '--polylines', dest='polylines',
                             help = 'comma separeted string of filenames of polylines to plot')
        self.parser.add_option('-s', '--sites', dest='sites',
                             help = 'comma separeted string of filenames of sites to plot')


    def parse(self, argv):
        options, args = self.parser.parse_args(argv)
        my_options = {}

        try:
            [ y0, y1, x0, x1 ] = [ float(x) for x in options.region.split(',') ]
            my_options['y0'] = y0
            my_options['y1'] = y1
            my_options['x0'] = x0
            my_options['x1'] = x1
        except ValueError:
            print "Error: Wrong region option"
            sys.exit()

        polylines = None
        if options.polylines:
            try:
                polylines = options.polylines.split(',')
            except ValueError:
                print "Error: Wrong polyline option"
                sys.exit()

        polygons = None
        if options.polygons:
            try:
                polygons = options.polygons.split(',')
            except ValueError:
                print "Error: Wrong polygons option"
                sys.exit()

        sites = None
        if options.sites:
            try:
                sites = options.sites.split(',')
            except ValueError:
                print "Error: Wrong sites option"
                sys.exit()

        return my_options, polylines, polygons, sites, args






