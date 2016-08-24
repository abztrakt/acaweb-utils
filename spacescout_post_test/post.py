""" post.py - 8/24/16 by cstimmel. Simple script for testing concurrent posts to spotseeker_server.
"""
import requests
from requests_oauthlib import OAuth1
import settings

def post_to_spot(spot_id):
    auth = OAuth1(settings.KEY, settings.SECRET)
    url = "{0}/api/v1/spot/{1}".format(settings.URL, spot_id)
    response = requests.get(url, auth=auth)
    print response.content

def main():
    post_to_spot(settings.SPOT)

if __name__ == "__main__":
    main()
