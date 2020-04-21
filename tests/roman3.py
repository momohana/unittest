import datetime


class OutOfRangeError(ValueError): 
  pass


class UppSparkColConvertException(Exception):
  pass


def to_roman(n):
  '''convert integer to Roman numeral'''
  if not (0 < n < 4000):
    raise OutOfRangeError('numeric out of range (must be 1..3999)')

  result = ''
  for numeral, integer in roman_numeral_map:
    while n >= integer:
      result += numeral
      n -= integer
  return result

def convert_date(date_str):
  format = '%Y-%m-%d %H:%M:%S'
  col_name = 'test'
  if date_str is not None and date_str != '':
    try:
      ts = datetime.datetime.strptime(date_str, format)
      return datetime.date(ts.year, ts.month, ts.day)
    
    except Exception as e:
      msg_notice = '日付の変換に失敗しました。列名: {}, ファイル内の値: {}, 期待する形式: {}'.format(col_name, format, date_str)
      raise UppSparkColConvertException(msg_notice, e)
    
  