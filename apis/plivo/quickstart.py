import os
import plivo

auth_id, auth_token, src = os.environ['PLIVO_PARAMS'].split(';')

api = plivo.RestAPI(auth_id, auth_token)

resp = api.send_message(dict(
    src=src,
    dst=os.environ['SMS_NUMBER'],
    text='Yay it works'
))

print(resp)
