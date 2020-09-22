# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base.domain import Domain
from twilio.rest.pricing.v1 import V1
from twilio.rest.pricing.v2 import V2


class Pricing(Domain):

    def __init__(self, twilio):
        """
        Initialize the Pricing Domain

        :returns: Domain for Pricing
        :rtype: twilio.rest.pricing.Pricing
        """
        super(Pricing, self).__init__(twilio)

        self.base_url = 'https://pricing.twilio.com'

        # Versions
        self._v1 = None
        self._v2 = None

    @property
    def v1(self):
        """
        :returns: Version v1 of pricing
        :rtype: twilio.rest.pricing.v1.V1
        """
        if self._v1 is None:
            self._v1 = V1(self)
        return self._v1

    @property
    def v2(self):
        """
        :returns: Version v2 of pricing
        :rtype: twilio.rest.pricing.v2.V2
        """
        if self._v2 is None:
            self._v2 = V2(self)
        return self._v2

    @property
    def messaging(self):
        """
        :rtype: twilio.rest.pricing.v1.messaging.MessagingList
        """
        return self.v1.messaging

    @property
    def phone_numbers(self):
        """
        :rtype: twilio.rest.pricing.v1.phone_number.PhoneNumberList
        """
        return self.v1.phone_numbers

    @property
    def voice(self):
        """
        :rtype: twilio.rest.pricing.v2.voice.VoiceList
        """
        return self.v2.voice

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Pricing>'
