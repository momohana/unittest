import unittest
from fuga import HogeError, fuga


class FugaTest(unittest.TestCase):
  # 発生した例外の種類だけチェックすれば十分な場合
  def test_hoge(self):
    with self.assertRaises(HogeError):
      fuga()

    # with使わない場合の書き方。withを使う方がぱっと見てわかりやすい
    self.assertRaises(HogeError, fuga)

  # 発生した例外のエラーメッセージもチェックしたい場合
  def test_fuga(self):
    # エラーメッセージのチェックには正規表現が使える
    with self.assertRaisesRegex(HogeError, ".*1234.*hoge.*"):
      fuga()

if __name__=='__main__':
  unittest.main()  