import unittest


class Tests_general(unitest.TestCase):
    def test_a1(self):
        assert len('abc') == 3
        
 
if __name__ == '__main__':
    unittest.main()
