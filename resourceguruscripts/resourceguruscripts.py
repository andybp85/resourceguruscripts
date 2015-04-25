"""A module that wraps the resourceguruapp.com API"""

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
from datetime import date
import pickle, json, urllib

import pprint as pp

class ResourceGuruScripts(object):
    RESOURCEGURU = 'https://api.resourceguruapp.com/'
    TOKEN_URI = RESOURCEGURU + 'oauth/token'
    #AUTHORIZE_URI = RESOURCEGURU + 'oauth/authorize'
    API = 'v1'
    API_URI = RESOURCEGURU + API


    def __init__(self, account, client_id, client_secret, username, password, redirect_uri=False):
        """
        Initializes the hook with OAuth2 parameters.
        """
        self.client_secret = client_secret
        self.base_uri = self.API_URI + '/' + account + '/'
        try:
            self.token = pickle.load(open('token.p', "rb"))
        except:
            self.token = []
            self.start_session(client_id, client_secret, redirect_uri, username, password)
        self.oauth = OAuth2Session(client_id           = client_id, \
                                   auto_refresh_url    = self.TOKEN_URI, \
                                   auto_refresh_kwargs = ['client_id', 'client_secret'], \
                                   token_updater       = self.token_updater(self.token), \
                                   token               = self.token)

    def start_session(self, client_id, client_secret, redirect_uri, username, password):
        """
        Requests an access token.
        """
        data = {'username'              : username, \
                'client_secret'         : client_secret, \
                'password'              : password, 'grant_type' : \
                'password', 'client_id' : client_id }

        response = self.oauth.post(self.TOKEN_URI, data)
        self.token_updater(json.loads(urllib.unquote(response.content)))

    def token_updater(self, token):
        """
        Helper function to persist and update token cache.
        """
        pickle.dump(token, open('token.p', "wb"))
        self.token = token


    """

    Setters and Gettters

    """


    def simple_list(self, endpoint, limit=50, offset=0, archived=False):
        """
        Accesses any simple list based API endpoint, returning a dictionary of
        dictionaries keyed by the item ID.
        """
        params = {'limit'         : limit,
                  'offset'        : offset}

        suffix = ''
        if archived:
            suffix = '/archived'
        import pdb; pdb.set_trace()
        response = self.oauth.get(self.base_uri + endpoint + suffix, params=params)
        json = response.json()
        # Create a dictionary indexed by item ID instead of a flat list.
        data = {item['id']:item for item in json}
        return data




    def get_bookings(self, start_date, end_date, limit=50, offset=0, booker_id=False):
        params = {'start_date' : start_date.isoformat(), \
                  'end_date'   : end_date.isoformat(), \
                  'limit'      : limit, \
                  'offset'     : offset}

        if booker_id:
            params['booker_id'] = booker_id
        #response = self.oauth.get(self.base_uri + 'bookings', params=params)
        return response.json()

    def set_booking(self, start_date, resource_id, duration=1, project_id=False, client_id=False):
        data = {'start_date': start_date.isoformat(), 'resource_id' : resource_id, 'duration' : duration }
        if project_id:
            data['project_id'] = project_id
        if client_id:
            data['client_id'] = client_id
        #response = self.oauth.post(self.base_uri + 'bookings', data=params)
        return response.json()


    def update_booking(self, booking_id, start_date, resource_id, duration=1, project_id=False, client_id=False):
        params = {'booking_id' : booking_id, 'start_date': start_date.isoformat(), 'resource_id' : resource_id, 'duration' : duration }
        if project_id:
            data['project_id'] = project_id
        if client_id:
            data['client_id'] = client_id
        #response = self.oauth.put(self.base_uri + 'bookings', params=params)
        return response.json()




    def get_project(self, in_name):
        #response = self.oauth.get(self.base_uri + 'projects')
        pprint.pprint(response)

    def get_resources(self, limit=50, offset=0, archived=False):
        return self.simple_list('resources', limit=limit, offset=offset, archived=archived)

    def get_clients(self, limit=50, offset=0, archived=False):
        return self.simple_list('clients', limit=limit, offset=offset, archived=archived)

    def get_projects(self, limit=50, offset=0, archived=False):
        return self.simple_list('projects', limit=limit, offset=offset, archived=archived)


    def get_resource(self, id):
        response = self.oauth.get(self.base_uri + 'resources/' + id)
        return response.json()

'''

    def authorization_url(self):
        """
        Returns the url to redirect the user to for user consent.
        """
        authorization_url, state = self.oauth.authorization_url(self.AUTHORIZE_URI)
        return authorization_url
'''
