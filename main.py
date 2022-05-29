
import json
from os import path
from sys import argv
from time import time
from datetime import datetime

import searcher, emailer

db_filename = 'seen.json'

def thisdir(filename):
	return path.join(path.dirname(path.abspath(__file__)), filename)

def load_db(filepath=thisdir(db_filename)):
	if not path.exists(filepath):
		return set()
	with open(filepath) as fileobj:
		try:
			db_contents = json.load(fileobj)
		except json.decoder.JSONDecodeError:
			return set()
		return set(db_contents)

def save_db(listings, filepath=thisdir(db_filename)):
	listings = list(set(listings))
	with open(filepath, 'w') as fileobj:
		json.dump(listings, fileobj)

def log_err(error):
	with open(thisdir('errors.log'), 'a') as fileobj:
		date = datetime.fromtimestamp(time())
		fileobj.write('{}\n{}\n\n'.format(date, error))

def _main(email, email_recipient):
	"""
	Searches for new housing listings.
	Prints new listings to stdout, and optionally
	emails them.
	"""
	seen_listings = load_db(db_filename)
	new_listings = {}
	print('starting with {} listings saved'.format(len(seen_listings)))

	for listing in searcher.process_listings(searcher.request_listings()):
		if listing['id'] not in seen_listings:
			new_listings[listing['id']] = listing

	if new_listings:
		print('found {} new listings'.format(len(new_listings)))
		body = ''
		for listing in new_listings.values():
			body += searcher.stringify_processed_listing(listing)
			body += '\n\n'
		body = body.strip()

		try:
			print(body)
			if email:
				email.send(email_recipient, 'New Housing Listing(s) : {}'.format(len(new_listings)), body)
			seen_listings.update(new_listings)
			save_db(seen_listings)
		except Exception as err:
			print(err)
			log_err(err)
	else:
		print('no new listings')

def main_with_email(email_info: dict):
	"""
	Email wrapper around the real main function.

	Takes a dict of email related information,
	or None if no emails are to be sent.

	Logs in, calls main, then logs out of the email client,
	"""
	email = emailer.login(
		email_info['username'],
		email_info['password'],
		domain=email_info.get('domain', 'smtp.gmail.com'),
		port=email_info.get('port', 587),
	)

	try:
		_main(email, email_info['recipient'])
	except Exception as e:
		raise e
	finally:
		email.logout()

if __name__ == '__main__':
	email_info = {}
	try:
		for index, key in enumerate(('username', 'password', 'recipient')):
			email_info[key] = argv[index + 1]
	except IndexError:
		print(path.basename(__file__), '[email_username] [email_password] [recipient_address] <email_domain> <email SMTP port>')
		quit()
	try:
		email_info['domain'] = argv[4]
		email_info['port'] = argv[5]
	except IndexError:
		pass
	main_with_email(email_info)
