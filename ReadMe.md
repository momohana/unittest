# Python3 unittest使い方まとめ

## 1.unittestとは？
公式の説明に「unittestとは」の全てが含まれているので引用します。
> `unittest`ユニットテストフレームワークは元々JUnitに触発されたもので、他の言語の主要なユニットテストフレームワークと同じような感じです。テストの自動化、テスト用のセットアップやシャットダウンのコードの共有、テストのコレクション化、そして報告フレームワークからのテストの独立性をサポートしています。

また、実査の使用感としてはかなり簡単に自動試験を作成でき、他のxUnit系のツールよりもお手軽です。
そもそもxUnitが分からない、という方は「単体テストを自動化して楽するためのツールなんだなー」ぐらいに考えておいてください。

テストコードを作ったりメンテナンスしたりするコストはかかりますが、バグ修正や仕様変更で後から修正が入ったときに再試験の手間が圧倒的に少なくなります。
(リフレクションテストってやつです。デグレで泣きを見たくなければやっておきましょう)

pythonのunittestは、作成コスト・学習コストがかなり低いので、この機会に勉強しておくといずれハッピーになれます。
少なくとも単体試験が工程として存在するのであれば、絶対に作るべきです。

## 2.基本的な使い方
一番基本的な使い方は、以下です。
1. 試験したい関数を呼び出す。
2. その結果が想定通りかを判定する。

例えば以下の関数の試験を考えてみます。
```python
def func_hoge(x):
  if x < 0:
    return 'a'
  else:
    return 'b'
```
この関数をunittestで自動化すると以下になります。
```python
import unittest

# テストしたい関数のあるモジュールをimport
import hoge


# クラス名は何でも良いが、unittest.TestCaseの継承は必須
class Hoge(unittest.TestCase):
  # unittestでは関数名がtest〜で始まる関数をテストコードとして扱う。
  # test〜としておかないとテストが実行されないので注意。
  def test_hoge(self):
    # 実際のテストコード。
    # ここでは関数を呼び出して、その結果が正しいことを確認している。
    return_value = hoge.func_hoge(-1)
    self.assertEqual(return_value, 'a')

    return_value = hoge.func_hoge(0)
    self.assertEqual(return_value, 'b')


if __name__=='__main__':
  unittest.main()
```
詳しい説明はコードのコメントに書きましたが、まずは以下を抑えておきましょう。
1. テストはunittest.TestCaseを継承したクラスの中に書く。
2. テストの関数名はtest〜で始まる。
3. 判定はself.assertEqual等、unittestで用意されている判定を使用する。

「3.」の判定はNotEqalやRegex等、他にも色々な種類があるので判定したい内容に合わせて変えていくことになるかと思います。
ちなみにこの判定関数はアサートメソッドというのが一般的です。
ここまで説明を忘れていましたが、テストケース等の語句は以下の意味で使用しています。
- テスト
  - def test_xx()のこと。
  - 1つのテスト項目に対応。
- テストケース
  - unittest.TestCaseを継承したクラスのこと。
  - テストの論理的なまとまり。
- テストスイート
  - テストケースのまとまり。

unittestの基本的な使い方は以上です。

## 3.テストケースの分け方
テストコードを書いているとテストケースをどの単位でまとめるかを迷うことは多々あるかと思います。
これは本当に人それぞれだと思うので、私の個人的な方針だけ書いておきます。
1. subTest()を使用sルウ場合を除き、1試験項目につき1つのテストを作成
2. 1関数に1つのテストケースを作成
3. 同じクラスのメソッドに対するテストケースはなるべくテストスイートにまとめる

「1.」は、試験が失敗したときにどこで失敗したのかが分からなくなるので、ほぼ必須かと思います。
「2.」と「3.」はsetUp/tearDownの処理を制御したい場合や、テスト対象の結合度的な部分で変わってくるので、ベストエフォートな感じです。

## 4.パターンが多い試験の扱い
テストしたい関数に影響するパラメータが大量にあって、ペアワイズ法とか直行表を使っても項目数が2〜3桁になってしまうことはザラにあるかと思います。
「じゃあ、for回せばよくね？」と思うかも知れませんが、for分でテストを実行すると以下のデメリットがあります。
-  途中で失敗した場合は、そのテストケースはそこで終了する。
-  テストケースの失敗として扱われるので、どのパターンで失敗したのかが分からない。

