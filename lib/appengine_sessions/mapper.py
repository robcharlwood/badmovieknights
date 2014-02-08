# import python deps
import operator
import logging

# import google deps
from google.appengine.ext import deferred
from google.appengine.runtime import DeadlineExceededError
from google.appengine.api.datastore_errors import TransactionFailedError

# Number of entities fetched in a deferred task
DEFERRED_BATCH_SIZE = 250


# query mapper
class QueryMapper(object):
    """
        Iterates over an ndb filtered query. Runs iterations in a
        deferred task.

        If mapping needs to scale, mapreduce should be used instead.
        We'll need to make that work with ndb.  Start here:
        http://code.google.com/p/appengine-mapreduce/wiki/UserGuidePython

        Query and filters are passed into `map` and evaluated in a way
        that looks strange, but is necessary to keep deferred happy when
        pickling arguments.
    """

    def __init__(
            self, model, filters=None, ancestor=None,
            queue='default', deferred_batch_size=DEFERRED_BATCH_SIZE):

        self.model = model
        self.filters = filters
        self.ancestor = ancestor
        self.queue = queue
        self.cursor = None
        self.deferred_batch_size = deferred_batch_size

        logging.info('Mapper `%s` created' % self.__class__.__name__)

    def process_key(self, key):
        """
        Specialise this no-op.
        """
        logging.info('processing key %s' % str(key))

    def transaction(self):
        # Build up the query in iteration, to keep deferred happy
        query = self.model.query(ancestor=self.ancestor)

        if self.filters:
            for operator_str, operands in self.filters.iteritems():
                query = query.filter(getattr(
                    operator, operator_str)(self.model._properties[
                        operands[0]], operands[1]))

        # Attempt to process an entire batch
        if query.count(self.deferred_batch_size) > 0:
            keys, cursor, more = query.fetch_page(
                self.deferred_batch_size, keys_only=True,
                start_cursor=self.cursor)

            for i, key in enumerate(keys):
                self.process_key(key)

            # If there are more entities, defer another process
            if more:
                self.cursor = cursor
                deferred.defer(self.map, _queue=self.queue)

        elif self.cursor is None:
            logging.info('No entities to map over.')

    def start(self):
        """
            Don't do anything in a time constrained view. Kick of the
            first deferred task.
        """
        deferred.defer(self.map, _queue=self.queue)

    def map(self):
        try:
            self.transaction()
        except (DeadlineExceededError, TransactionFailedError):
            # We ran out of time, or the transaction failed
            deferred.defer(self.map, _queue=self.queue)


class DeleteMapper(QueryMapper):
    """
        Delete all entities mapped.
    """
    def process_key(self, key):
        # Deleting key
        logging.info('DeleteMapper deleted %s' % str(key))
        key.delete()
