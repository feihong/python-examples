import os
from stamps.config import StampsConfiguration
from stamps.services import StampsService


kwargs = dict(zip(('integration_id', 'username', 'password'), os.environ['STAMPS_PARAMS'].split(';')))
configuration = StampsConfiguration(wsdl='testing', **kwargs)
service = StampsService(configuration=configuration)
account = service.get_account()
import ipdb; ipdb.set_trace()
