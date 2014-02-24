#!/usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib
import email.utils
import email.encoders
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
import MySQLdb
import time
# from email.mime.image import MIMEImage
# import getpass

#global var
MAIL_SERVER_NAME = 'smtp.163.com'
USERNAME = 'shangbo808@163.com'
PASSWORD = 'sbcheerup123'
BASIC_PATH = '../'


#get information which is checked but not send email
def get_info():
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='shangbo123',db='droidbox',charset='utf8')
    cur = conn.cursor()
    cur.execute("select name,email,md5 from droidbox_upload_droidmodel where is_checked = 1 and is_sent_email = 0")
    info = cur.fetchone()
    cur.close()
    conn.close()
    return info


# set is_sent_email = 1 by md5
def set_info(md5):
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='shangbo123',db='droidbox',charset='utf8')
    cur = conn.cursor()
    cur.execute("update droidbox_upload_droidmodel set is_sent_email = 1 where md5 = '%s'" % md5)
    conn.commit()
    cur.close()
    conn.close()


# identify message
def get_main_body():
    try:
        f = open(BASIC_PATH+'templates/mail.html', 'r+')
    except IOError:
        f = open('templates/mail.html', 'r+')
    text = f.read()
    f.close()
    msg_text = MIMEText(text, _subtype='html')

    return msg_text


def get_result(apk_name):
    try:
        f = open(BASIC_PATH+'AnalysisInformation/'+apk_name+'_Information.txt','r+')
    except IOError:
        f = open('AnalysisInformation/'+apk_name+'_Information.txt','r+')
    result = f.read()
    f.close()

    msg_file_result = MIMEBase('text','plain')
    msg_file_result.set_payload(result)
    email.encoders.encode_base64(msg_file_result)
    msg_file_result.add_header('Content-Disposition','attachment',filename='result.txt')

    return msg_file_result


def get_images(apk_name):
    try:
        f = open(BASIC_PATH+'AnalysisImages/'+apk_name+'_behaviorgraph.png','rb')
    except IOError:
        f = open('AnalysisImages/'+apk_name+'_behaviorgraph.png','rb')
    image_1 = f.read()
    f.close()
    try:
        f = open(BASIC_PATH+'AnalysisImages/'+apk_name+'_tree.png','rb')
    except IOError:
        f = open('AnalysisImages/'+apk_name+'_tree.png','rb')
    image_2 = f.read()
    f.close()

    msg_image_1 = MIMEApplication(image_1)
    msg_image_1.add_header('Content-Disposition', 'attachment', filename='behavior.png')
    msg_image_2 = MIMEApplication(image_2)
    msg_image_2.add_header('Content-Disposition', 'attachment', filename='tree.png')

    return msg_image_1,msg_image_2


def get_msg(main_body,result,images):
    msg_main = MIMEMultipart()
    msg_main.attach(main_body)
    msg_main.attach(result)
    msg_main.attach(images[0])
    msg_main.attach(images[1])

    return msg_main


def set_header(msg_main,to_email):
    msg_main.set_unixfrom('soul')
    msg_main['To'] = email.utils.formataddr(('shangbo', to_email))
    msg_main['From'] = email.utils.formataddr(('soul', 'shangbo808@163.com'))
    msg_main['Subject'] = 'Test from soul'
    msg_main['Date'] = email.utils.formatdate()


def send_email(msg_main,to_email):
    server = smtplib.SMTP(MAIL_SERVER_NAME)
    try:
        server.set_debuglevel(True)
        server.ehlo()
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo()
        server.login(USERNAME,PASSWORD)
        server.sendmail('shangbo808@163.com', [to_email], msg_main.as_string())
    finally:
        server.quit()


def mail_main():
    while True:
        info = get_info()
        if info:
            apk_name,to_email,md5 = info[0],info[1],info[2]
            print 'send email to ',to_email
            msg_text = get_main_body()
            msg_file_result = get_result(apk_name)
            msg_file_images = get_images(apk_name)
            msg_main = get_msg(msg_text,msg_file_result,msg_file_images)
            set_header(msg_main,to_email)
            send_email(msg_main,to_email)
            set_info(md5)
        else:
            print '没有需要发送的邮件！'
            time.sleep(3)


def mail_again(name, email):
    apk_name = name
    msg_text = get_main_body()
    msg_file_result = get_result(apk_name)
    msg_file_images = get_images(apk_name)
    msg_main = get_msg(msg_text, msg_file_result,msg_file_images)
    set_header(msg_main, email)
    send_email(msg_main, email)
if __name__ == '__main__':
    mail_main()