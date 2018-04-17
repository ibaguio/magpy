import os
import json
import logging
import requests

SANDBOX_URL = 'https://sandbox.api.magpie.im/v1'
PRODUCTION_URL = 'https://api.magpie.im/v1'


class MagpieRequest(object):
    def __init__(self, is_sandbox=False, **kwargs):
        self.is_sandbox = is_sandbox

        self.pk = os.environ.get('MAGPIE_PUBLIC_KEY', kwargs.get('pk'))
        self.sk = os.environ.get('MAGPIE_SECRET_KEY', kwargs.get('sk'))

        if not self.pk or not self.sk:
            raise Exception('Public or Secret Key not set in Environment')

        elif 'test' in self.pk:
            self.is_sandbox = True

        self.url = SANDBOX_URL if is_sandbox else PRODUCTION_URL

        self.session = requests.Session()
        self.session.auth = (self.sk, '')
        self.session.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self.logger = logging.getLogger('magpy.request')

    def _process_response(self, response):
        if response.status_code in [200, 201]:
            return json.loads(response.content)

        elif response.status_code == 401:
            self.logger.error('Authorization error. Check your token')
            print 'Authorization error. Check your token'

        elif response.status_code == 402:
            self.logger.error('Invalid card!')
            print 'Invalid card!'

        elif response.status_code == 404:
            self.logger.error('Authorization error. Token not found')
            print 'Authorization error. Token not found'

        else:
            self.logger.error('Invalid request')
            print 'Invalid request'
