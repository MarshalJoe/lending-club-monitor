import datetime
import os
import config
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = config.smtp_server
SMTP_LOGIN = config.smtp_login
SMTP_PASS = config.smtp_pass
EMAIL = config.email

def email_file(img_filename, email_text):
	d = datetime.datetime.now()
	header = "Lending Club Release - {0}/{1}/{2}".format(d.month, d.day, d.year)
	text = "{0}:00".format(d.hour)
	img_data = open(img_filename, 'rb').read()
	msg = MIMEMultipart()
	msg['Subject'] = header
	msg['From'] = 'me'
	msg['To'] = 'me'
	text = MIMEText(email_text)
	msg.attach(text)
	image = MIMEImage(img_data, name=os.path.basename(img_filename))
	msg.attach(image)
	s = smtplib.SMTP(SMTP_SERVER)
	s.ehlo()
	s.login(SMTP_LOGIN, SMTP_PASS)
	s.sendmail('joe', EMAIL, msg.as_string())
	s.quit()