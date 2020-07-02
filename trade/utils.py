import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.image import MIMEImage


def send_email(subject, message, my_user):

    try:
        my_sender = '1158677160@qq.com'  # 邮件发送者
        my_pass = ''  # 邮件发送者邮箱密码
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = formataddr(["From Server", my_sender])
        msg['To'] = formataddr(["Client", my_user])
        msg['Subject'] = subject

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
        print("---邮件发送成功---")
        return 0, ""
    except Exception as e:
        print(e, "---邮件发送失败---")
        return 1, str(e)
