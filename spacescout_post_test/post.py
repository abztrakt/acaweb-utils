""" post.py - 8/24/16 by cstimmel. Simple script for testing concurrent posts
to spotseeker_server.
"""
import json
import random
import requests
from requests_oauthlib import OAuth1
import settings


def get_spot(spot_id):
    auth = OAuth1(settings.KEY, settings.SECRET)
    url = "{0}/api/v1/spot/{1}".format(settings.URL, spot_id)
    response = requests.get(url, auth=auth)
    return response


def post_to_spot(spot_id, response):
    auth = OAuth1(settings.KEY, settings.SECRET)
    url = "{0}/api/v1/spot/{1}".format(settings.URL, spot_id)
    data =  json.loads(response.content)
    etag = data['etag']
    print "GET etag: {0}".format(etag)
    rand = random.randrange(0,9999)
    data["extended_info"]["random_int"] = rand
    data = json.dumps(data)
    print data
    headers = {'X-OAuth-User': settings.USER,
               'If-Match': etag,
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    response2 = requests.put(url, auth=auth, data=data, headers=headers)
    print response2
    print response2.content


def main():
    resp = get_spot(settings.SPOT)
    post_to_spot(settings.SPOT, resp)


if __name__ == "__main__":
    main()
