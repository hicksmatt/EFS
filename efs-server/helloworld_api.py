"""API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import os
import base64
import httplib2
import StringIO

from apiclient import errors
from apiclient.http import MediaIoBaseUpload
from apiclient.http import MediaFileUpload
from apiclient import discovery
from google.appengine.ext import db
from oauth2client.appengine import StorageByKeyName
from oauth2client.appengine import CredentialsProperty
from google.appengine.api import oauth
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.client import AccessTokenCredentials
import dropbox



WEB_CLIENT_ID = 'replace this with your web client ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPE = 'https://www.googleapis.com/auth/drive'

package = 'Hello'
class CredentialsModel(db.Model):
  credentials = CredentialsProperty()

class FileUpload(messages.Message):
    """Full on FILE"""
    user = messages.StringField(1)
    filename = messages.StringField(2)
    filedata = messages.StringField(3)

class FileRequest(messages.Message):
    filename = messages.StringField(1)
    
class FileDownload(messages.Message):
    user = messages.StringField(1)
    filename = messages.StringField(2)
    filedata = messages.StringField(3)

class FileResponse(messages.Message):
    user = messages.StringField(1)
    filename = messages.StringField(2)
    filedata = messages.StringField(3)

@endpoints.api(name='helloworld', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[SCOPE, endpoints.EMAIL_SCOPE])
class HelloWorldApi(remote.Service):
  """helloworld API v1."""

  LOCATION_RESOURCE = endpoints.ResourceContainer(
      FileUpload,
      times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                  required=True))
  @endpoints.method(LOCATION_RESOURCE, FileResponse,
                    path='file/{times}', http_method='POST',
                    name='file.authed')
  def file_authed(self, request1):
    if request1.times == 1:
        
        current_user = endpoints.get_current_user()
        if "HTTP_AUTHORIZATION" in os.environ:
          (tokentype, token)  = os.environ["HTTP_AUTHORIZATION"].split(" ")

        credentials = AccessTokenCredentials(token, 'my-user-agent/1.0')
        http = httplib2.Http()
        #http = credentials.authorize(http)

        service = discovery.build('drive', 'v2', http=http)
        #storage = StorageByKeyName(CredentialsModel, current_user.user_id(), 'credentials')
        #credentials = storage.get()
        http = credentials.authorize(http)
        
        body = {'title':request1.filename,
                'description':'Encrypted',
                'mimeType':'text/plain'}

        media_body = MediaIoBaseUpload(StringIO.StringIO(request1.filedata), 'text/plain',resumable=False)
        
        
        results = service.files().insert(body=body,media_body=media_body).execute()
        
        fileReturn = FileResponse()
        fileReturn.filename = request1.filename
        fileReturn.filedata = request1.filedata
        fileReturn.user = (current_user.email() if current_user is not None
                 else 'Anonymous')
        return fileReturn #Greeting(message='hello %s' % (email,))
    else:
        dbx = dropbox.Dropbox('REPLACE THIS WITH YOUR DROPBOX API KEY')
        #dbx.users_get_current_account()
        fileplus = '/'+request1.filename+'.txt'
        dbx.files_upload(StringIO.StringIO(request1.filedata),fileplus)
        fileReturn = FileResponse()
        fileReturn.filename = request1.filename
        fileReturn.filedata = request1.filedata
        fileReturn.user = (current_user.email() if current_user is not None
         else 'Anonymous')
        return fileReturn



  FILE_RESOURCE = endpoints.ResourceContainer(
      FileRequest,
      times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                  required=True))
  @endpoints.method(FILE_RESOURCE, FileResponse,
                    path='fileask/{times}', http_method='POST',
                    name='fileask.authed')
  def fileask_authed(self, request1):
    if request1.times == 1:
        
        current_user = endpoints.get_current_user()
        if "HTTP_AUTHORIZATION" in os.environ:
          (tokentype, token)  = os.environ["HTTP_AUTHORIZATION"].split(" ")

        credentials = AccessTokenCredentials(token, 'my-user-agent/1.0')
        http = httplib2.Http()
        #http = credentials.authorize(http)

        service = discovery.build('drive', 'v2', http=http)
        #storage = StorageByKeyName(CredentialsModel, current_user.user_id(), 'credentials')
        #credentials = storage.get()
        http = credentials.authorize(http)
        items = service.files().list(q="title = '" + request1.filename + "'").execute()['items']
        #drive_files = service.files().list(q="title = 'dan'").execute()
        download_url = items[0].get('downloadUrl')
        resp, content = service._http.request(download_url)

        fileReturn = FileResponse()
        fileReturn.filename = request1.filename
        fileReturn.filedata = content
        fileReturn.user = (current_user.email() if current_user is not None
                 else 'Anonymous')
        return fileReturn #Greeting(message='hello %s' % (email,))
    else:
        dbx = dropbox.Dropbox('REPLACE THIS WITH YOUR DROPBOX API KEY')
        #dbx.users_get_current_account()
        fileplus = '/'+request1.filename+'.txt'
        dbx.files_upload(StringIO.StringIO(request1.filedata),fileplus)
        fileReturn = FileResponse()
        fileReturn.filename = request1.filename
        fileReturn.filedata = request1.filedata
        fileReturn.user = (current_user.email() if current_user is not None
         else 'Anonymous')
        return fileReturn

APPLICATION = endpoints.api_server([HelloWorldApi])
