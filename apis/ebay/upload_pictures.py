"""
Uploads all .jpg files in the current directory to eBay.

"""
import re
import os
from pathlib import Path
from pprint import pprint
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

imgfiles = [f for f in Path('.').iterdir() if f.suffix == '.jpg']

for imgfile in enumerate(imgfiles):
    files = {'file': ('EbayImage', imgfile.open('rb'))}

    try:
        response = api.execute('UploadSiteHostedPictures', {
            'WarningLevel': 'High',
            'PictureName': imgfile.stem,
        }, files=files)
        pprint(response.dict())
        details = response.reply.SiteHostedPictureDetails
        print('URL: ' + details.FullURL)
        print('Use by date: ' + details.UseByDate)
    except ConnectionError as ce:
        print(ce)
        pprint(ce.response.dict())
