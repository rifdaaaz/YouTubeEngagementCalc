import requests
from urllib import urlencode
import json
from subprocess import Popen

client_id = "615677142223-hcjeucs12o40tf2jaoeqs3t4e5kd267m.apps.googleusercontent.com"
client_secret = "0PPZlYAhe18vY4vqmvIlEDpu"
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
base_url = r"https://accounts.google.com/o/oauth2/"
authorization_code = ""
access_token = ""

"""
Retrieving authorization_code from authorization API.
"""
def retrieve_authorization_code():
  authorization_code_req = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": (r"https://www.googleapis.com/auth/userinfo.profile" +
              r" https://www.googleapis.com/auth/userinfo.email" +
              r" https://www.googleapis.com/auth/calendar")
    }

  r = requests.get(base_url + "auth?%s" % urlencode(authorization_code_req),
                   allow_redirects=False)
  print "下記URLを開いて、アクセス承認後に表示された文字列を入力してください。"
  url = r.headers.get('location')
  Popen(["open", url])

  authorization_code = raw_input("\nAuthorization Code >>> ")
  return authorization_code


"""
Retrieving access_token and refresh_token from Token API.
"""
def retrieve_tokens(authorization_code):
  access_token_req = {
    "code" : authorization_code,
    "client_id" : client_id,
    "client_secret" : client_secret,
    "redirect_uri" : redirect_uri,
    "grant_type": "authorization_code",
    }
  content_length=len(urlencode(access_token_req))
  access_token_req['content-length'] = str(content_length)

  r = requests.post(base_url + "token", data=access_token_req)
  data = json.loads(r.text)
  return data