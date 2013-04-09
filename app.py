#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage: 
python app.py <username>
"""
import json
import os
import sys
import requests
	
def crawl(username, photos=[], max_id=None):
	url   = 'http://instagram.com/' + username + '/media' + ('?&max_id=' + max_id if max_id is not None else '')
	media = json.loads(requests.get(url).text)
	
	for photo in media['items']:
		photos.append(photo['images']['standard_resolution']['url'])

	if 'more_available' not in media or media['more_available'] is False:
		return photos
	else:
		max_id = media['items'][-1]['id']
		return crawl(username, photos, max_id)
	
def download(url, save_dir='./'):
	if not os.path.exists(save_dir):
		os.makedirs(save_dir)
	
	base_name = url.split('/')[-1]
	file_path = os.path.join(save_dir, base_name)
	
	with open(file_path, 'wb') as file:
		print 'Downloading ' + base_name
		bytes = requests.get(url).content
		file.write(bytes)

if __name__ == '__main__':
	for url in crawl(sys.argv[1]): 
		download(url)


