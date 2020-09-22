import os

from tornado import web

try:
    import sprockets_influxdb as influxdb
except ImportError:
    influxdb = None

from sprockets_dynamodb import exceptions

INFLUXDB_DATABASE = 'dynamodb'
INFLUXDB_MEASUREMENT = os.getenv('SERVICE', 'DynamoDB')


def _no_creds_should_return_429():
    """Returns ``True`` if the ``DYANMODB_NO_CREDS_RATE_LIMIT`` environment
    variable is set to the string ``true``.

    :rtype: bool

    """
    return os.environ.get('DYANMODB_NO_CREDS_RATE_LIMIT', '').lower() == 'true'


class DynamoDBMixin(object):
    """The DynamoDBMixin is an opinionated :class:`~tornado.web.RequestHandler`
    mixin class that

    """
    def initialize(self):
        super(DynamoDBMixin, self).initialize()
        self.application.dynamodb.set_error_callback(
            self._on_dynamodb_exception)
        if influxdb:
            self.application.dynamodb.set_instrumentation_callback(
                self._record_dynamodb_execution)

    def _on_dynamodb_exception(self, error):
        """Dynamically handle DynamoDB exceptions, returning HTTP error
        responses.

        :param exceptions.DynamoDBException error:

        """
        if isinstance(error, exceptions.ConditionalCheckFailedException):
            raise web.HTTPError(409, reason='Condition Check Failure')
        elif isinstance(error, exceptions.NoCredentialsError):
            if _no_creds_should_return_429():
                raise web.HTTPError(429, reason='Instance Credentials Failure')
        elif isinstance(error, (exceptions.ThroughputExceeded,
                                exceptions.ThrottlingException)):
            raise web.HTTPError(429, reason='Too Many Requests')
        if hasattr(self, 'logger'):
            self.logger.error('DynamoDB Error: %s', error)
        raise web.HTTPError(500, reason=str(error))

    @staticmethod
    def _record_dynamodb_execution(measurements):
        for row in measurements:
            measurement = influxdb.Measurement(INFLUXDB_DATABASE,
                                               INFLUXDB_MEASUREMENT)
            measurement.set_timestamp(row.timestamp)
            measurement.set_tag('action', row.action)
            measurement.set_tag('table', row.table)
            measurement.set_tag('attempt', row.attempt)
            if row.error:
                measurement.set_tag('error', row.error)
            measurement.set_field('duration', row.duration)
            influxdb.add_measurement(measurement)