かと言って、1パターン毎にテストを書くのはしんどいですよね。
そんなときのベストプラクティスがunittestには用意されています。
それがsubTestという仕組みです。
コードを見てもらったほうが早いと思うので、まずは以下をどうぞ。
```python
import unittest


def sum(x, y):
  return x + y


class Hoge(unittest.TestCase):
  def test_sum(self):
    # テストパターンをlistで用意する。
    # (x, y, 正解値)の組み合わせ
    patterns = [
      (0, 1, 1),
      (-1, 1, 0),
      (1, -2, -1),
    ]

    # 作ったテストパターンのlistをforで回す
    for x, y, result in patterns:
      # subTest()の引数には失敗時に出力したい内容を指定。パラメータ全てを入れておくのが無難。
      with self.subTest(x=x, y=y, result=result):
        self.assertEqual(sum(s, y), result)


if __name__=='__main"__':
  unittest.main()
```
このようにsubTestを利用した書き方をすると、一つにテストケース内で複数のパターンを個別にテストすることができます。
もちろん途中で失敗のパターンがあっても最後まで実行してくれますし、失敗のパターンも個別に表示してくれます。

```bash
$ python3 ./subtest.py
=======================================================================
FAIL: test_sum (__main__.Hoge) (x=-1, y=1, result=2)
-----------------------------------------------------------------------
Traceback (most recent call last):
  File "./subtest.py", line 22, in test_sum
    self.assertEqual(sum(x, y), result)
AssertionError: 0 != 2

-----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILD (failures=1)
```

## 5.例外の試験
例外の試験の確認方法はそんなに難しくないです。
```python
import unittest


# 適当な例外クラス
class HogeError(Exception):
  def __init__(self, code, message):
    self.code = vode
    self.message

  def __str__(self):
    return "[{0}]: {1}".format(self.code, self.message)

# 例外を返す適当な関数
def hoge():
  raise HogeError(1234, "hoge")


class HogeTest(unittest.TestCase):
  # 発生した例外の種類だけチェックすれば十分な場合
  def test_hoge(self):
    with self.assertRaises(HogeError):
      hoge()

    # withを使わない場合の書き方。
    self.assertRaises(HogeError, hoge)

  # 発生した例外のエラーメッセージもチェックしたい場合
  def test_fuga(self):
    # エラーメッセージのチェックには正規表現が使える
    with self.assertRaisesRegex(HogeError, ".*1234.*hoge.*"):
      hoge()

    # コンテキストマネージャに格納された例外オブジェクト
    the_exception = cm.exception

    # 中身を好きにチェックする
    self.assertEqual(the_exception.ode, 1234)


if __name__=='__main__':
  unittest.main()
```

