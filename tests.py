import unittest


class Tests_general(unittest.TestCase):
    def test_a1(self):
        assert len('abc') == 3
    def test_a2(self):
        assert len('aaa') == 2
        
 
if __name__ == '__main__':
    unittest.main()
