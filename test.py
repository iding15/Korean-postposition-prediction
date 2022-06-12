import unittest
from mkEumjul import hab_eum, bun_eum, bneum
import re
import numpy as np


class UnitTest(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_noun_splited(self):
        noun = '파리바  게트'
        noun = re.sub('\s+','',noun)
        self.assertEqual(noun, '파리바게트')

        splited = list(noun)
        self.assertEqual(splited[0], '파')
    
    def test_buneum(self):
        two_eum = '까'
        three_eum = '몽'

        bun_eum: str = bneum(two_eum)
        self.assertEqual(len(bun_eum), 2)

        bun_eum: str = bneum(three_eum)
        self.assertEqual(len(bun_eum), 3)
    
    def test_np_array_reshape(self):
        list_ = ['안녕하세요', '황금', '커피', '아이폰', '맥북']
        a = np.array(list_)
        b = np.array(list_).reshape(len(list_), 1)
        c = b = np.array(list_).reshape(len(list_), )
        self.assertTrue(np.array_equal(a, b))
        self.assertTrue(np.array_equal(a, c))


if __name__=='__main__':
    unittest.main()
