"""A module that wraps the resourceguruapp.com API"""

from requests_oauthlib import OAuth2Session
from datetime import date
import pickle

class ResourceGuru(object):
    RESOURCEGURU = 'https://api.resourceguruapp.com/'
    TOKEN_URI = RESOURCEGURU + 'oauth/token'
    AUTHORIZE_URI = RESOURCEGURU + 'oauth/authorize'
    API = 'v1'
    API_URI = RESOURCEGURU + API

    def __init__(self, account, client_id, client_secret, redirect_uri):
        """
        Initializes the hook with OAuth2 parameters.
        """
        self.client_secret = client_secret
        self.base_uri = self.API_URI + '/' + account + '/'
        try:
            self.token = pickle.load(open('token.p', "rb"))
        except FileNotFoundError:
            self.token = []
        self.oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, auto_refresh_url=self.TOKEN_URI, auto_refresh_kwargs=['client_id', 'client_secret'], token_updater=self.token_updater(self.token), token=self.token)

    def authorization_url(self):
        """
        Returns the url to redirect the user to for user consent.
        """
        authorization_url, state = self.oauth.authorization_url(self.AUTHORIZE_URI)
        return authorization_url

    def start_session(self, authorization_response):
        """
        Requests an access token.
        """
        self.token_updater(self.oauth.fetch_token(self.TOKEN_URI, client_secret=self.client_secret, authorization_response=authorization_response))
        return True

    def simple_list(self, endpoint, limit=50, offset=0, archived=False):
        """
        Accesses any simple list based API endpoint, returning a dictionary of
        dictionaries keyed by the item ID.
        """
        params = {'limit': limit, 'offset': offset}
        suffix = ''
        if archived:
            suffix = '/archived'
        response = self.oauth.get(self.base_uri + endpoint + suffix, params=params)
        json = response.json() 
        # Create a dictionary indexed by item ID instead of a flat list.
        data = {item['id']:item for item in json}
        return data

    def get_resources(self, limit=50, offset=0, archived=False):
        return self.simple_list('resources', limit=limit, offset=offset, archived=archived)

    def get_clients(self, limit=50, offset=0, archived=False):
        return self.simple_list('clients', limit=limit, offset=offset, archived=archived)

    def get_projects(self, limit=50, offset=0, archived=False):
        return self.simple_list('projects', limit=limit, offset=offset, archived=archived)

    def get_bookings(self, start_date, end_date, limit=50, offset=0, booker_id=False):
        params = {'start_date': start_date.isoformat(), 'end_date': end_date.isoformat(), 'limit': limit, 'offset': offset}
        if booker_id:
            params['booker_id'] = booker_id
        response = self.oauth.get(self.base_uri + 'bookings', params=params)
        return response.json() 

    def token_updater(self, token):
        """
        Helper function to persist and update token cache.
        """
        pickle.dump(token, open('token.p', "wb"))
        self.token = token
