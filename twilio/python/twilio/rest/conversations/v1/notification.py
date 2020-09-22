# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class NotificationList(ListResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version):
        """
        Initialize the NotificationList

        :param Version version: Version that contains the resource

        :returns: twilio.rest.conversations.v1.notification.NotificationList
        :rtype: twilio.rest.conversations.v1.notification.NotificationList
        """
        super(NotificationList, self).__init__(version)

        # Path Solution
        self._solution = {}

    def get(self, chat_service_sid):
        """
        Constructs a NotificationContext

        :param chat_service_sid: The SID of the Chat Service that the Configuration applies to.

        :returns: twilio.rest.conversations.v1.notification.NotificationContext
        :rtype: twilio.rest.conversations.v1.notification.NotificationContext
        """
        return NotificationContext(self._version, chat_service_sid=chat_service_sid, )

    def __call__(self, chat_service_sid):
        """
        Constructs a NotificationContext

        :param chat_service_sid: The SID of the Chat Service that the Configuration applies to.

        :returns: twilio.rest.conversations.v1.notification.NotificationContext
        :rtype: twilio.rest.conversations.v1.notification.NotificationContext
        """
        return NotificationContext(self._version, chat_service_sid=chat_service_sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Conversations.V1.NotificationList>'


class NotificationPage(Page):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, response, solution):
        """
        Initialize the NotificationPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API

        :returns: twilio.rest.conversations.v1.notification.NotificationPage
        :rtype: twilio.rest.conversations.v1.notification.NotificationPage
        """
        super(NotificationPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of NotificationInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.conversations.v1.notification.NotificationInstance
        :rtype: twilio.rest.conversations.v1.notification.NotificationInstance
        """
        return NotificationInstance(self._version, payload, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Conversations.V1.NotificationPage>'


class NotificationContext(InstanceContext):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, chat_service_sid):
        """
        Initialize the NotificationContext

        :param Version version: Version that contains the resource
        :param chat_service_sid: The SID of the Chat Service that the Configuration applies to.

        :returns: twilio.rest.conversations.v1.notification.NotificationContext
        :rtype: twilio.rest.conversations.v1.notification.NotificationContext
        """
        super(NotificationContext, self).__init__(version)

        # Path Solution
        self._solution = {'chat_service_sid': chat_service_sid, }
        self._uri = '/Services/{chat_service_sid}/Configuration/Notifications'.format(**self._solution)

    def update(self, log_enabled=values.unset, new_message_enabled=values.unset,
               new_message_template=values.unset, new_message_sound=values.unset,
               new_message_badge_count_enabled=values.unset,
               added_to_conversation_enabled=values.unset,
               added_to_conversation_template=values.unset,
               added_to_conversation_sound=values.unset,
               removed_from_conversation_enabled=values.unset,
               removed_from_conversation_template=values.unset,
               removed_from_conversation_sound=values.unset):
        """
        Update the NotificationInstance

        :param bool log_enabled: Weather the notification logging is enabled.
        :param bool new_message_enabled: Whether to send a notification when a new message is added to a conversation.
        :param unicode new_message_template: The template to use to create the notification text displayed when a new message is added to a conversation.
        :param unicode new_message_sound: The name of the sound to play when a new message is added to a conversation.
        :param bool new_message_badge_count_enabled: Whether the new message badge is enabled.
        :param bool added_to_conversation_enabled: Whether to send a notification when a participant is added to a conversation.
        :param unicode added_to_conversation_template: The template to use to create the notification text displayed when a participant is added to a conversation.
        :param unicode added_to_conversation_sound: The name of the sound to play when a participant is added to a conversation.
        :param bool removed_from_conversation_enabled: Whether to send a notification to a user when they are removed from a conversation.
        :param unicode removed_from_conversation_template: The template to use to create the notification text displayed to a user when they are removed.
        :param unicode removed_from_conversation_sound: The name of the sound to play to a user when they are removed from a conversation.

        :returns: The updated NotificationInstance
        :rtype: twilio.rest.conversations.v1.notification.NotificationInstance
        """
        data = values.of({
            'LogEnabled': log_enabled,
            'NewMessage.Enabled': new_message_enabled,
            'NewMessage.Template': new_message_template,
            'NewMessage.Sound': new_message_sound,
            'NewMessage.BadgeCountEnabled': new_message_badge_count_enabled,
            'AddedToConversation.Enabled': added_to_conversation_enabled,
            'AddedToConversation.Template': added_to_conversation_template,
            'AddedToConversation.Sound': added_to_conversation_sound,
            'RemovedFromConversation.Enabled': removed_from_conversation_enabled,
            'RemovedFromConversation.Template': removed_from_conversation_template,
            'RemovedFromConversation.Sound': removed_from_conversation_sound,
        })

        payload = self._version.update(method='POST', uri=self._uri, data=data, )

        return NotificationInstance(
            self._version,
            payload,
            chat_service_sid=self._solution['chat_service_sid'],
        )

    def fetch(self):
        """
        Fetch the NotificationInstance

        :returns: The fetched NotificationInstance
        :rtype: twilio.rest.conversations.v1.notification.NotificationInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return NotificationInstance(
            self._version,
            payload,
            chat_service_sid=self._solution['chat_service_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Conversations.V1.NotificationContext {}>'.format(context)


class NotificationInstance(InstanceResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, payload, chat_service_sid=None):
        """
        Initialize the NotificationInstance

        :returns: twilio.rest.conversations.v1.notification.NotificationInstance
        :rtype: twilio.rest.conversations.v1.notification.NotificationInstance
        """
        super(NotificationInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'chat_service_sid': payload.get('chat_service_sid'),
            'new_message': payload.get('new_message'),
            'added_to_conversation': payload.get('added_to_conversation'),
            'removed_from_conversation': payload.get('removed_from_conversation'),
            'log_enabled': payload.get('log_enabled'),
            'url': payload.get('url'),
        }

        # Context
        self._context = None
        self._solution = {'chat_service_sid': chat_service_sid or self._properties['chat_service_sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: NotificationContext for this NotificationInstance
        :rtype: twilio.rest.conversations.v1.notification.NotificationContext
        """
        if self._context is None:
            self._context = NotificationContext(
                self._version,
                chat_service_sid=self._solution['chat_service_sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The unique id of the Account responsible for this configuration.
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def chat_service_sid(self):
        """
        :returns: The SID of the Chat Service that the Configuration applies to.
        :rtype: unicode
        """
        return self._properties['chat_service_sid']

    @property
    def new_message(self):
        """
        :returns: The Push Notification configuration for New Messages.
        :rtype: dict
        """
        return self._properties['new_message']

    @property
    def added_to_conversation(self):
        """
        :returns: The Push Notification configuration for being added to a Conversation.
        :rtype: dict
        """
        return self._properties['added_to_conversation']

    @property
    def removed_from_conversation(self):
        """
        :returns: The Push Notification configuration for being removed from a Conversation.
        :rtype: dict
        """
        return self._properties['removed_from_conversation']

    @property
    def log_enabled(self):
        """
        :returns: Weather the notification logging is enabled.
        :rtype: bool
        """
        return self._properties['log_enabled']

    @property
    def url(self):
        """
        :returns: An absolute URL for this configuration.
        :rtype: unicode
        """
        return self._properties['url']

    def update(self, log_enabled=values.unset, new_message_enabled=values.unset,
               new_message_template=values.unset, new_message_sound=values.unset,
               new_message_badge_count_enabled=values.unset,
               added_to_conversation_enabled=values.unset,
               added_to_conversation_template=values.unset,
               added_to_conversation_sound=values.unset,
               removed_from_conversation_enabled=values.unset,
               removed_from_conversation_template=values.unset,
               removed_from_conversation_sound=values.unset):
        """
        Update the NotificationInstance

        :param bool log_enabled: Weather the notification logging is enabled.
        :param bool new_message_enabled: Whether to send a notification when a new message is added to a conversation.
        :param unicode new_message_template: The template to use to create the notification text displayed when a new message is added to a conversation.
        :param unicode new_message_sound: The name of the sound to play when a new message is added to a conversation.
        :param bool new_message_badge_count_enabled: Whether the new message badge is enabled.
        :param bool added_to_conversation_enabled: Whether to send a notification when a participant is added to a conversation.
        :param unicode added_to_conversation_template: The template to use to create the notification text displayed when a participant is added to a conversation.
        :param unicode added_to_conversation_sound: The name of the sound to play when a participant is added to a conversation.
        :param bool removed_from_conversation_enabled: Whether to send a notification to a user when they are removed from a conversation.
        :param unicode removed_from_conversation_template: The template to use to create the notification text displayed to a user when they are removed.
        :param unicode removed_from_conversation_sound: The name of the sound to play to a user when they are removed from a conversation.

        :returns: The updated NotificationInstance
        :rtype: twilio.rest.conversations.v1.notification.NotificationInstance
        """
        return self._proxy.update(
            log_enabled=log_enabled,
            new_message_enabled=new_message_enabled,
            new_message_template=new_message_template,
            new_message_sound=new_message_sound,
            new_message_badge_count_enabled=new_message_badge_count_enabled,
            added_to_conversation_enabled=added_to_conversation_enabled,
            added_to_conversation_template=added_to_conversation_template,
            added_to_conversation_sound=added_to_conversation_sound,
            removed_from_conversation_enabled=removed_from_conversation_enabled,
            removed_from_conversation_template=removed_from_conversation_template,
            removed_from_conversation_sound=removed_from_conversation_sound,
        )

    def fetch(self):
        """
        Fetch the NotificationInstance

        :returns: The fetched NotificationInstance
        :rtype: twilio.rest.conversations.v1.notification.NotificationInstance
        """
        return self._proxy.fetch()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Conversations.V1.NotificationInstance {}>'.format(context)