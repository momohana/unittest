import unittest
import hoge_sum


class HogeSum(unittest.TestCase):
  def test_hoge_sum(self):
    # テストパターンをlistで用意する
    # (x, y, 正解値)の組み合わせ
    patterns = [
        (0, 1, 1),
        (-1, 1, 0),
        (1, -2, -1)
    ]
    
    # 作ったパターンのlistをforで回す
    for x, y, result in patterns:
      # subTest()の引数には失敗時に出力したい内容を指定。パラメータすべてを入れておくのが無難。
      with self.subTest(x=x, y=y, result=result):
        self.assertEqual(hoge_sum.hoge_sum(x,y), result)


if __name__=='__main__':
  unittest.main()