#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import chardet
import re 

class TextDetect:
    path_root = ''
    file_pattern = ''

    def __init__(self, path_root, file_pattern):
        self.path_root = path_root
        self.file_pattern = file_pattern

    def print_member():
        print("path_root = %s"%(self.path_root))
        print("file_pattern = %s"%(self.file_pattern))


    def convert(self,file, in_enc="GBK", out_enc="UTF-8"):
        """
        该程序用于将目录下的文件从指定格式转换到指定格式，默认的是GBK转到utf-8
        :param file:    文件路径
        :param in_enc:  输入文件格式
        :param out_enc: 输出文件格式
        :return:
        """
        in_enc = in_enc.upper()
        out_enc = out_enc.upper()
        try:
            print("convert [ " + file.split('\\')[-1] + " ].....From " + in_enc + " --> " + out_enc)
            f = codecs.open(file, 'r', in_enc, "ignore")
            new_content = f.read()
            codecs.open(file, 'w', out_enc).write(new_content)
        except IOError as err:
            print("I/O error: {0}".format(err))


    def detect(self, in_enc="GBK", out_enc="UTF-8"):
        for root, dirs, files in os.walk(self.path_root, topdown=True):
            for item in files:
                match = re.match(self.file_pattern, item, re.IGNORECASE)
                if not match:
                    continue
                item_path = os.path.join(root,item)
                print("find file name = %s"%(item))
                with open(item_path, "rb") as f:
                    data = f.read()
                    codeType = chardet.detect(data)['encoding']
                    print("%s's codeType is %s"%(item, codeType))
                    if in_enc == "GBK": #GBK特殊处理一下
                        if codeType == 'GB2312' or codeType == 'GBK' or codeType == 'GB18030':
                            print("%s's codeType is %s,change encode!"%(item,codeType))
                            self.convert(item_path, codeType, out_enc)
                    else:
                        if codeType == in_enc:
                            print("%s's codeType is %s,change encode!"%(item,codeType))
                            self.convert(item_path, codeType, out_enc)



if __name__ == "__main__":
    # 使用时填写这四个参数即可

    # 处理的根路径
    path_root = r"C:\Users\yu\Desktop\QvtkDicomReader-master\QvtkDicomViewer"

    # 要进行格式转换的文件正则表达式,匹配某一类型的文件
    search_file_pattern = ".*\.[ch][ph]*"

    # 要转换的源编码
    in_enc = "GB2312"

    # 要转换的目的编码
    out_enc = "UTF-8"


    my_detect=TextDetect(path_root, search_file_pattern)
    my_detect.detect(in_enc, out_enc)