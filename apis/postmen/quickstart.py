import os
from postmen import Postmen


api_key = os.environ['POSTMEN_API_KEY']
region = 'sandbox'


api = Postmen(api_key, region)
rates = api.get('rates')
