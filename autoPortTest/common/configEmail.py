# coding:utf-8
"""
测试完成后，发送邮件
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading
import readConfig as readConfig
from email.header import Header
from common.Log import MyLog
import zipfile


logger = MyLog.get_log()
localReadConfig = readConfig.ReadConfig()


class Email:
    def __init__(self):
        global host, user, password, port, sender, title, tester
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        title = localReadConfig.get_email("subject")
        tester = localReadConfig.get_email("testuser")
        self.logger = logger.get_logger()
        # content = localReadConfig.get_email("content")

        # get receiver list
        self.value = localReadConfig.get_email("receiver")
        self.receiver = []
        for n in str(self.value).split("/"):
            self.receiver.append(n)

        # defined email subject
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = "接口测试报告" + " " + date + '       <Tester : ' + tester + '>'

        # self.log = MyLog.get_log()
        # self.logger = self.log.get_logger()
        self.msg = MIMEMultipart()

    def config_header(self):
        """
        defined email header include subject, sender and receiver
        :return:
        """
        self.msg['subject'] = self.subject
        self.msg['from'] = sender
        self.msg['to'] = ";".join(self.receiver)

    def config_content(self):
        """
        write the content of email
        :return:
        """
        f = open(os.path.join(readConfig.proDir, 'testFile', 'emailStyle.txt'))
        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'UTF-8')
        self.msg.attach(content_plain)
        # self.config_image()

    def config_image(self):
        """
        config image that be used by content
        :return:
        """
        # defined image path
        image1_path = os.path.join(readConfig.proDir, 'testFile', 'img', 'test.txt')
        fp1 = open(image1_path, 'rb')
        msgImage1 = MIMEImage(fp1.read())
        # self.msg.attach(msgImage1)
        fp1.close()

        # defined image id
        msgImage1.add_header('Content-ID', '<image1>')
        self.msg.attach(msgImage1)

        image2_path = os.path.join(readConfig.proDir, 'testFile', 'img', 'test.txt')
        fp2 = open(image2_path, 'rb')
        msgImage2 = MIMEImage(fp2.read())
        # self.msg.attach(msgImage2)
        fp2.close()

        # defined image id
        msgImage2.add_header('Content-ID', '<image2>')
        self.msg.attach(msgImage2)

    def config_file(self):
        """
        config email file
        :return:
        """
        # if the file content is not null, then config the email file
        if self.check_file():
            reportpath = os.path.join(readConfig.proDir, "result")
            file = os.listdir(reportpath)[-1]
            zippath = os.path.join(readConfig.proDir, "result", file + ".zip")

            # zip file
            files = os.path.join(readConfig.proDir, "result") + '/' + file
            f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
            # 压缩文件
            for dirpath, dirnames, filenames in os.walk(files):
                fpath = dirpath.replace(files, '')
                fpath = fpath and fpath + os.sep or ''
                for filename in filenames:
                    f.write(os.path.join(dirpath, filename), fpath + filename)
            self.logger.info("Compress success")
            f.close()

            reportfile = open(zippath, 'rb').read()
            filehtml = MIMEText(reportfile, 'base64', 'utf-8')
            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment; filename="test.zip"'
            self.msg.attach(filehtml)

    def check_file(self):
        """
        check test report
        :return:
        """
        reportpath = os.path.join(readConfig.proDir, "result")

        if os.path.exists(reportpath):
            return True
        else:
            return False

    def send_email(self):
        """
        send email
        :return:
        """
        self.config_header()
        self.config_content()
        self.config_file()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host, port)
            smtp.starttls()
            smtp.login(user, password)
            smtp.sendmail(sender, self.receiver, self.msg.as_string())
            smtp.quit()
            self.logger.info("The test report has send to developer by email.")
        except smtplib.SMTPException as ex:
            self.logger.info("Email sending failed")
            self.logger.error(str(ex))


class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email


if __name__ == "__main__":
    email = MyEmail.get_email()
    email.config_header()
    email.send_email()
