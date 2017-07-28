import unittest
from picksource import *

class TestResConvert(unittest.TestCase):

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_xlsx_save(self):
        res = []
        save_to_xlsx(res)


if __name__ == '__main__':
    unittest.main()
