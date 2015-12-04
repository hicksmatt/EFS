#Encrypted File Storage (EFS) 

EFS is comprised of two applications. The first implements a backend for passing encrypted files to Google Drive and the second is front end that handles the encryption of selected files. The backend uses Google Cloud Endpoints, App Engine, and Python. The frontend client uses HTML5, JavaScript, and the forge encryption suite.

## Setup Instructions

1. Make sure to have the [App Engine SDK for Python][4] installed, version
   1.7.5 or higher.
2. Change `'YOUR-CLIENT-ID'` in [`index.html`][5] (2x places) and 
   [`helloworld_api.py`][6] (1x places) to the respective client ID(s) you have registered 
   in the [APIs Console][7].
3. Update the value of `application` in the server [`app.yaml`][8] and the client [`app.yaml`][8] files to the app IDs you have registered in the App Engine admin console
4. Update both applications by running `appcfg.py update [directory]` for both applications. 
5. Test your Endpoints by visiting the Google APIs Explorer: 
  `your-app-id.appspot.com/_ah/api/explorer`

[1]: https://developers.google.com/appengine
[2]: http://python.org/
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://developers.google.com/appengine/downloads
[5]: https://github.com/hicksmatt/EFS/blob/master/efs-client/index.html
[6]: https://github.com/hicksmatt/EFS/blob/master/efs-server/helloworld_api.py
[7]: https://code.google.com/apis/console
[8]: https://github.com/hicksmatt/EFS/blob/master/efs-server/app.yaml
[9]: https://github.com/hicksmatt/EFS/blob/master/efs-client/app.yaml
