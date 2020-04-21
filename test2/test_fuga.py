import unittest
import fuga


class FugaTest(unittest.TestCase):
  # 発生した例外の種類だけチェックすれば十分な場合
  def test_fuga(self):
    with self.assertRaises()