#!/usr/bin/env python
# -*- coding:utf-8 -*-
###################################################
#      Filename: main.py
#        Author: lzw.whu@gmail.com
#       Created: 2019-03-25 11:01:58
# Last Modified: 2019-03-25 12:09:56
###################################################
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os


def getopts():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('zipfile', type=str, help='location of duplicate_file.csv.zip')
    return parser.parse_args()


def make_sure_path_exists(path):
    import errno
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e


def main():
    import codecs
    import zipfile
    zipfn = getopts().zipfile
    csv_dir = os.path.join(os.path.dirname(os.path.realpath(zipfn)), 'data')
    make_sure_path_exists(csv_dir)
    with zipfile.ZipFile(zipfn) as zfp:
        for f in zfp.namelist():
            zfp.extract(f, csv_dir)

    check_d = {}
    to_delete = []

    csvfn = os.path.join(csv_dir, 'duplicate_file.csv')
    with codecs.open(csvfn, encoding='utf-16le') as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.strip('\n')
            cols = line.split('\t')

            groupid = cols[0]
            fn = cols[2]
            if groupid not in check_d:
                check_d[groupid] = fn
            else:
                to_delete.append((groupid, fn.strip('"')))

        print(len(to_delete))
        for groupid, fn in to_delete:
            try:
                os.remove(fn)
                print(groupid, fn, "...deleted")
            except Exception as e:
                print(groupid, fn, "...failed", e)


if __name__ == '__main__':
    main()
