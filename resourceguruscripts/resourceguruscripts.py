"""A module that wraps the resourceguruapp.com API"""

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
#from oauthlib.oauth2 import TokenExpiredError
import pickle, json, urllib, iso8601
import os.path, time

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
        #self.client_secret = client_secret
        self.base_uri = self.API_URI + '/' + account + '/'
        try:
            token = pickle.load(open('token.p', "rb"))
            token['expires_in'] = token['expires_in'] - (int(time.time()) - int(os.path.getmtime('token.p')))
            self._token_updater(token)
        except:
            self.token = {}
        self.oauth = OAuth2Session(client_id           = client_id,
                                   auto_refresh_url    = self.TOKEN_URI,
                                   auto_refresh_kwargs = ['client_id', 'client_secret'],
                                   token_updater       = self._token_updater(self.token),
                                   token               = self.token)
        self._token_updater(self.oauth.token)
        self._start_session(client_id, client_secret, redirect_uri, username, password)


#1: clients funcs

    def getProjects(self, limit=0, offset=0, archived=False):
        """
        Get all projects
        Returns json
        """
        return self._simple_list('clients', limit=limit, offset=offset, archived=archived)

    def setClient(self, name):
        """
        Checks if a client exists, if not creates it
        Returns ID
        """
        response = self.getOneByName('clients', name)
        if not response:
            return self.addClient(name)
        else:
            return response

    def addClient(self, name):
        """
        Add client
        Returns ID
        """
        data = {'name' : name}
        response = json.dumps(self.oauth.post(self.base_uri + 'clients/', data=data))
        return respons["id"]

    def updateClient(self, client_id, name=False, notes=False):
        """
        Update a client
        Returns json or False
        """
        data = {}
        if name:
            data["name"] = name
        if notes:
            data["notes"] = notes
        if not data:
            return False
        return json.dumps(self.oauth.put(self.base_uri + 'clients/' + client_id, data=data))


#2:  projects funcs

    def getProjects(self, limit=0, offset=0, archived=False):
        """
        Get all projects
        Returns json
        """
        return self._simple_list('projects', limit=limit, offset=offset, archived=archived)


    def setProject(self, booking_id, name, client):
        """
        Checks if project exists, if not creates it
        Returns ID
        """
        response = self.getOneByName('project', name, client)
        if not response:
            return self.addProject(name, client)
        else:
            return response

    def addProject(self, name, client=False):
        """
        Add a project by name (and client if applicable)
        Returns an ID 
        """
        if client:
            client_id = self.set_client(client)
            data = {'name'      : name,
                    'client_id' : client_id}
        else:
            data = {'name' : name}
        response = json.dumps(self.oauth.post(self.base_uri + 'projects/', data=data))
        return respons["id"]

    def updateProject(self, proj_id, name=False, archived=False, notes=False, client_id=False):
        """
        Update a project
        Returns full json project representation of False

        self.updateProject( project_id, [name], [archived], [notes], [client_id] )
        """
        data = {}
        if name:
            data["name"] = name
        if archived:
            data["archived"] = archived
        if notes:
            data["notes"] = notes
        if client_id:
            data["client_id"] = client_id
        if not data:
            return False
        return json.dumps(self.oauth.put(self.base_uri + 'projects/' + proj_id, data=data))


#3: bookings funcs

    def getBookingsByDates(self, start_date, end_date, limit=0, offset=0, booker_id=False):
        """
        Get all bookings between two dates
        Returns json
        """
        params = {'start_date' : iso8601.parse_date(start_date),
                  'end_date'   : iso8601.parse_date(end_date),
                  'limit'      : limit,
                  'offset'     : offset}
        if booker_id:
            params['booker_id'] = booker_id
        return json.dumps(self.oauth.get(self.base_uri + 'bookings', params=params))

    def addBooking(self, start_date, resource, duration=1, project, client):
        """
        Adds a booking
        Returns json
        """
        data = {'start_date' : iso8601.parse_date(start_date), 
                'duration'   : duration }
        data['client_id']   = self.setClient(client)
        data['project_id']  = self.setProject(project, client)
        data['resource_id'] = self.getOneByName(resource, 'resources')
        response = self.oauth.post(self.base_uri + 'bookings', data=params)
        return json.dumps(response)


    def updateBooking(self, booking_id, resource=False, start_date=False, project=False, client=False, duration=1,):
        """
        Update a booking
        Returns json or False

        self.updateBooking( booking_id, [resource_name], [start_date], [project_name], [client_name], [duration] )
        """
        data =  {}
        if start_date:
            data["start_date"] = iso8601.parse_date(start_date)
        if duration:
            data["duration"] = duration
        if client:
            data['client_id']   = self.setClient(client)
        if project:
            data['project_id']  = self.setProject(project, client)
        if resource:
            data['resource_id'] = self.getOneByName(resource, 'resources')
        if not data:
            return False
        response = self.oauth.put(self.base_uri + 'bookings/' + booking_id, params=params)
        return json.dumps(response)


#4: Other funcs

    def getResources(self, limit=0, offset=0, archived=False):
        """
        Get all reouces
        Returns json
        """
        return self._simple_list('resources', limit=limit, offset=offset, archived=archived)

    def getOneByName(self, name, what, client_id=False, limit=0, offset=0, archived=False):
        """
        Get one of something by name (and client if applicable).
        Returns an ID or False

        self.get_one( name, projects|clients|bookings|resources|etc...,[client id], [limit], [offset], [archived])
        """
        params = {'limit'    : limit,
                  'offset'   : offset,
                  'archived' : archived}
        response = json.dumps(self.oauth.get(self.base_uri + what, params=params))
        if client_id:
            for r in response:
                if response["name"] == name and response["client_id"] == client_id:
                    return response['id']
        else:
            for r in response:
                if response["name"] == name:
                    return response['id']
        return 'False'

    def getNameById(self, endpoint, item_id):
        """
        Get client or project name by ID
        Return name or False
        """
        response = json.dumps(self.oauth.get(base_uri + endpoint + '/' + item_id))
        try:
            return response["name"]
        except:
            return False


#5: Plumbing funcs

    def _simple_list(self, endpoint, limit=0, offset=0, archived=False):
        """
        Accesses any simple list based API endpoint, returning a dictionary of
        dictionaries keyed by the item ID.
        """
        params = { 'limit'  : limit, 'offset' : offset }
        suffix = ''
        if archived:
            suffix = '/archived'
        response = self.oauth.get(self.base_uri + endpoint + suffix, params=params)
        #import pdb; pdb.set_trace()
        content = json.loads(response.content)
        # Create a dictionary indexed by item ID instead of a flat list.
        data = {item['id']:item for item in content}
        return data

    def _start_session(self, client_id, client_secret, redirect_uri, username, password):
        data = {'username'              : username,
                'client_secret'         : client_secret,
                'password'              : password,
                'grant_type'            : 'password',
                'client_id'             : client_id }


        response = self.oauth.post(self.TOKEN_URI, data)
        self._token_updater(json.loads(urllib.unquote(response.content)))

    def _token_updater(self, token):
        pickle.dump(token, open('token.p', "wb"))
        self.token = token


