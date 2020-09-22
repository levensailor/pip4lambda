"""
DynamoDB Client
===============

"""
import collections
import json
import logging
import os
import select as _select
import socket
import ssl
import time

from tornado import concurrent, gen, httpclient, ioloop
import tornado_aws
from tornado_aws import exceptions as aws_exceptions

from sprockets_dynamodb import exceptions, utils

LOGGER = logging.getLogger(__name__)

Measurement = collections.namedtuple(
    'Measurement',
    ['timestamp', 'action', 'table', 'attempt', 'duration', 'error'])


class Client(object):
    """
    Asynchronous DynamoDB Client

    :keyword str region: AWS region to send requests to
    :keyword str access_key: AWS access key.  If unspecified, this
        defaults to the :envvar:`AWS_ACCESS_KEY_ID` environment
        variable and will fall back to using the AWS CLI credentials
        file.  See :class:`tornado_aws.client.AsyncAWSClient` for
        more details.
    :keyword str secret_key: AWS secret used to secure API calls.
        If unspecified, this defaults to the :envvar:`AWS_SECRET_ACCESS_KEY`
        environment variable and will fall back to using the AWS CLI
        credentials as described in :class:`tornado_aws.client.AsyncAWSClient`.
    :keyword str profile: optional profile to use in AWS API calls.
        If unspecified, this defaults to the :envvar:`AWS_DEFAULT_PROFILE`
        environment variable or ``default`` if unset.
    :keyword str endpoint: DynamoDB endpoint to contact.  If unspecified,
        the default is determined by the region.
    :keyword int max_clients: optional maximum number of HTTP requests
        that may be performed in parallel.
    :keyword int max_retries: Maximum number of times to retry a request when
        if fails under certain conditions. Can also be set with the
        :envvar:`DYNAMODB_MAX_RETRIES` environment variable.
    :keyword method instrumentation_callback: A method that is invoked with a
        list of measurements that were collected during the execution of an
        individual action.
    :keyword method on_error_callback: A method that is invoked when there is
        a request exception that can not automatically be retried or the
        maximum number of retries has been exceeded for a request.

    Any of the methods invoked in the client can raise the following
    exceptions:

      - :exc:`sprockets_dynamodb.exceptions.DynamoDBException`
      - :exc:`sprockets_dynamodb.exceptions.ConfigNotFound`
      - :exc:`sprockets_dynamodb.exceptions.NoCredentialsError`
      - :exc:`sprockets_dynamodb.exceptions.NoProfileError`
      - :exc:`sprockets_dynamodb.exceptions.TimeoutException`
      - :exc:`sprockets_dynamodb.exceptions.RequestException`
      - :exc:`sprockets_dynamodb.exceptions.InternalFailure`
      - :exc:`sprockets_dynamodb.exceptions.LimitExceeded`
      - :exc:`sprockets_dynamodb.exceptions.MissingParameter`
      - :exc:`sprockets_dynamodb.exceptions.OptInRequired`
      - :exc:`sprockets_dynamodb.exceptions.ResourceInUse`
      - :exc:`sprockets_dynamodb.exceptions.RequestExpired`
      - :exc:`sprockets_dynamodb.exceptions.ServiceUnavailable`
      - :exc:`sprockets_dynamodb.exceptions.ValidationException`

    Create an instance of this class to interact with a DynamoDB
    server.  A :class:`tornado_aws.client.AsyncAWSClient` instance
    implements the AWS API wrapping and this class provides the
    DynamoDB specifics.

    """
    DEFAULT_MAX_RETRIES = 3

    def __init__(self, **kwargs):
        self.logger = LOGGER.getChild(self.__class__.__name__)
        if os.environ.get('DYNAMODB_ENDPOINT', None):
            kwargs.setdefault('endpoint', os.environ['DYNAMODB_ENDPOINT'])
        self._client = tornado_aws.AsyncAWSClient('dynamodb', **kwargs)
        self._ioloop = kwargs.get('io_loop', ioloop.IOLoop.current())
        self._max_retries = kwargs.get(
            'max_retries', os.environ.get(
                'DYNAMODB_MAX_RETRIES', self.DEFAULT_MAX_RETRIES))
        self._instrumentation_callback = kwargs.get('instrumentation_callback')
        self._on_error = kwargs.get('on_error_callback')

    def create_table(self, table_definition):
        """
        Invoke the ``CreateTable`` function.

        :param dict table_definition: description of the table to
            create according to `CreateTable`_
        :rtype: tornado.concurrent.Future

        .. _CreateTable: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_CreateTable.html

        """
        return self.execute('CreateTable', table_definition)

    def update_table(self, table_definition):
        """
        Modifies the provisioned throughput settings, global secondary
        indexes, or DynamoDB Streams settings for a given table.

        You can only perform one of the following operations at once:

        - Modify the provisioned throughput settings of the table.
        - Enable or disable Streams on the table.
        - Remove a global secondary index from the table.
        - Create a new global secondary index on the table. Once the index
          begins back-filling, you can use *UpdateTable* to perform other
          operations.

        *UpdateTable* is an asynchronous operation; while it is executing, the
        table status changes from ``ACTIVE`` to ``UPDATING``. While it is
        ``UPDATING``, you cannot issue another *UpdateTable* request. When the
        table returns to the ``ACTIVE`` state, the *UpdateTable* operation is
        complete.

        :param dict table_definition: description of the table to
            update according to `UpdateTable`_
        :rtype: tornado.concurrent.Future

        .. _UpdateTable: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_UpdateTable.html

        """
        raise NotImplementedError

    def delete_table(self, table_name):
        """
        Invoke the `DeleteTable`_ function. The DeleteTable operation deletes a
        table and all of its items. After a DeleteTable request, the specified
        table is in the DELETING state until DynamoDB completes the deletion.
        If the table is in the ACTIVE state, you can delete it. If a table is
        in CREATING or UPDATING states, then a
        :py:exc:`~sprockets_dynamodb.exceptions.ResourceInUse`
        exception is raised. If the  specified table does not exist, a
        :exc:`~sprockets_dynamodb.exceptions.ResourceNotFound`
        exception is raised. If table is already in the DELETING state, no
        error is returned.

        :param str table_name: name of the table to describe.
        :rtype: tornado.concurrent.Future

        .. _DeleteTable: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_DeleteTable.html

        """
        return self.execute('DeleteTable', {'TableName': table_name})

    def describe_table(self, table_name):
        """
        Invoke the `DescribeTable`_ function.

        :param str table_name: name of the table to describe.
        :rtype: tornado.concurrent.Future

        .. _DescribeTable: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_DescribeTable.html

        """
        return self.execute('DescribeTable', {'TableName': table_name})

    def list_tables(self, exclusive_start_table_name=None, limit=None):
        """
        Invoke the `ListTables`_ function.

        Returns an array of table names associated with the current account
        and endpoint. The output from *ListTables* is paginated, with each page
        returning a maximum of ``100`` table names.

        :param str exclusive_start_table_name: The first table name that this
            operation will evaluate. Use the value that was returned for
            ``LastEvaluatedTableName`` in a previous operation, so that you can
            obtain the next page of results.
        :param int limit: A maximum number of table names to return. If this
            parameter is not specified, the limit is ``100``.

        .. _ListTables: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_ListTables.html

        """
        payload = {}
        if exclusive_start_table_name:
            payload['ExclusiveStartTableName'] = exclusive_start_table_name
        if limit:
            payload['Limit'] = limit
        return self.execute('ListTables', payload)

    def put_item(self, table_name, item,
                 condition_expression=None,
                 expression_attribute_names=None,
                 expression_attribute_values=None,
                 return_consumed_capacity=None,
                 return_item_collection_metrics=None,
                 return_values=None):
        """Invoke the `PutItem`_ function, creating a new item, or replaces an
        old item with a new item. If an item that has the same primary key as
        the new item already exists in the specified table, the new item
        completely replaces the existing item. You can perform a conditional
        put operation (add a new item if one with the specified primary key
        doesn't exist), or replace an existing item if it has certain attribute
        values.

        For more information about using this API, see Working with Items in
        the Amazon DynamoDB Developer Guide.

        :param str table_name: The table to put the item to
        :param dict item: A map of attribute name/value pairs, one for each
            attribute. Only the primary key attributes are required; you can
            optionally provide other attribute name-value pairs for the item.

            You must provide all of the attributes for the primary key. For
            example, with a simple primary key, you only need to provide a
            value for the partition key. For a composite primary key, you must
            provide both values for both the partition key and the sort key.

            If you specify any attributes that are part of an index key, then
            the data types for those attributes must match those of the schema
            in the table's attribute definition.
        :param str condition_expression: A condition that must be satisfied in
            order for a conditional *PutItem* operation to succeed. See the
            `AWS documentation for ConditionExpression <http://docs.aws.amazon.
            com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-Put
            Item-request-ConditionExpression>`_ for more information.
        :param dict expression_attribute_names: One or more substitution tokens
            for attribute names in an expression. See the `AWS documentation
            for ExpressionAttributeNames <http://docs.aws.amazon.com/amazon
            dynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-
            ExpressionAttributeNames>`_ for more information.
        :param dict expression_attribute_values: One or more values that can be
            substituted in an expression. See the `AWS documentation
            for ExpressionAttributeValues <http://docs.aws.amazon.com/amazon
            dynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-
            ExpressionAttributeValues>`_ for more information.
        :param str return_consumed_capacity: Determines the level of detail
            about provisioned throughput consumption that is returned in the
            response. Should be ``None`` or one of ``INDEXES`` or ``TOTAL``
        :param str return_item_collection_metrics: Determines whether item
            collection metrics are returned.
        :param str return_values: Use ``ReturnValues`` if you want to get the
            item attributes as they appeared before they were updated with the
            ``PutItem`` request.
        :rtype: tornado.concurrent.Future

        .. _PutItem: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_PutItem.html

        """
        payload = {'TableName': table_name, 'Item': utils.marshall(item)}
        if condition_expression:
            payload['ConditionExpression'] = condition_expression
        if expression_attribute_names:
            payload['ExpressionAttributeNames'] = expression_attribute_names
        if expression_attribute_values:
            payload['ExpressionAttributeValues'] = expression_attribute_values
        if return_consumed_capacity:
            payload['ReturnConsumedCapacity'] = return_consumed_capacity
        if return_item_collection_metrics:
            payload['ReturnItemCollectionMetrics'] = 'SIZE'
        if return_values:
            _validate_return_values(return_values)
            payload['ReturnValues'] = return_values
        return self.execute('PutItem', payload)

    def get_item(self, table_name, key_dict,
                 consistent_read=False,
                 expression_attribute_names=None,
                 projection_expression=None,
                 return_consumed_capacity=None):
        """
        Invoke the `GetItem`_ function.

        :param str table_name: table to retrieve the item from
        :param dict key_dict: key to use for retrieval.  This will
            be marshalled for you so a native :class:`dict` works.
        :param bool consistent_read: Determines the read consistency model: If
            set to :py:data`True`, then the operation uses strongly consistent
            reads; otherwise, the operation uses eventually consistent reads.
        :param dict expression_attribute_names: One or more substitution tokens
            for attribute names in an expression.
        :param str projection_expression: A string that identifies one or more
            attributes to retrieve from the table. These attributes can include
            scalars, sets, or elements of a JSON document. The attributes in
            the expression must be separated by commas. If no attribute names
            are specified, then all attributes will be returned. If any of the
            requested attributes are not found, they will not appear in the
            result.
        :param str return_consumed_capacity: Determines the level of detail
            about provisioned throughput consumption that is returned in the
            response:

              - INDEXES: The response includes the aggregate consumed
                capacity for the operation, together with consumed capacity for
                each table and secondary index that was accessed. Note that
                some operations, such as *GetItem* and *BatchGetItem*, do not
                access any indexes at all. In these cases, specifying INDEXES
                will only return consumed capacity information for table(s).
              - TOTAL: The response includes only the aggregate consumed
                capacity for the operation.
              - NONE: No consumed capacity details are included in the
                response.
        :rtype: tornado.concurrent.Future

        .. _GetItem: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_GetItem.html

        """
        payload = {'TableName': table_name,
                   'Key': utils.marshall(key_dict),
                   'ConsistentRead': consistent_read}
        if expression_attribute_names:
            payload['ExpressionAttributeNames'] = expression_attribute_names
        if projection_expression:
            payload['ProjectionExpression'] = projection_expression
        if return_consumed_capacity:
            _validate_return_consumed_capacity(return_consumed_capacity)
            payload['ReturnConsumedCapacity'] = return_consumed_capacity
        return self.execute('GetItem', payload)

    def update_item(self, table_name, key_dict,
                    condition_expression=None,
                    update_expression=None,
                    expression_attribute_names=None,
                    expression_attribute_values=None,
                    return_consumed_capacity=None,
                    return_item_collection_metrics=None,
                    return_values=None):
        """Invoke the `UpdateItem`_ function.

        Edits an existing item's attributes, or adds a new item to the table
        if it does not already exist. You can put, delete, or add attribute
        values. You can also perform a conditional update on an existing item
        (insert a new attribute name-value pair if it doesn't exist, or replace
        an existing name-value pair if it has certain expected attribute
        values).

        :param str table_name: The name of the table that contains the item to
            update
        :param dict key_dict: A dictionary of key/value pairs that are used to
            define the primary key values for the item. For the primary key,
            you must provide all of the attributes. For example, with a simple
            primary key, you only need to provide a value for the partition
            key. For a composite primary key, you must provide values for both
            the partition key and the sort key.
        :param str condition_expression: A condition that must be satisfied in
            order for a conditional *UpdateItem* operation to succeed. One of:
            ``attribute_exists``, ``attribute_not_exists``, ``attribute_type``,
            ``contains``, ``begins_with``, ``size``, ``=``, ``<>``, ``<``,
            ``>``, ``<=``, ``>=``, ``BETWEEN``, ``IN``, ``AND``, ``OR``, or
            ``NOT``.
        :param str update_expression: An expression that defines one or more
            attributes to be updated, the action to be performed on them, and
            new value(s) for them.
        :param dict expression_attribute_names: One or more substitution tokens
            for attribute names in an expression.
        :param dict expression_attribute_values: One or more values that can be
            substituted in an expression.
        :param str return_consumed_capacity: Determines the level of detail
            about provisioned throughput consumption that is returned in the
            response. See the `AWS documentation
            for ReturnConsumedCapacity <http://docs.aws.amazon.com/
            amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-Update
            Item-request-ReturnConsumedCapacity>`_ for more information.
        :param str return_item_collection_metrics: Determines whether item
            collection metrics are returned.
        :param str return_values: Use ReturnValues if you want to get the item
            attributes as they appeared either before or after they were
            updated. See the `AWS documentation for ReturnValues <http://docs.
            aws.amazon.com/amazondynamodb/latest/APIReference/
            API_UpdateItem.html#DDB-UpdateItem-request-ReturnValues>`_
        :rtype: tornado.concurrent.Future

        .. _UpdateItem: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_UpdateItem.html

        """
        payload = {'TableName': table_name,
                   'Key': utils.marshall(key_dict),
                   'UpdateExpression': update_expression}
        if condition_expression:
            payload['ConditionExpression'] = condition_expression
        if expression_attribute_names:
            payload['ExpressionAttributeNames'] = expression_attribute_names
        if expression_attribute_values:
            payload['ExpressionAttributeValues'] = \
                utils.marshall(expression_attribute_values)
        if return_consumed_capacity:
            _validate_return_consumed_capacity(return_consumed_capacity)
            payload['ReturnConsumedCapacity'] = return_consumed_capacity
        if return_item_collection_metrics:
            _validate_return_item_collection_metrics(
                return_item_collection_metrics)
            payload['ReturnItemCollectionMetrics'] = \
                return_item_collection_metrics
        if return_values:
            _validate_return_values(return_values)
            payload['ReturnValues'] = return_values
        return self.execute('UpdateItem', payload)

    def delete_item(self, table_name, key_dict,
                    condition_expression=None,
                    expression_attribute_names=None,
                    expression_attribute_values=None,
                    return_consumed_capacity=None,
                    return_item_collection_metrics=None,
                    return_values=False):
        """Invoke the `DeleteItem`_ function that deletes a single item in a
        table by primary key. You can perform a conditional delete operation
        that deletes the item if it exists, or if it has an expected attribute
        value.

        :param str table_name: The name of the table from which to delete the
            item.
        :param dict key_dict: A map of attribute names to ``AttributeValue``
            objects, representing the primary key of the item to delete. For
            the primary key, you must provide all of the attributes. For
            example, with a simple primary key, you only need to provide a
            value for the partition key. For a composite primary key, you must
            provide values for both the partition key and the sort key.
        :param str condition_expression: A condition that must be satisfied in
            order for a conditional *DeleteItem* to succeed. See the `AWS
            documentation for ConditionExpression <http://docs.aws.amazon.com/
            amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-Delete
            Item-request-ConditionExpression>`_ for more information.
        :param dict expression_attribute_names: One or more substitution tokens
            for attribute names in an expression. See the `AWS documentation
            for ExpressionAttributeNames <http://docs.aws.amazon.com/
            amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-Delete
            Item-request-ExpressionAttributeNames>`_ for more information.
        :param dict expression_attribute_values: One or more values that can be
            substituted in an expression. See the `AWS documentation
            for ExpressionAttributeValues <http://docs.aws.amazon.com/
            amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-Delete
            Item-request-ExpressionAttributeValues>`_ for more information.
        :param str return_consumed_capacity: Determines the level of detail
            about provisioned throughput consumption that is returned in the
            response. See the `AWS documentation
            for ReturnConsumedCapacity <http://docs.aws.amazon.com/
            amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-Delete
            Item-request-ReturnConsumedCapacity>`_ for more information.
        :param str return_item_collection_metrics: Determines whether item
            collection metrics are returned.
        :param str return_values: Return the item attributes as they appeared
            before they were deleted.

        .. _DeleteItem: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_DeleteItem.html

        """
        payload = {'TableName': table_name, 'Key': utils.marshall(key_dict)}
        if condition_expression:
            payload['ConditionExpression'] = condition_expression
        if expression_attribute_names:
            payload['ExpressionAttributeNames'] = expression_attribute_names
        if expression_attribute_values:
            payload['ExpressionAttributeValues'] = \
                utils.marshall(expression_attribute_values)
        if return_consumed_capacity:
            _validate_return_consumed_capacity(return_consumed_capacity)
            payload['ReturnConsumedCapacity'] = return_consumed_capacity
        if return_item_collection_metrics:
            _validate_return_item_collection_metrics(
                return_item_collection_metrics)
            payload['ReturnItemCollectionMetrics'] = \
                return_item_collection_metrics
        if return_values:
            _validate_return_values(return_values)
            payload['ReturnValues'] = return_values
        return self.execute('DeleteItem', payload)

    def batch_get_item(self):
        """Invoke the `BatchGetItem`_ function.

        .. _BatchGetItem: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_BatchGetItem.html

        """
        raise NotImplementedError

    def batch_write_item(self):
        """Invoke the `BatchWriteItem`_ function.

        .. _BatchWriteItem: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_BatchWriteItem.html

        """
        raise NotImplementedError

    def query(self, table_name,
              index_name=None,
              consistent_read=None,
              key_condition_expression=None,
              filter_expression=None,
              expression_attribute_names=None,
              expression_attribute_values=None,
              projection_expression=None,
              select=None,
              exclusive_start_key=None,
              limit=None,
              scan_index_forward=True,
              return_consumed_capacity=None):
        """A `Query`_ operation uses the primary key of a table or a secondary
        index to directly access items from that table or index.

        :param str table_name: The name of the table containing the requested
            items.
        :param bool consistent_read: Determines the read consistency model: If
            set to ``True``, then the operation uses strongly consistent reads;
            otherwise, the operation uses eventually consistent reads. Strongly
            consistent reads are not supported on global secondary indexes. If
            you query a global secondary index with ``consistent_read`` set to
            ``True``, you will receive a
            :exc:`~sprockets_dynamodb.exceptions.ValidationException`.
        :param dict exclusive_start_key: The primary key of the first
            item that this operation will evaluate. Use the value that was
            returned for ``LastEvaluatedKey`` in the previous operation. In a
            parallel scan, a *Scan* request that includes
            ``exclusive_start_key`` must specify the same segment whose
            previous *Scan* returned the corresponding value of
            ``LastEvaluatedKey``.
        :param dict expression_attribute_names: One or more substitution tokens
            for attribute names in an expression.
        :param dict expression_attribute_values: One or more values that can be
            substituted in an expression.
        :param str key_condition_expression: The condition that specifies the
            key value(s) for items to be retrieved by the *Query* action. The
            condition must perform an equality test on a single partition key
            value, but can optionally perform one of several comparison tests
            on a single sort key value. The partition key equality test is
            required. For examples see `KeyConditionExpression
            <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/
            Query.html#Query.KeyConditionExpressions>.
        :param str filter_expression: A string that contains conditions that
            DynamoDB applies after the *Query* operation, but before the data
            is returned to you. Items that do not satisfy the criteria are not
            returned. Note that a filter expression is applied after the items
            have already been read; the process of filtering does not consume
            any additional read capacity units. For more information, see
            `Filter Expressions <http://docs.aws.amazon.com/amazondynamodb/
            latest/developerguide/QueryAndScan.html#FilteringResults>`_ in the
            Amazon DynamoDB Developer Guide.
        :param str projection_expression:
        :param str index_name: The name of a secondary index to query. This
            index can be any local secondary index or global secondary index.
            Note that if you use this parameter, you must also provide
            ``table_name``.
        :param int limit: The maximum number of items to evaluate (not
            necessarily the number of matching items). If DynamoDB processes
            the number of items up to the limit while processing the results,
            it stops the operation and returns the matching values up to that
            point, and a key in ``LastEvaluatedKey`` to apply in a subsequent
            operation, so that you can pick up where you left off. Also, if the
            processed data set size exceeds 1 MB before DynamoDB reaches this
            limit, it stops the operation and returns the matching values up to
            the limit, and a key in ``LastEvaluatedKey`` to apply in a
            subsequent operation to continue the operation. For more
            information, see `Query and Scan <http://docs.aws.amazon.com/amazo
            ndynamodb/latest/developerguide/QueryAndScan.html>`_ in the Amazon
            DynamoDB Developer Guide.
        :param str return_consumed_capacity: Determines the level of detail
            about provisioned throughput consumption that is returned in the
            response:

              - ``INDEXES``: The response includes the aggregate consumed
                capacity for the operation, together with consumed capacity for
                each table and secondary index that was accessed. Note that
                some operations, such as *GetItem* and *BatchGetItem*, do not
                access any indexes at all. In these cases, specifying
                ``INDEXES`` will only return consumed capacity information for
                table(s).
              - ``TOTAL``: The response includes only the aggregate consumed
                capacity for the operation.
              - ``NONE``: No consumed capacity details are included in the
                response.
        :param bool scan_index_forward: Specifies the order for index
            traversal: If ``True`` (default), the traversal is performed in
            ascending order; if ``False``, the traversal is performed in
            descending order. Items with the same partition key value are
            stored in sorted order by sort key. If the sort key data type is
            *Number*, the results are stored in numeric order. For type
            *String*, the results are stored in order of ASCII character code
            values. For type *Binary*, DynamoDB treats each byte of the binary
            data as unsigned. If set to ``True``, DynamoDB returns the results
            in the order in which they are stored (by sort key value). This is
            the default behavior. If set to ``False``, DynamoDB reads the
            results in reverse order by sort key value, and then returns the
            results to the client.
        :param str select: The attributes to be returned in the result. You can
            retrieve all item attributes, specific item attributes, the count
            of matching items, or in the case of an index, some or all of the
            attributes projected into the index. Possible values are:

              - ``ALL_ATTRIBUTES``: Returns all of the item attributes from the
                specified table or index. If you query a local secondary index,
                then for each matching item in the index DynamoDB will fetch
                the entire item from the parent table. If the index is
                configured to project all item attributes, then all of the data
                can be obtained from the local secondary index, and no fetching
                is required.
              - ``ALL_PROJECTED_ATTRIBUTES``: Allowed only when querying an
                index. Retrieves all attributes that have been projected into
                the index. If the index is configured to project all
                attributes, this return value is equivalent to specifying
                ``ALL_ATTRIBUTES``.
              - ``COUNT``: Returns the number of matching items, rather than
                the matching items themselves.
        :rtype: dict

        .. _Query: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_Query.html

        """
        payload = {'TableName': table_name,
                   'ScanIndexForward': scan_index_forward}
        if index_name:
            payload['IndexName'] = index_name
        if consistent_read is not None:
            payload['ConsistentRead'] = consistent_read
        if key_condition_expression:
            payload['KeyConditionExpression'] = key_condition_expression
        if filter_expression:
            payload['FilterExpression'] = filter_expression
        if expression_attribute_names:
            payload['ExpressionAttributeNames'] = expression_attribute_names
        if expression_attribute_values:
            payload['ExpressionAttributeValues'] = \
                utils.marshall(expression_attribute_values)
        if projection_expression:
            payload['ProjectionExpression'] = projection_expression
        if select:
            _validate_select(select)
            payload['Select'] = select
        if exclusive_start_key:
            payload['ExclusiveStartKey'] = utils.marshall(exclusive_start_key)
        if limit:
            payload['Limit'] = limit
        if return_consumed_capacity:
            _validate_return_consumed_capacity(return_consumed_capacity)
            payload['ReturnConsumedCapacity'] = return_consumed_capacity
        return self.execute('Query', payload)

    def scan(self,
             table_name,
             index_name=None,
             consistent_read=None,
             projection_expression=None,
             filter_expression=None,
             expression_attribute_names=None,
             expression_attribute_values=None,
             segment=None,
             total_segments=None,
             select=None,
             limit=None,
             exclusive_start_key=None,
             return_consumed_capacity=None):
        """The `Scan`_ operation returns one or more items and item attributes
        by accessing every item in a table or a secondary index.

        If the total number of scanned items exceeds the maximum data set size
        limit of 1 MB, the scan stops and results are returned to the user as a
        ``LastEvaluatedKey`` value to continue the scan in a subsequent
        operation. The results also include the number of items exceeding the
        limit. A scan can result in no table data meeting the filter criteria.

        By default, Scan operations proceed sequentially; however, for faster
        performance on a large table or secondary index, applications can
        request a parallel *Scan* operation by providing the ``segment`` and
        ``total_segments`` parameters. For more information, see
        `Parallel Scan <http://docs.aws.amazon.com/amazondynamodb/latest/
        developerguide/QueryAndScan.html#QueryAndScanParallelScan>`_ in the
        Amazon DynamoDB Developer Guide.

        By default, *Scan* uses eventually consistent reads when accessing the
        data in a table; therefore, the result set might not include the
        changes to data in the table immediately before the operation began. If
        you need a consistent copy of the data, as of the time that the *Scan*
        begins, you can set the ``consistent_read`` parameter to ``True``.

        :rtype: dict

        .. _Scan: http://docs.aws.amazon.com/amazondynamodb/
           latest/APIReference/API_Scan.html

        """
        payload = {'TableName': table_name}
        if index_name:
            payload['IndexName'] = index_name
        if consistent_read is not None:
            payload['ConsistentRead'] = consistent_read
        if filter_expression:
            payload['FilterExpression'] = filter_expression
        if expression_attribute_names:
            payload['ExpressionAttributeNames'] = expression_attribute_names
        if expression_attribute_values:
            payload['ExpressionAttributeValues'] = \
                utils.marshall(expression_attribute_values)
        if projection_expression:
            payload['ProjectionExpression'] = projection_expression
        if segment:
            payload['Segment'] = segment
        if total_segments:
            payload['TotalSegments'] = total_segments
        if select:
            _validate_select(select)
            payload['Select'] = select
        if exclusive_start_key:
            payload['ExclusiveStartKey'] = utils.marshall(exclusive_start_key)
        if limit:
            payload['Limit'] = limit
        if return_consumed_capacity:
            _validate_return_consumed_capacity(return_consumed_capacity)
            payload['ReturnConsumedCapacity'] = return_consumed_capacity
        return self.execute('Scan', payload)

    @gen.coroutine
    def execute(self, action, parameters):
        """
        Execute a DynamoDB action with the given parameters. The method will
        retry requests that failed due to OS level errors or when being
        throttled by DynamoDB.

        :param str action: DynamoDB action to invoke
        :param dict parameters: parameters to send into the action
        :rtype: tornado.concurrent.Future

        This method creates a future that will resolve to the result
        of calling the specified DynamoDB function.  It does it's best
        to unwrap the response from the function to make life a little
        easier for you.  It does this for the ``GetItem`` and ``Query``
        functions currently.

        :raises:
            :exc:`~sprockets_dynamodb.exceptions.DynamoDBException`
            :exc:`~sprockets_dynamodb.exceptions.ConfigNotFound`
            :exc:`~sprockets_dynamodb.exceptions.NoCredentialsError`
            :exc:`~sprockets_dynamodb.exceptions.NoProfileError`
            :exc:`~sprockets_dynamodb.exceptions.TimeoutException`
            :exc:`~sprockets_dynamodb.exceptions.RequestException`
            :exc:`~sprockets_dynamodb.exceptions.InternalFailure`
            :exc:`~sprockets_dynamodb.exceptions.LimitExceeded`
            :exc:`~sprockets_dynamodb.exceptions.MissingParameter`
            :exc:`~sprockets_dynamodb.exceptions.OptInRequired`
            :exc:`~sprockets_dynamodb.exceptions.ResourceInUse`
            :exc:`~sprockets_dynamodb.exceptions.RequestExpired`
            :exc:`~sprockets_dynamodb.exceptions.ResourceNotFound`
            :exc:`~sprockets_dynamodb.exceptions.ServiceUnavailable`
            :exc:`~sprockets_dynamodb.exceptions.ThroughputExceeded`
            :exc:`~sprockets_dynamodb.exceptions.ValidationException`

        """
        measurements = collections.deque([], self._max_retries)
        for attempt in range(1, self._max_retries + 1):
            try:
                result = yield self._execute(
                    action, parameters, attempt, measurements)
            except (exceptions.InternalServerError,
                    exceptions.RequestException,
                    exceptions.ThrottlingException,
                    exceptions.ThroughputExceeded,
                    exceptions.ServiceUnavailable) as error:
                if attempt == self._max_retries:
                    if self._instrumentation_callback:
                        self._instrumentation_callback(measurements)
                    self._on_exception(error)
                duration = self._sleep_duration(attempt)
                self.logger.warning('%r on attempt %i, sleeping %.2f seconds',
                                    error, attempt, duration)
                yield gen.sleep(duration)
            except exceptions.DynamoDBException as error:
                if self._instrumentation_callback:
                    self._instrumentation_callback(measurements)
                self._on_exception(error)
            else:
                if self._instrumentation_callback:
                    self._instrumentation_callback(measurements)
                self.logger.debug('%s result: %r', action, result)
                raise gen.Return(_unwrap_result(action, result))

    def set_error_callback(self, callback):
        """Assign a method to invoke when a request has encountered an
        unrecoverable error in an action execution.

        :param method callback: The method to invoke

        """
        self.logger.debug('Setting error callback: %r', callback)
        self._on_error = callback

    def set_instrumentation_callback(self, callback):
        """Assign a method to invoke when a request has completed gathering
        measurements.

        :param method callback: The method to invoke

        """
        self.logger.debug('Setting instrumentation callback: %r', callback)
        self._instrumentation_callback = callback

    def _execute(self, action, parameters, attempt, measurements):
        """Invoke a DynamoDB action

        :param str action: DynamoDB action to invoke
        :param dict parameters: parameters to send into the action
        :param int attempt: Which attempt number this is
        :param list measurements: A list for accumulating request measurements
        :rtype: tornado.concurrent.Future

        """
        future = concurrent.Future()
        start = time.time()

        def handle_response(request):
            """Invoked by the IOLoop when fetch has a response to process.

            :param tornado.concurrent.Future request: The request future

            """
            self._on_response(
                action, parameters.get('TableName', 'Unknown'), attempt,
                start, request, future, measurements)

        ioloop.IOLoop.current().add_future(self._client.fetch(
            'POST', '/',
            body=json.dumps(parameters).encode('utf-8'),
            headers={
                'x-amz-target': 'DynamoDB_20120810.{}'.format(action),
                'Content-Type': 'application/x-amz-json-1.0',
            }), handle_response)
        return future

    def _on_exception(self, error):
        """Handle exceptions that can not be retried.

        :param error: The exception that was raised
        :type error: sprockets_dynamodb.exceptions.DynamoDBException

        """
        if not self._on_error:
            raise error
        self._on_error(error)

    def _on_response(self, action, table, attempt, start, response, future,
                     measurements):
        """Invoked when the HTTP request to the DynamoDB has returned and
        is responsible for setting the future result or exception based upon
        the HTTP response provided.

        :param str action: The action that was taken
        :param str table: The table name the action was made against
        :param int attempt: The attempt number for the action
        :param float start: When the request was submitted
        :param tornado.concurrent.Future response: The HTTP request future
        :param tornado.concurrent.Future future: The action execution future
        :param list measurements: The measurement accumulator

        """
        self.logger.debug('%s on %s request #%i = %r',
                          action, table, attempt, response)
        now, exception = time.time(), None
        try:
            future.set_result(self._process_response(response))
        except aws_exceptions.ConfigNotFound as error:
            exception = exceptions.ConfigNotFound(str(error))
        except aws_exceptions.ConfigParserError as error:
            exception = exceptions.ConfigParserError(str(error))
        except aws_exceptions.NoCredentialsError as error:
            exception = exceptions.NoCredentialsError(str(error))
        except aws_exceptions.NoProfileError as error:
            exception = exceptions.NoProfileError(str(error))
        except aws_exceptions.AWSError as error:
            exception = exceptions.DynamoDBException(error)
        except (ConnectionError, ConnectionResetError, OSError,
                aws_exceptions.RequestException, ssl.SSLError,
                _select.error, ssl.socket_error, socket.gaierror) as error:
            exception = exceptions.RequestException(str(error))
        except TimeoutError:
            exception = exceptions.TimeoutException()
        except httpclient.HTTPError as error:
            if error.code == 599:
                exception = exceptions.TimeoutException()
            else:
                exception = exceptions.RequestException(
                    getattr(getattr(error, 'response', error),
                            'body', str(error.code)))
        except Exception as error:
            exception = error

        if exception:
            future.set_exception(exception)

        measurements.append(
            Measurement(now, action, table, attempt, max(now, start) - start,
                        exception.__class__.__name__
                        if exception else exception))

    @staticmethod
    def _process_response(response):
        """Process the raw AWS response, returning either the mapped exception
        or deserialized response.

        :param tornado.concurrent.Future response: The request future
        :rtype: dict or list
        :raises:  sprockets_dynamodb.exceptions.DynamoDBException

        """
        error = response.exception()
        if error:
            if isinstance(error, aws_exceptions.AWSError):
                if error.args[1]['type'] in exceptions.MAP:
                    raise exceptions.MAP[error.args[1]['type']](
                        error.args[1]['message'])
            raise error
        http_response = response.result()
        if not http_response or not http_response.body:
            raise exceptions.DynamoDBException('empty response')
        return json.loads(http_response.body.decode('utf-8'))

    @staticmethod
    def _sleep_duration(attempt):
        """Calculates how long to sleep between exceptions. Returns a value
        in seconds.

        :param int attempt: The attempt number
        :rtype: float

        """
        return (float(2 ** attempt) * 100) / 1000


