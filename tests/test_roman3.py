import roman3
import unittest


class ToRomanBadInput(unittest.TestCase):
  def test_too_large(self):
    '''to_roman should fail with large input'''
    self.assertRaises(roman3.OutOfRangeError, roman3.to_roman, 4000)

  def test_zero(self):
    '''to_roman should fail with 0'''
    self.assertRaises(roman3.OutOfRangeError, roman3.to_roman, 0)
    
  def test_negative(self):
    '''to_roman should fail with negative input'''
    self.assertRaises(roman3.OutOfRangeError, roman3.to_roman, -1)

  def test_convert_date(self):
    self.assertRaises(roman3.UppSparkColConvertException, roman3.convert_date, '2020')
    
  def test_convert_date_1(self):
    with self.assertRaises(Exception, msg='日付の変換に失敗しました。'):
      roman3.convert_date('2020')
      
if __name__ == '__main__':
    unittest.main()