import pathlib
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection

BASE_DIR = pathlib.Path(__file__).resolve().parent

ASTRA_CONNECT_BUNDLE = f"{BASE_DIR}/unencrpyted/astradb_conenct.zip"
ASTRA_CLIENT_ID = "<<CLIENT ID>>"
ASTRA_CLIENT_SECRET = "<<CLIENT SECRET>>"


def get_session():
    cloud_config = {
        'secure_connect_bundle': ASTRA_CONNECT_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    return session
