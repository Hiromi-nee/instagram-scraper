#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage: 
python app.py <username>
"""
import json
import os
import requests
import sys
import concurrent.futures

def crawl(username, items=[], max_id=None):
    url   = 'http://instagram.com/' + username + '/media' + ('?&max_id=' + max_id if max_id is not None else '')
    media = json.loads(requests.get(url).text)

    items.extend( [ curr_item[ curr_item['type'] + 's' ]['standard_resolution']['url'] for curr_item in media['items'] ] )

    if 'more_available' not in media or media['more_available'] is False:
        return items
    else:
        max_id = media['items'][-1]['id']
        return crawl(username, items, max_id)

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
  username = sys.argv[1]
  
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_url = dict( (executor.submit(download, url, './' + username), url) for url in crawl(username) )
  
    for future in concurrent.futures.as_completed(future_to_url):
      url = future_to_url[future]
      
      if future.exception() is not None:
        print '%r generated an exception: %s' % (url, future.exception())

