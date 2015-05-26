ResourceGuruScripts
============

This module wraps the ResourceGuru Api using OAuth2 BackendApplicationClient and Basic Auth to allow automated scripts access.

Includes functionality to create, read, update, and delete bookings, clients, and projects 

Init:

    ResourceGuruScripts( account, client_id, client_secret, username, password )

Methods:

##1: Clients
    getClients(limit=0, offset=0, archived=False)
    setClient(name)
    addClient(name, notes=False):
    updateClient(client_id, name=False, notes=False)
    deleteClient(client_id)

##2: Projects
    getProjects(limit=0, offset=0, archived=False)
    setProject(name, project_notes, client)
    addProject(name, notes=False, client=False, client_id=False)
    updateProject(proj_id, name=False, archived=False, notes=False, client_id=False)
    deleteProject(proj_id)

##3: Bookings
    getBookings(start_date=False, end_date=False, project=False, client=False, resource=False, limit=0, offset=0, booker_id=False)
    addBooking(start_date, resource, project, project_notes, client, client_notes, details=False, duration=1)
    updateBooking(booking_id, resource=False, start_date=False, project=False, client=False, duration=1,)
    deleteBooking(booking_id)

##4: webhooks
    getWebhooks()
    setWebhook(name, payload_url, events, secret=False)
    updateWebhook(webhook_id, name=False, payload_url=False, events=False, secret=False):
    deleteWebhook(self, webhook_id)

##5: Other
    getResources(limit=0, offset=0, archived=False)
    getOneByName(endpoint, name, client_id=False, limit=0, offset=0, archived=False)
    getNameById(endpoint, item_id)
    simple_list(endpoint, limit=0, offset=0, archived=False):

##6: Session Handling
    _start_session(client_id, client_secret, redirect_uri, username, password)
    _token_updater(token)


