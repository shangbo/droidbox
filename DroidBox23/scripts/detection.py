#!/usr/bin/env python
# -*- coding:utf-8 -*-
import MySQLdb
import sys
import subprocess
import commands
import hashlib
import time
def database_get():
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='shangbo123',db='droidbox',charset='utf8')
    cur = conn.cursor()
    cur.execute('select name,md5 from droidbox_upload_droidmodel where is_checked = 0')
    not_checked_apk = cur.fetchall()
    cur.close()
    conn.close()
    return not_checked_apk

def database_set(md5):
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='shangbo123',db='droidbox',charset='utf8')
    cur = conn.cursor()
    cur.execute("update droidbox_upload_droidmodel set is_checked = 1 where md5='%s'" % md5)
    conn.commit()
    cur.close()
    conn.close()

def check_device():
    a = commands.getoutput('adb devices')
    hash = hashlib.md5()
    hash.update(a)
    return hash.hexdigest()
def main():
    while True:
        not_checked_apk = ''
        try:
            not_checked_apk = database_get()
        except MySQLdb.OperationalError:
            print '内部异常!'
            print '错误代号:%s' % sys.exc_value[0]
        except MySQLdb.ProgrammingError:
            print '数据库异常!'
            print '错误代号:%s' % sys.exc_value[0]
            print '具体细节请查询代号含义,若无法解决,请联系管理员'
        if not_checked_apk:
            hex_md5 = check_device()
            if not hex_md5 == 'bf08de11258388979967af8238d89d3e':
                print "请打开模拟器或者关掉多余的模拟器"
            else:
                i = iter(not_checked_apk)
                non_finished = True
                t = i.next()
                while non_finished:
                    ApkName = t[0]
                    md5 = t[1]
                    print '检测到应用:'
                    print '文件名:',ApkName
                    print 'md5:',md5
                    try:
                        # subprocess.call(['../droidbox.sh','../../ApkFile/'+ApkName])
                        subprocess.call(['droidbox.sh','../ApkFile/'+ApkName])
                    except KeyboardInterrupt:
                        database_set(md5)
                        try:
                            t = i.next()
                        except StopIteration:
                            non_finished = False
        else:
            print '没有未检测的应用！'
            time.sleep(3)
if __name__ == '__main__':
    main()