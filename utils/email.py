import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE
from email.encoders import encode_base64
import os

from configs import ACCOUNT, MAIL_SERVER, CC, TO, logger

if type(TO) == list:
    to = ', '.join(TO)
else:
    to = TO

if type(CC) == list:
    cc = ', '.join(CC)
else:
    cc = CC

def send_email(html, subject='', attached_file=''):
    if html:
        mime_text = MIMEText(html, 'html')
        mimemsg = MIMEMultipart()
        mimemsg['From'] = 'BUSINESS CENTER' + '<' + ACCOUNT['email'] + '>'
        mimemsg['To'] = to
        if CC:
            mimemsg['Cc'] = cc
        mimemsg['Subject'] = subject
        mimemsg.attach(mime_text)
        part = None 
        attached_file_path = ''

        if attached_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attached_file,'rb').read())
            encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={}'.format(attached_file.split('/')[-1]))
            mimemsg.attach(part)
        try:
            connection = smtplib.SMTP(host=MAIL_SERVER['host'], port=MAIL_SERVER['port'])
            connection.ehlo('mylowercasehost')
            connection.starttls()
            connection.ehlo('mylowercasehost')
            if MAIL_SERVER['host'] == 'smtp.office365.com':
                connection.login(ACCOUNT['email'], ACCOUNT['password'])
            connection.send_message(mimemsg)
            connection.quit()
            logger.info('send email')
            return True
        except Exception as e:
            logger.error(e)
            return False
    else:
        return False
