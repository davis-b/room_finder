import requests
import json

default_header = {'User-Agent':"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

default_api_url = 'https://studentenplatformapi.hexia.io/api/v1/actueel-aanbod'

def request_listings(api_endpoint=default_api_url, region_id=3) -> dict:
	# Region id 3 == Amsterdam
	# To discover a different region id, use the filter functionality of
	# the website, and look at the "hexia.io" Post->Request json data
	# (sent over the network).
	params = {
		'limit':'60',
		'locale':'en_GB',
		'page':'0',
		'sort':'-publicationDate'
		''
	}
	
	filters = {"filters":{"$and":[{"$and":[{"regio.id":{"$eq":str(region_id)}}]}]},"hidden-filters":{"$and":[{"dwellingType.categorie":{"$eq":"woning"}},{"isExtraAanbod":{"$eq":""}},{"isWoningruil":{"$eq":""}},{"$and":[{"$or":[{"street":{"$like":""}},{"houseNumber":{"$like":""}},{"houseNumberAddition":{"$like":""}}]},{"$or":[{"street":{"$like":""}},{"houseNumber":{"$like":""}},{"houseNumberAddition":{"$like":""}}]}]},{"rentBuy":{"$eq":"Huur"}}]}}
	opts_response = requests.options(api_endpoint, params=params)
	response = requests.post(api_endpoint, headers=default_header, params=params, json=filters)
	if not response.ok:
		raise EnvironmentError('HTML request did not succeed. Return code = {}'.format(response.status_code))
	return response.json()

def expand_urlkey(key) -> str:
	return 'https://www.room.nl/en/offerings/to-rent/details/' + str(key)

def process_listings(raw_listing_response):
	listings = raw_listing_response['data']
	misc_types = ['dwellingType', 'heating', 'sleepingRoom', 'kitchen', 'floor']
	for l in listings:
		misc = [i.get('naam_en_GB') for i in (l.get(j) for j in misc_types) if i]

		yield {
			'street': l.get('street'),
			'house_number': l.get('houseNumber'),
			'postal_code': l.get('postalcode'),
			'city': l.get('city', {}).get('name'),
			# 'municipality': l.get('municipality', {}).get('name'),
			'posted_on': l.get('publicationDate', '')[:10],
			'closing_on': l.get('closingDate', '')[:10],
			'can_move_in_on': l.get('availableFromDate', '')[:10],
			'total_rent': l.get('totalRent'),
			'latitude': l.get('latitude'),
			'longitude': l.get('longitude'),
			'construction_year': l.get('constructionYear'),
			'misc': misc,
			'id': str(l.get('id', '?')),
			'url': expand_urlkey(l.get('urlKey', 'no_url_key'))
		}

def stringify_processed_listing(listing):
	result = ''
	longest = max(map(len, listing.keys()))
	for k, v in listing.items():
		result += '{}{}\t{}\n'.format(k, (longest + 5 - len(k)) * ' ', v)
	return result 

if __name__ == '__main__':
	for i in process_listings(request_listings()):
		print(stringify_processed_listing(i))