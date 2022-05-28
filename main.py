
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
		return {}
	with open(filepath) as fileobj:
		return json.load(fileobj)

def save_db(listings, filepath=thisdir(db_filename)):
	with open(filepath, 'w') as fileobj:
		json.dump(listings, fileobj)

def log_err(error):
	with open(thisdir('errors.log'), 'a') as fileobj:
		date = datetime.fromtimestamp(time())
		fileobj.write('{}\n{}\n\n'.format(date, error))

def _main(email, email_recipient):
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

def main(email_username, email_password, email_recipient):
	email = emailer.login(email_username, email_password)
	try:
		_main(email, recipient)
	except Exception as e:
		raise e
	finally:
		email.logout()

if __name__ == '__main__':
	try:
		username = argv[1]
		password = argv[2]
		recipient = argv[3]
	except IndexError:
		print(path.basename(__file__), '[email_username] [email_password] [recipient_address]')
		quit()
	main(username, password, recipient)
