#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: seedjyh@gmail.com
# Create date: 2018/11/2
import re


class Decrypter:
    """
    decrypt javascript code such as "eval(function(p,a,c,k,e,d){...}(...))"
    """

    @staticmethod
    def decrypt(ciphertext):
        re_result = re.search("}\('(.*)',(\d+),(\d+),'(.*)'.split", ciphertext)
        pattern = re_result.group(1)
        base = int(re_result.group(2)) # 10 means {0~9}, 36 means {0~9,a~z}, 62 means {0~9,a~z,A~Z}.
        # matcher_size = int(re_result.group(3)) # same as len(matcher_list)
        dictionary = Dictionary(re_result.group(4))
        result = ""
        while True:
            search_result = re.search("\w+", pattern)
            if search_result:
                begin, end = search_result.span()
                result += pattern[:begin] + dictionary.get(pattern[begin:end], base)
                pattern = pattern[end:]
            else:
                result += pattern
                break
        return result


class Dictionary:
    """
    This class accepts a str such as "pages|jpg|var||str", words separated by "|""
    Then, it returns word matched by a "index word", which is a number contains 0-9a-zA-Z based on 2~62.
    If there's matched word, returns the word, else, returns the "index word".
    """
    def __init__(self, word_str):
        self.word_list = word_str.split("|")

    def get(self, index_word, base):
        index = self.parse_int(index_word, base)
        if index >= len(self.word_list):
            raise Exception("Index %d is out of range of word list of size %d" % (index, len(self.word_list)))
        result = self.word_list[index]
        if result == "":
            # if value is empty str, return index word.
            return index_word
        else:
            return result

    @staticmethod
    def parse_int(word, base):
        """
        @word is a 'str'
        @base could be 2,3,...,62
        10 means 0~9
        36 means 0,1,...,9,a,b,...,z
        52 means 0,1,...,9,a,b,...,z,A,B,...,Z
        return a 'int'
        """
        dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if base < 2 or base > len(dictionary):
            raise Exception("Invalid base which is %d and should be [2,%d]" % (base, len(dictionary)))
        result = 0
        for c in word:
            now_number = dictionary.find(c)
            if now_number >= base:
                raise Exception("Letter %s does not exist in such base %d" % (c, base))
            result = result * base + now_number
        return result


if __name__ == "__main__":
    pass
