import smtplib
from email.mime.text import MIMEText

class Email:
	def __init__(self, email, username):
		self.email = email
		self.username = username

	def send(self, recipient: str, subject: str, body: str):
		encoded_body = MIMEText(body.strip().encode('utf-8'), _charset='utf-8')
		message = 'Subject: {}\n{}'.format(subject, encoded_body)
		self.email.sendmail(self.username, recipient, message)

	def logout(self):
		self.email.quit()

def login(username: str, password: str, domain: str, port: int) -> Email:
	email = smtplib.SMTP(domain, port)
	email.ehlo()
	email.starttls()
	email.login(username, password)
	return Email(email, username)