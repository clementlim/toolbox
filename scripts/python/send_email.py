import os
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_email(send_from, send_to, subject, text, files=[], server="xbox.financialcad.com"):
  assert type(send_to)==list
  assert type(files)==list

  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = COMMASPACE.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject

  msg.attach(MIMEText(text))

  for f in files:
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(f,"rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)

  smtp = smtplib.SMTP(server)
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()

if __name__ == '__main__':
  From = "automated.test.cradle@fincad.com"
  To = ["c.lim@fincad.com"]
  Subject = "Python generated email"
  testFile = os.path.join(os.environ.get("FINCAD_ROOT"), 'test', 'spreadsheets', 'xls', 'test_cradle.xls')
  testReport = os.path.join(os.environ.get("FINCAD_ROOT"), 'test', 'spreadsheets', 'xls', 'test_report.txt')
  Text = open(testReport,"rb").read()

  Attachments = [testFile, testFile2]
  
  send_email(From, To, Subject, Text, Attachments)