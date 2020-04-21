from unittest import TestCase
from foo.foo import Foo


class TestFoo(TestCase):
  
  def test_say(self):
    self.assertEqual(Foo().say(), 'foo')
    
