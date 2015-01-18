#!/usr/bin/env python
""" bulk delete Zendesk users based on search filter """

import argparse
import json
import pycurl
from StringIO import StringIO


# Zendesk API URL
apiurl = 'https://somedomain.zendesk.com/api/v2/users/'

# Zendesk API credentials
apiuser = ''
apipass = ''

# parse parameters and options
parser = argparse.ArgumentParser(description='bulk delete Zendesk users based on search filter')

parser.add_argument('--search-filter',
                    dest='searchfilter',
                    help='search filter',
                    required=True)

args = parser.parse_args()

searchfilter = args.searchfilter


# retrieve from API
def get_search_results(searchfilter):

    # create a buffer for the HTTP stream
    buffer = StringIO()

    # create PycURL object and retrieve JSON
    c = pycurl.Curl()
    c.setopt(c.URL, apiurl + 'search.json?query=' + searchfilter)
    c.setopt(pycurl.USERPWD, '%s:%s' % (apiuser, apipass))
    c.setopt(pycurl.CONNECTTIMEOUT, 30)
    c.setopt(pycurl.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()

    # get the JSON from the buffer
    userjson = json.loads(buffer.getvalue())

    return userjson


# delete using API
def del_user_ids(userjson):

    # loop through each user and delete it
    for user in userjson["users"]:
        print 'Deleting user ID: %s with email: %s' % (user['id'], user['email'])

        # create a buffer for the HTTP stream
        buffer = StringIO()

        # create PycURL object and send id to delete
        c = pycurl.Curl()
        c.setopt(c.URL, apiurl + str(user['id']) + '.json')
        c.setopt(pycurl.USERPWD, '%s:%s' % (apiuser, apipass))
        c.setopt(pycurl.CONNECTTIMEOUT, 30)
        c.setopt(pycurl.TIMEOUT, 30)
        c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()
        c.close()


# main
if __name__ == "__main__":
    (userjson) = get_search_results(searchfilter)
    del_user_ids(userjson)
