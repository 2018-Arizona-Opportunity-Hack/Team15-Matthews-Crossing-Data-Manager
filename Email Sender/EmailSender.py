import json
import sys
import os

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


def send_email(toaddr, subject, body, filepath):
	config_data = None

	with open("email_config.json", "r") as f:
		config_data = json.load(f)

	fromaddr = config_data["From"]

	msg = MIMEMultipart()

	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject

	msg.attach(MIMEText(body, 'plain'))

	filename = os.path.basename(filepath)
	attachment = open(filepath, "rb")

	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

	msg.attach(part)

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, config_data["Password"])
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

if __name__ == '__main__':
	toaddr = sys.argv[1]
	subject = sys.argv[2]
	body = sys.argv[3]
	filepath = sys.argv[4]
	send_email(toaddr, subject, body, filepath)
