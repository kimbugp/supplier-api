from datetime import timedelta
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.diagnostics import PingState
from couchbase.exceptions import (
    CouchbaseException,
)

from couchbase.options import ClusterOptions, LockMode, ClusterTimeoutOptions


class CouchbaseClient(object):
    def __init__(self, host, bucket, username, pw):
        self.host = host
        self.bucket_name = bucket
        self.username = username
        self.password = pw

    def connect(self, **kwargs):
        print('Connecting to couchbase database')
        try:
            timeout_opts = ClusterTimeoutOptions(
                kv_timeout=timedelta(seconds=60),
                connect_timeout=timedelta(seconds=60),
                query_timeout=timedelta(seconds=60))
            auth = PasswordAuthenticator(self.username, self.password)
            self._cluster = Cluster('couchbase://{}'.format(self.host),
                                    ClusterOptions(auth, timeout_options=timeout_opts), **kwargs)
            self._cluster.wait_until_ready(timedelta(seconds=5))
        except CouchbaseException as error:
            print(f"Could not connect to cluster. Error: {error}")
            raise

        self._bucket = self._cluster.bucket(self.bucket_name)
        # try:
        #     # create index if it doesn't exist
        #     createIndexProfile = f"CREATE PRIMARY INDEX default_profile_index ON {self.bucket_name}.{self.scope_name}.{self.collection_name}"
        #     createIndex = f"CREATE PRIMARY INDEX ON {self.bucket_name}"

        #     self._cluster.query(createIndexProfile).execute()
        #     self._cluster.query(createIndex).execute()
        # except CouchbaseException as e:
        #     print("Index already exists")
        # except Exception as e:
        #     print(f"Error: {type(e)}{e}")
        print('Connection complete')

    def ping(self):
        try:
            result = self._cluster.ping()
            for _, reports in result.endpoints.items():
                for report in reports:
                    if not report.state == PingState.OK:
                        return False
            return True
        except AttributeError:
            return False

    def get(self, key):
        return self._collection.get(key)

    def insert(self, key, doc):
        return self._collection.insert(key, doc)

    def upsert(self, key, doc):
        return self._collection.upsert(key, doc)

    def remove(self, key):
        return self._collection.remove(key)

    def query(self, strQuery, *options, **kwargs):
        return self._cluster.query(strQuery, *options, **kwargs)
