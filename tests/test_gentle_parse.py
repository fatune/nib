import sys
import unittest

sys.path.insert(0, '../nib')


from nib.gentle_parse import GentleParse

class Test(unittest.TestCase):
    def test_one(self):
        strings = ["# This is a comment",
                   "150 70 0 1 0 BC Text",
                   "150 70 0 1 1 BC Text ugly terminate string",
                   "150 70 0 1 2 BC Text ugly terminate string"]
        lbls = GentleParse(strings)
        lbls.parse(["float", "float", "int", "int", "int", "str", "str"])

        strings2 = lbls.unparse()
        self.assertEqual(strings, strings2)

        lbls_list = lbls.aslist()
        lst = [[150.0, 70.0, 0, 1, 0, "BC", "Text"],
               [150.0, 70.0, 0, 1, 1, "BC", "Text"],
               [150.0, 70.0, 0, 1, 2, "BC", "Text"]]
        self.assertEqual(lst, lbls_list)

        self.assertEqual(lst[0][4], 0)
        self.assertEqual(lst[1][4], 1)
        self.assertEqual(lst[2][4], 2)

        lst[0][4] = 6
        self.assertEqual(lst[0][4], 6)

        strings3 =["# This is a comment",
                   "150 70 0 1 6 BC Text",
                   "150 70 0 1 1 BC Text ugly terminate string",
                   "150 70 0 1 2 BC Text ugly terminate string"]
        self.assertEqual(strings, strings3)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

