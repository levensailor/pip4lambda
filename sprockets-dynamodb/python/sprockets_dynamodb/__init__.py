"""
Sprockets DynamoDB
==================

"""
import logging
try:
    from sprockets_dynamodb.client import Client
except ImportError:   # pragma: nocover
    Client = None
try:
    from sprockets_dynamodb.mixin import DynamoDBMixin
except ImportError:  # pragma: nocover
    DynamoDBMixin = None

try:
    from sprockets_dynamodb.exceptions import *
except ImportError:  # pragma: nocover
    pass

version_info = (3, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Table status constants
TABLE_ACTIVE = 'ACTIVE'
TABLE_CREATING = 'CREATING'
TABLE_DELETING = 'DELETING'
TABLE_DISABLED = 'DISABLED'
TABLE_UPDATING = 'UPDATING'

__all__ = [
    'client',
    'exceptions',
    'mixin',
    'utils',
    'Client',
    'DynamoDBMixin',
    'DynamoDBException',
    'ConditionalCheckFailedException',
    'ConfigNotFound',
    'ConfigParserError',
    'InternalFailure',
    'ItemCollectionSizeLimitExceeded',
    'InvalidAction',
    'InvalidParameterCombination',
    'InvalidParameterValue',
    'InvalidQueryParameter',
    'LimitExceeded',
    'MalformedQueryString',
    'MissingParameter',
    'NoCredentialsError',
    'NoProfileError',
    'OptInRequired',
    'RequestException',
    'RequestExpired',
    'ResourceInUse',
    'ResourceNotFound',
    'ServiceUnavailable',
    'ThroughputExceeded',
    'ThrottlingException',
    'TimeoutException',
    'ValidationException',
    '__version__',
    'version_info',
    'TABLE_ACTIVE',
    'TABLE_CREATING',
    'TABLE_DELETING',
    'TABLE_DISABLED',
    'TABLE_UPDATING',
]
