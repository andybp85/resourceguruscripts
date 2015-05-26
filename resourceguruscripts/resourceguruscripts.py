"""ResourceGuru API Python wrapper wrapper for back-end scripts

This module wraps the ResourceGuru Api using OAuth2 BackendApplicationClient and Basic Auth to allow automated scripts access.

Import:

    from resourceguruscripts import ResourceGuruScripts

Init:

    ResourceGuruScripts( account, client_id, client_secret, username, password )

Methods:

#1: Clients
    getClients(limit=0, offset=0, archived=False)
    setClient(name)
    addClient(name, notes=False):
    updateClient(client_id, name=False, notes=False)
    deleteClient(client_id)

#2: Projects
    getProjects(limit=0, offset=0, archived=False)
    setProject(name, project_notes, client)
    addProject(name, notes=False, client=False, client_id=False)
    updateProject(proj_id, name=False, archived=False, notes=False, client_id=False)
    deleteProject(proj_id)

#3: Bookings
    getBookings(start_date=False, end_date=False, project=False, client=False, resource=False, limit=0, offset=0, booker_id=False)
    addBooking(start_date, resource, project, project_notes, client, client_notes, details=False, duration=1)
    updateBooking(booking_id, resource=False, start_date=False, project=False, client=False, duration=1,)
    deleteBooking(booking_id)

#4: webhooks
    getWebhooks()
    setWebhook(name, payload_url, events, secret=False)
    updateWebhook(webhook_id, name=False, payload_url=False, events=False, secret=False):
    deleteWebhook(self, webhook_id)

#5: Other
    getResources(limit=0, offset=0, archived=False)
    getOneByName(endpoint, name, client_id=False, limit=0, offset=0, archived=False)
    getNameById(endpoint, item_id)
    simple_list(endpoint, limit=0, offset=0, archived=False):

#6: Session Handling
    _start_session(client_id, client_secret, redirect_uri, username, password)
    _token_updater(token)

"""
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from urllib import urlencode
import pickle, sys, os.path, time

class ResourceGuruScripts(object):
    RESOURCEGURU = 'https://api.resourceguruapp.com/'
    TOKEN_URI = RESOURCEGURU + 'oauth/token'
    API = 'v1'
    API_URI = RESOURCEGURU + API

    def __init__(self, account, client_id, client_secret, username, password, redirect_uri=False):
        """
        Initializes the hook with OAuth2 parameters.
        """
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

    def getClients(self, limit=0, offset=0, archived=False):
        """
        Get all projects
        Returns json
        """
        return self.simple_list('clients', limit=limit, offset=offset, archived=archived)

    def setClient(self, name, notes=False):
        """
        Checks if a client exists, if not creates it
        Returns ID
        """
        response = self.getOneByName('clients', name)

        if not response:
            return self.addClient(name, notes)
        else:
            return response

    def addClient(self, name, notes=False):
        """
        Add client
        Returns ID
        """
        data = {'name' : name}
        if notes:
            data["notes"] = notes

        response = self.oauth.post(self.base_uri + 'clients/', data=data)

        if response.status_code == 404:
            return False
        else:
            resData = response.json()
            return resData["id"]

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

        return self.oauth.put(self.base_uri + 'clients/' + str(client_id), data=data).json()

    def deleteClient(self, client_id):
        """
        Delete single client by ID
        Returns True if success, False if not
        """
        response = self.oauth.delete(self.base_uri + 'clients/' + str(client_id))

        if response.status_code == 204:
            return True
        else:
            return False


#2:  projects funcs

    def getProjects(self, limit=0, offset=0, archived=False):
        """
        Get all projects
        Returns json
        """
        return self.simple_list('projects', limit=limit, offset=offset, archived=archived)


    def setProject(self, name, project_notes, client):
        """
        Checks if project exists, if not creates it
        Returns ID
        """
        client_id= self.getOneByName('clients', client)
        response = self.getOneByName('projects', name, client_id)

        if not response:
            return self.addProject(name, notes=project_notes, client_id=client_id)
        else:
            return response

    def addProject(self, name, notes=False, client=False, client_id=False):
        """
        Add a project by name (and client if applicable)
        Returns an ID
        """
        if client:
            client_id = self.setClient(client)
            data = {'name'      : name,
                    'client_id' : client_id}
        elif client_id:
            data = {'name'      : name,
                    'client_id' : client_id}
        else:
            data = {'name' : name}

        if notes:
            data['notes'] = notes

        response = self.oauth.post(self.base_uri + 'projects/', data=data).json()

        return response["id"]

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

        return self.oauth.put(self.base_uri + 'projects/' + str(proj_id), data=data).json()

    def deleteProject(self, proj_id):
        """
        Delete single project by ID
        Returns True if success, False if not
        """
        response = self.oauth.delete(self.base_uri + 'projects/' + str(proj_id))

        if response.status_code == 204:
            return True
        else:
            return False