def _unwrap_result(action, result):
    """Unwrap a request response and return only the response data.

    :param str action: The action name
    :param result: The result of the action
    :type: result: list or dict
    :rtype: dict | None

    """
    if not result:
        return
    elif action in {'DeleteItem', 'PutItem', 'UpdateItem'}:
        return _unwrap_delete_put_update_item(result)
    elif action == 'GetItem':
        return _unwrap_get_item(result)
    elif action == 'Query' or action == 'Scan':
        return _unwrap_query_scan(result)
    elif action == 'CreateTable':
        return _unwrap_create_table(result)
    elif action == 'DescribeTable':
        return _unwrap_describe_table(result)
    return result


def _unwrap_delete_put_update_item(result):
    response = {
       'Attributes': utils.unmarshall(result['Attributes'] if result else {})
    }
    if 'ConsumedCapacity' in result:
        response['ConsumedCapacity'] = result['ConsumedCapacity']
    if 'ItemCollectionMetrics' in result:
        response['ItemCollectionMetrics'] = {
            'ItemCollectionKey': utils.unmarshall(
                result['ItemCollectionMetrics'].get('ItemCollectionKey', {})),
            'SizeEstimateRangeGB':
                result['ItemCollectionMetrics'].get('SizeEstimateRangeGB',
                                                    [None]).pop()
        }
    return response


