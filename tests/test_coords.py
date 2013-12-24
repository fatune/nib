import sys
import unittest

sys.path.insert(0, '../nib')


from nib.coords import latlong2merc, merc2latlong



import unittest

class Test(unittest.TestCase):
    def test_one(self):
        latlong = [[150, 60]]
        merc = latlong2merc(latlong)
        latlong2 = merc2latlong(merc)

        [[lat1, long1]] = latlong
        [[x, y]] = merc
        [[lat2, long2]] = latlong2

        self.assertAlmostEqual(lat1, lat2)
        self.assertAlmostEqual(long1, long2)
        self.assertAlmostEqual(y, 75.45612929021685)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

