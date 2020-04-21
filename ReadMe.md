# Python3 unittest使い方まとめ

## 1. unittestとは？
公式の説明に「unittestとは」の全てが含まれているので引用します。
> `unittest`ユニットテストフレームワークは元々JUnitに触発されたもので、他の言語の主要なユニットテストフレームワークと同じような感じです。テストの自動化、テスト用のセットアップやシャットダウンのコードの共有、テストのコレクション化、そして報告フレームワークからのテストの独立性をサポートしています。

また、実査の使用感としてはかなり簡単に自動試験を作成でき、他のxUnit系のツールよりもお手軽です。
そもそもxUnitが分からない、という方は「単体テストを自動化して楽するためのツールなんだなー」ぐらいに考えておいてください。

テストコードを作ったりメンテナンスしたりするコストはかかりますが、バグ修正や仕様変更で後から修正が入ったときに再試験の手間が圧倒的に少なくなります。
(リフレクションテストってやつです。デグレで泣きを見たくなければやっておきましょう)

pythonのunittestは、作成コスト・学習コストがかなり低いので、この機会に勉強しておくといずれハッピーになれます。
少なくとも単体試験が工程として存在するのであれば、絶対に作るべきです。

## 2. 基本的な使い方
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
  
```