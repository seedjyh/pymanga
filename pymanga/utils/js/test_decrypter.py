#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: seedjyh@gmail.com
# Create date: 2018/11/2
import unittest
from unittest import TestCase

from pymanga.utils.js.decrypter import Decrypter, Dictionary


class TestDecrypter(TestCase):

    def test_decypt(self):
        self.maxDiff = None
        ciphertext = """eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('y j=j=\'["q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/o.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/r.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/s.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/t.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/u.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/k.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/l.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/m.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/n.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/p.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/F.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/C.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/D.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/v.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/E.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/B.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/A.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/w.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/x.b","q\\/%1%2%8%0%9%7%0%a%6%3%5%4%0%d%h%g%i%e\\/f%1%2%c\\/z.b"]\';',42,42,'E5|E8|AF|E4|8A|B8|B0|A8t|B7|9C|8F|jpg|9D|BE|91|21|E7|AE|AC|pages|P06|P07|P08|P09|P01|P10||P02|P03|P04|P05|P14|P18|P19|var|P20|P17|P16|P12|P13|P15|P11'.split('|'),0,{}))"""
        expected_plaintext = """var pages=pages='["q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P01.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P02.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P03.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P04.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P05.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P06.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P07.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P08.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P09.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P10.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P11.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P12.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P13.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P14.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P15.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P16.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P17.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P18.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P19.jpg","q\/%E8%AF%B7%E5%9C%A8t%E5%8F%B0%E4%B8%8A%E5%BE%AE%E7%AC%91\/21%E8%AF%9D\/P20.jpg"]';"""
        plaintext = Decrypter.decrypt(ciphertext)
        self.assertEqual(plaintext, expected_plaintext)


class TestDictionary(TestCase):
    def test_parse_int(self):
        self.assertEqual(12, Dictionary.parse_int("12", 10))
        self.assertEqual(46, Dictionary.parse_int("1a", 36))
        self.assertEqual(98, Dictionary.parse_int("1A", 62))


if __name__ == "__main__":
    unittest.main()
