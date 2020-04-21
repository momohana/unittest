import unittest

import hoge


# クラス名は何でも良いが、unittest.Testcaseの継承は必須
class Hoge(unittest.TestCase):
  # unittestでは関数名がtest〜で始まる関数をテストコードとして扱う。
  # test〜としておかないとテストが実行されないので注意
  def test_hoge(self):
    # 実際のテストコード。
    # ここでは関数を呼び出してその結果が正しいことを確認している。
    return_value = hoge.func_hoge(-1)
    self.assertEqual(return_value, 'a')
    
    return_value = hoge.func_hoge(0)
    self.assertEqual(return_value, 'b')


if __name__=='__main__':
  unittest.main()