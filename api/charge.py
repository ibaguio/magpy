import logging
from magpy.request import MagpieRequest

logger = logging.getLogger('magpy.api.charge')


class Charge(MagpieRequest):
    def __init__(self, is_sandbox=False, **kwargs):
        super(Charge, self).__init__(is_sandbox, **kwargs)
        self.logger = logger

    def create(
            self, amount, source, description,
            statement_description, capture=True, currency='PHP'):

        response = self.session.post(self.url + '/charges', json={
            'amount': amount,
            'source': source,
            'description': description,
            'statement_description': statement_description,
            'capture': capture,
            'currency': currency.lower()
        })

        return self._process_response(response)

    def get(self, charge_id):
        """Retrieves the details of a charge that has previously been
        created. Supply the unique charge ID that was returned from your
        previous request, and Magpie will return the corresponding
        charge information."""

        response = self.session.get(
            self.url + '/charges/%s' % charge_id)

        return self._process_response(response)

    def capture(self, charge_id, amount):
        """Capture an uncaptured charge object."""

        response = self.session.post(
            self.url + '/charges/%s/capture' % charge_id,
            json={'amount': amount})

        return self._process_response(response)

    def void(self, charge_id):
        """Cancel an authorized transaction. Can also be used to cancel
        a captured/purchased transaction that has not yet settled at the
        merchant account."""

        response = self.session.post(
            self.url + '/charges/%s/void' % charge_id)

        return self._process_response(response)

    def refund(self, charge_id, amount):
        """Refund a specific charge."""

        response = self.session.post(
            self.url + '/charges/%s/refund' % charge_id,
            json={'amount': amount})

        return self._process_response(response)
