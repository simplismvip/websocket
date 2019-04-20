#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import os
import hashlib
def md5hex(word):
    """ MD5加密算法，返回32位小写16进制符号
    """
    if isinstance(word, unicode):
        word = word.encode("utf-8")
    elif not isinstance(word, str):
        word = str(word)
    m = hashlib.md5()
    m.update(word)
    return m.hexdigest()
 
def md5sum(fname):
    """ 计算文件的MD5值
    """
    def read_chunks(fh):
        fh.seek(0)
        chunk = fh.read(8096)
        while chunk:
            yield chunk
            chunk = fh.read(8096)
        else: #最后要将游标放回文件开头
            fh.seek(0)
    m = hashlib.md5()
    if isinstance(fname, basestring) \
            and os.path.exists(fname):
        with open(fname, "rb") as fh:
            for chunk in read_chunks(fh):
                m.update(chunk)
    #上传的文件缓存 或 已打开的文件流
    elif fname.__class__.__name__ in ["StringIO", "StringO"] \
            or isinstance(fname, file):
        for chunk in read_chunks(fname):
            m.update(chunk)
    else:
        return ""
    return m.hexdigest()

if __name__ == "__main__":
    path1 = "/Users/junming/Desktop/Code/iOS/AppProject/ChinaPoem/ChinaPoem/Source/ChinaPoem.ttf"
    # 659a5977129abe43c6cea976bbb53dd1
    # 34d8cd0803e7bd5af3af83c3112e75f3
    path2 = "/Users/junming/Desktop/Code/iOS/AppProject/CPoem/JMPoem/DataSource/SentyZHAO.ttf"
    # a518d732b98577365aa0a6998ea9f367
    # 34d8cd0803e7bd5af3af83c3112e75f3
    md5 = md5sum(path1)
    print md5











