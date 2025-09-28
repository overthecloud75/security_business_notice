import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE
from email.encoders import encode_base64
import os

from configs import ACCOUNT, MAIL_SERVER, CC, TO, logger

def send_email(html, subject='', attached_file=''):
    if html:
        mime_text = MIMEText(html, 'html')
        mimemsg = MIMEMultipart()
        mimemsg['From'] = 'BUSINESS CENTER' + '<' + ACCOUNT['email'] + '>'
        mimemsg['To'] = TO
        if CC:
            mimemsg['Cc'] = CC
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

def get_email_html(subject, results=[]):
    html = '''
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Threat Intelligence</title>
        <style>
            .vertical-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            .vertical-table th, .vertical-table td {
                border: 1px solid #dddddd;
                padding: 8px;
            }
            .vertical-table th {
                background-color: #f2f2f2;
            }
            @media (max-width: 600px) {
                table {
                    display: block;
                }
                caption {
                    display: none;
                }
                thead {
                    display: none; /* 헤더 숨기기 */
                }
                tbody, tr, td {
                    display: block;
                    width: 100%;
                }
                tr {
                    margin-bottom: 16px; /* 각 데이터 그룹 간 간격 */
                }
                td {
                    position: relative;
                    padding-left: 50%; /* 헤더를 가상으로 표시할 공간 */
                }
            }
        </style>
    </head>
    <body style='font-family: Arial, sans-serif;'>
    '''

    html += f'''
        <table class='vertical-table' style='width: 100%; border-collapse: collapse; margin: 20px 0;'>
            <caption style='font-size: 15px; font-weight: bold; color: #333; text-align: center; margin-bottom: 10px;'>{subject}</caption>
            <thead>
                <tr>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 8px;'>No</th>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 8px;'>출처</th>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 8px;'>타입</th>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 8px;'>Title</th>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 8px;'>Date</th>
                </tr>
            </thead>
            <tbody>
    '''
    for i, result in enumerate(results):
        if result['title']:
            html += f'''
                <tr>
                    <td style='text-align: center; border: 1px solid #dddddd; padding: 8px; align-items: center;'>{i + 1}</td>
                    <td style='text-align: center; border: 1px solid #dddddd; padding: 8px; align-items: center;'>{result['source']}</td>
                    <td style='text-align: center; border: 1px solid #dddddd; padding: 8px; align-items: center;'>{result['kind']}</td>
                    <td style='border: 1px solid #dddddd; padding: 8px; align-items: center;'>
                        <a href={result['href']}>{result['title']}</a>
                    </td>                                                                                     
                    <td style='text-align: center; border: 1px solid #dddddd; padding: 8px; align-items: center;'>{result['date']}</td>
                </tr>
            '''
    html += '''
            </tbody>
        </table>
    </body>
    </html>
    '''

    return html 
 