#3: bookings funcs

    def getBookings(self, start_date=False, end_date=False, project=False, client=False, resource=False, limit=0, offset=0, booker_id=False):
        """
        Get bookings by dates, project, client, or resource
        Returns json or False
        """
        params = {'limit' : limit, 'offset' : offset}

        if start_date and end_date:
            params['start_date'] = start_date
            params['end_date'] = end_date
            response = self.oauth.get(self.base_uri + 'bookings', params=params)

        if project:
            response = self.oauth.get(self.base_uri + 'projects/' + str(self.getOneByName('projects', project)) + '/bookings')
        if client:
            response = self.oauth.get(self.base_uri + 'clients/' + str(self.getOneByName('clients', client)) + '/bookings')
        if resource:
            response = self.oauth.get(self.base_uri + 'resources/' + str(self.getOneByName('resources', resource)) + '/bookings')

        if response and response.status_code == 200:
            return response.json()

        return False


    def addBooking(self, start_date, resource, project, project_notes, client, client_notes, details=False, duration=1):
        """
        Adds a booking
        Returns json or False
        """
        data = {'start_date'    : start_date,
                'end_date'      : start_date,
                'duration'      : duration,
                'allow_waiting' : 'true'}

        data['client_id']   = self.setClient(client, client_notes)
        data['project_id']  = self.setProject(project, project_notes, client)
        data['resource_id'] = self.getOneByName('resources', resource)

        if details:
            data["details"] = details
        response = self.oauth.post(self.base_uri + 'bookings', data=data)

        if response.status_code != 201:
            return False

        return response.json()

    def updateBooking(self, booking_id, resource=False, start_date=False, project=False, client=False, duration=1,):
        """
        Update a booking
        Returns json or False

        self.updateBooking( booking_id, [resource_name], [start_date], [project_name], [client_name], [duration] )
        """
        data =  {}

        if start_date:
            data["start_date"] = start_date
        if duration:
            data["duration"] = duration
        if client:
            data['client_id'] = self.setClient(client, client_notes)
        if project:
            data['project_id'] = self.setProject(project, client)
        if resource:
            data['resource_id'] = self.getOneByName('resources', resource)
        if not data:
            return False

        response = self.oauth.put(self.base_uri + 'bookings/' +  str(booking_id), data=data)

        return response.json()

    def deleteBooking(self, booking_id):
        """
        Delete single booking by ID
        Returns True if success, False if not
        """
        response = self.oauth.delete(self.base_uri + 'bookings/' +  str(booking_id))

        if response.status_code == 204:
            return True
        else:
            return False

#4: webhooks

    def getWebhooks(self):
        """
        Gets all webhooks.
        Returns JSON
        """
        response = self.ouath.get(self.base_uri + 'webhooks')
        return response.json()

    def setWebhook(self, name, payload_url, events, secret=False):
        """
        Sets a webhook. Can pass secret stored in session.
        Returns JSON

        self.setWebhook(name, payload_url, events(Array), [secret(Bool)] )
        """
        data = {'name'        : name,
                'payload_url' : payload_url,
                'events[]'      : events}

        if secret:
            data['secret'] = self.secret

        response = self.oauth.post(self.base_uri + 'webhooks', data)

        return response.json()

    def updateWebhook(self, webhook_id, name=False, payload_url=False, events=False, secret=False):
        """
        Update a webhook. Can pass secret stored in session.
        Returns True if success, False if no parameters or JSON if error

        self.updateWebhook(webhook_id, [name], [payload_url], [events(Array)], [secret(Bool)] )
        """
        data = {}

        if name:
            data['name'] = name
        if payload_url:
            data['payload_url'] = payload_url
        if events:
            data['events[]'] = events
        if not data:
            return False

        if secret:
            data['secret'] = self.secret

        response = self.oauth.put(self.base_uri + 'webhooks/' + webhook_id, data)

        if response.status_code == 201:
            return True

        return response.json()


    def deleteWebhook(self, webhook_id):
        """
        Deletes a webhook
        Returns True if success or JSON if error

        self.deleteWebhook(id)
        """
        response = self.oauth.delete(self.base_uri + 'webhooks/' + webhook_id)

        if response.status_code == 201:
            return True

        return response.json()

#5: Other funcs

    def getResources(self, limit=0, offset=0, archived=False):
        """
        Get all reouces
        Returns json
        """
        return self.simple_list('resources', limit=limit, offset=offset, archived=archived)

    def getOneByName(self, endpoint, name, client_id=False, limit=0, offset=0, archived=False):
        """
        Get one of something by name (and client if applicable). Doesn't work for bookings - no name!
        Returns an ID or False

        self.get_one( name, projects|clients|resources|etc...,[client id], [limit], [offset], [archived])
        """
        params = {'limit'    : limit,
                  'offset'   : offset,
                  'archived' : archived}

        if endpoint == 'bookings':
            return False

        response = self.oauth.get(self.base_uri + endpoint, params=params)

        if response.status_code == 404:
            return response['errors']

        if client_id:
            for field in response.json():
                if field["name"] == name and field["client_id"] == client_id:
                    return field['id']
        else:
            for field in response.json():
                if field["name"] == name:
                    return field['id']

    def getNameById(self, endpoint, item_id):
        """
        Get client or project name by ID
        Return name or False
        """
        response = self.oauth.get(base_uri + endpoint + '/' + item_id).json()

        try:
            return response["name"]
        except:
            return False

    def simple_list(self, endpoint, limit=0, offset=0, archived=False):
        """
        Accesses any simple list based API endpoint, returning a dictionary of
        dictionaries keyed by the item ID.
        """
        params = { 'limit'  : limit, 'offset' : offset }

        if archived:
            suffix = '/archived'
        else:
             suffix = ''

        response = self.oauth.get(self.base_uri + endpoint + suffix, params=params)
        content = response.json()

        # Create a dictionary indexed by item ID instead of a flat list.
        data = {item['id']:item for item in content}
        return data

#6:  Session Handling

    def _start_session(self, client_id, client_secret, redirect_uri, username, password):
        self.secret = client_secret

        data = {'username'              : username,
                'client_secret'         : client_secret,
                'password'              : password,
                'grant_type'            : 'password',
                'client_id'             : client_id }

        response = self.oauth.post(self.TOKEN_URI, data)
        self._token_updater(response.json())

    def _token_updater(self, token):
        pickle.dump(token, open('token.p', "wb"))
        self.token = token