## 6.標準入力・標準出力の試験
### 標準入力の試験
標準入力を試験したい、というか標準入力を想定した試験がしたい場合は、特に変わったことをする必要はありません。
標準入力する関数(input()等)にパッチを当てるだけです。
モックやパッチについては[こちら](#8.mock)で説明しているのでそちらをご確認してください。

### 標準出力の試験
続いて標準出力の確認ですが、こちらは少し小手先のテクニックが必要です。
```python
import sys
from io import StringIO
from contextlib import redirect_stdout


io = StringIO()
with redirect_stdout(io):
  # このwith句内での標準出力はioに格納される
  print('hoge')

# 標準出力なので、改行文字などに注意
self.assertEqual(io.getvalue(), 'hoge\n')
```
ポイントは以下です。
- StringIO()を用意し、redirect_stdout()で標準出力をリダイレクトする
- redirect_stdout()のwith句内でテストしたい標準出力を実行する
- getvalue()で標準出力された文字列を取得し比較する

## 7.main関数の試験
unittestでmainを試験すべきかどうかの議論もありますが、今回はそれを置いておいて、main関数を試験するテクニックをさくっとご紹介します。
```python
import unittest
# 標準出力をみるためのモジュール達
import sys
from io import StringIO
from contextlib import redirect_stdout
# テスト対象
import sample


class MainTest(unittest.TestCase):
  def test_main(self):
    # main関数の呼び出し自体は他の関数とかと同じ
    # main()は標準入出力を扱う必要があるのでそこが少し面倒

    # コマンドライン引数を懐疑的に再現するためsys.argv()に自前で格納
    # cleanしないと正しい引数を渡せないので注意
    sys.argv.clear()
    sys.argv.append('./sample.py')
    sys.argv.append('--arg1')
    sys.argv.append('hogehoge')

    # main()の標準出力をioにリダイレクト
    io = StringIO()
    with redirect_stdout(io):
      sample.main()

    # mainの標準出力をチェック
    self.assertEqual(io.getvalue(), 'hogehoge\n')

if __name__=='__main__':
  unittest.main()
```
コード内のコメントで大体説明していますが、以下の2点を押さえていれば問題ないでしょう。
- コマンドライン引数を疑似るためにsys.argvに自前で値を格納する
- main関数の標準出力をリダイレクトしてチェックできるようにする

pythonスクリプトだとあまり見かけないので省略しましたが、スクリプトの修了ステータスをチェックしたい場合はsys.exit()等をモックにしてチェックすることになります。
このときの注意点としては、pythonだと"main()の返り値" != "スクリプトの終了ステータス"だと言うことです。main()でreturn 1だとしても終了ステータスが1になるわけではないのです。
異常系の試験でmain()の終了ステータスとして確認すべきは、sys.exit()が呼ばれたかどうかとその値が0以外であることです。

## 8.mock
まずはmockとはなんぞや、という話ですが、「テスト対象のコード内で使用している別のオブジェクト(テスト対象ではないシステムの関数等)を置き換える機能」と考えて貰えれば良いかと思います。誤解を恐れずに言えば、スタブです。
何が嬉しいかというと、例えばsocketを使用しているコードの試験をする際に、socketをmockにしておけばテストのたびに接続先を用意する必要がなくなり、環境構築とかいう糞みたいな作業から開放されます。
Pythonのunittestの世界ではモック(mock)とパッチ(patch)という概念があり、それぞれ以下のような認識です。
- mock : 引数や呼び出された回数をチェックする機能を持ち、返り値や例外送出も自在に設定可能なオブジェクト。
- patch : システムの関数やクラスをmockオブジェクトに置き換えること。また、その仕組み。

mock & patch を使用すれば異常系の試験も楽々です。

### 8.1.mockの使い方
まずは簡単なモックを作りos.path.abspath()にパッチを当ててみたいと思います。
```python
import unittest
import unittest.mock
import os


def print_abspath(x):
  print(os.path.abspath(x))


class MockTest(unittest.TestCase):
  def test_hoge(self):
    # モックを作成
    m = unittest.mock.MagicMock()

    # 動作を置き換えたいオブジェクトにモックを代入(パッチを当てる)
    os.path.abspath = m

    # テスト対象コードの実行
    print_abspath('hoge')

    # モックが正しい引数で呼び出されたことのチェック
    m.assert_called_with('hoge')


if __name__=='__main__':
  unittest.main()
```
unittestと同じで方法さえ分かってしまえばmockも使い方はとても簡単なのです。
コード内のコメントで説明していますが、ポイントをまとめると以下のとおりです。
1. モックを作る。
2. 動作を置き換えたいオブジェクトにパッチを当てる。
3. テスト対象のコードを実行する。
4. テスト対象のコードがモックを想定どおりに呼び出したかをチェックする。

「4.」のチェックで今回はassert_called_with()を使用しましたが、このアサートメソッドは他にも種類があります。

### 8.2.mockをカッコよくきれいに書く方法
このページの解説では分かりやすさ重視で冗長に書いていますが、デコレータ等を使用するとmockの記述はもっとスッキリ書くことができます。
一重にmockといいましても、テスト単位で当てるのか、テストケース単位で当てるのか等、状況によってベストプラクティスは変わってくるものです。
ここではありがちなパターンでの「僕の考えた最強のモックの書き方」をご紹介致します。
#### 特定のテスト内でパッチを当てる
この場合は愚直に定義する方法の他に2つのアプローチがとれます。
1. コンテキストマネージャ(with句)を使う方法
```python
with unittest.mock.patch('os.path.abspath', side_effect=time.sleep(3)) as m:
  m.return_value = 'hoge'
  path = print_abspath('hoge')
```
書き方としてはpatch()の第一引数にパッチを当てたいオブジェクト名の文字列、キーワード引数でそれぞれ設定したい項目です。
with〜as m:にして、m.return_value等で設定することも可能です。
この書き方であればwith句を出れば自動的にパッチが解除されるのでお掃除系を考えなくてもよくて楽です。

2. テストに対してデコレータを使用する方法
```python
@unittest.mock.patch('os.path.abspath', return_value='hoge')
def test_hoge(self, mock):
  mock.side_effect = OSError("dummy_error")
  path = os.path.abspath()
```
この書き方であればデコレータを設定したテスト全体でmockが適用されます。
テストの第二引数以降にパッチが指定されてくるのですが、自分は複数指定した場合にハマってしまいました。

例えば以下のように2つパッチを設定するとします。
```python
@unittest.mock.patch('func1')
@unittest.mock.patch('func2')
def test_hoge(self, p1, p2):
  pass
```
このとき、p1,p2には何が入っていると思います？
p1 → func2のパッチ
p2 → func1のパッチ
ですよ？
「「「ざっけんなぁぁぁぁ」」」って公式ドキュメント見に行ったら、デコレータはそんなもんだぜ、って書いてありました。
話が逸れましたが、テスト単位でパッチを当てる場合はwith句を使用する方法とデコレータを使用する方法があると言うことです。
with句の方がスコープが厳密で正しいのかも知れませんが、インデントを深くしたくないので、デコレータを愛用しています。

#### テストケースの単位でパッチを当てる
テストケース単位でパッチを当てる場合も2つのアプローチがあります。
1. デコレータを使用する
```python
@unittest.mock.patch('os.path.abspath')
class HogeTest(unittest.TestCase):
  def test_hoge(self, mock):
    pass
```
基本的な書き方はテスト単位のデコレータと同じなので割愛しますが、テストケースのクラスに対してデコレータ式を使用することで、そのテストケース全体でそのパッチが使用できるようになります。
若干扱いが面倒なので、以下の2点には注意が必要です。
   1. テストケース内の全てのテストでdef test_*(..., mock): のようにモックを引数にとる必要がある。
   2. テストの中でreturn_value等を設定した場合は他のテストには反映されない(モックはテスト毎に別オブジェクト扱い)

2. setUpで定義する
```python
class HogeTest(unittest.TestCase):
  def setUp(self):
    patcher = unittest.mock.patch('os.path.abspath')
    self.mock = patcher.start()
    self.addCleanup(patcher.stop)

def test_hoge(self):
    pass
```
setUp()内でパッチを定義＆開始して、それをメンバ変数に入れています。
addCleanup()はテストケースが異常終了してtearDown()した場合でもパッチを修了させるために書いています。
「1.」同様、パッチはテスト毎に生成されて別オブジェクトになるのでテスト内でパッチを弄っても他のテストには反映されません。
「1.」、「2.」一長一短ではありますが、テスト毎に一々モックを引数をとるのは煩わしいので、「2.」がお勧めです。

### 8.3.mockの戻り値や例外送出を設定する方法
方法さえ知っていれば簡単。
```python
def get_joined_path(x, y):
  return os.path.join(x, y)


class MockTest(unittest.TestCase):
  def test_hoge(self):
    m = unittest.mock.MagickMock()

    # モックに戻り値を設定してテストを実行
    m.return_value = 'aaaa'
    os.path.join = m
    path = get_joined_path('hoge', 'piyo')

    # 戻り値が正しいことのチェック(mockでわざと書き換えた値なので正しくはないですが)
    self.assertEqual(path, 'aaaa')

    # 例外送出を設定したい場合はside_effectに例外を指定する
    m.side_effect = OSError("dummy_error")

    # 例外の試験なのでassertRaisesで囲っておく
    with self.assertRaises(OSError) as cm:
      path = get_joined_path('aaaa', 'bbbb')

    # 例外が想定どおりであることを確認
    self.assertEqual(str(cm.exception), str(OSError("dummy_error")))
```

### 8.4.print()等、ビルトイン関数にパッチを当てたい場合
方法さえ知っていれば簡単。
```python
import unittest
import unittest.mock


def print_hoge():
  print(hoge)


class HogeTest(unittest.TestHoge):
  # 組み込み関数にパッチを当てる場合は__main__.*に当てる
  @unittest.mock.patch('__main__.print')
  def test_print():
    print_hoge()

    m.assert_called_with('hoge')

if __name__=='__main__':
  unittest.main()
```

## 9.アサートメソッドについて
よく使うアサートメソッド一覧

|メソッド|どのようなチェックが行われるか|
|:--|:--|
|assertEqual(a, b)|a == b|
|assertNotEqual(a, b)|a != b|
|assertTrue(x)|bool(x) is True|
|assertFalse(x)|bool(x) is False|
|assertIs(a, b)|a is b|
|assertIsNot(a, b)|a is not b|
|assertIsNone(x)|x is None|
|assertIsNotNone(x)|x is not None|
|assertIn(a, b)|a in b|
|assertNotIn(a, b)|a not in b|
|assertIsInstance(a, b)|isinstance(a, b)|
|assertNotIsInstance(a, b)|not isinstance(a, b)|
|assertRaises(exc, fun, *arg, **kwads)|fun(*arg, **kwds)がexcを送出する|
|assertRaisesRegex(exc, r, fun, *arg, **kwds)|fun(*arg, **kwds)がexcを送出してメッセージが正規表現rとマッチする|
|assertGreater(a, b)|a > b|
|assertGreaterEqual(a, b)|a >= b|
|assertLess(a, b)|a < b|
|assertLessEqual(a, b)|a <= b|
|assertRegex(s, r)|r.search(s)|
|assertNotRegex(s, r)|not r.search(s)|