def _unwrap_get_item(result):
    response = {
       'Item': utils.unmarshall(result['Item'] if result else {})
    }
    if 'ConsumedCapacity' in result:
        response['ConsumedCapacity'] = result['ConsumedCapacity']
    return response


def _unwrap_query_scan(result):
    response = {
        'Count': result.get('Count', 0),
        'Items': [utils.unmarshall(i) for i in result.get('Items', [])],
        'ScannedCount': result.get('ScannedCount', 0)
    }
    if 'LastEvaluatedKey' in result:
        response['LastEvaluatedKey'] = \
            utils.unmarshall(result['LastEvaluatedKey'])
    if 'ConsumedCapacity' in result:
        response['ConsumedCapacity'] = result['ConsumedCapacity']
    return response


def _unwrap_create_table(result):
    return result['TableDescription']


def _unwrap_describe_table(result):
    return result['Table']


def _validate_return_consumed_capacity(value):
    if value not in ['INDEXES', 'TOTAL', 'NONE']:
        raise ValueError('Invalid return_consumed_capacity value')


def _validate_return_item_collection_metrics(value):
    if value not in ['NONE', 'SIZE']:
        raise ValueError('Invalid return_item_collection_metrics value')


def _validate_return_values(value):
    if value not in ['NONE', 'ALL_NEW', 'ALL_OLD',
                     'UPDATED_NEW', 'UPDATED_OLD']:
        raise ValueError('Invalid return_values value')


def _validate_select(value):
    if value not in ['ALL_ATTRIBUTES', 'ALL_PROJECTED_ATTRIBUTES', 'COUNT',
                     'SPECIFIC_ATTRIBUTES']:
        raise ValueError('Invalid select value')
