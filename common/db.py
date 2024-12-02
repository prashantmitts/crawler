import json

import psycopg2

from monitoring.network_event import NetworkEvent


class Database:
    def __init__(self, config: dict):
        self.config = config
        self.conn = psycopg2.connect(**self.config)
        self.cursor = self.conn.cursor()

    def store_network_call(self, session_id, network_call: NetworkEvent):
        query = """
            INSERT INTO network_calls (url, headers, metadata, event, session_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        url = network_call.url
        headers = json.dumps(network_call.headers)  # Serialize dict to JSON
        metadata = json.dumps(network_call.metadata)  # Serialize dict to JSON
        event = network_call.event

        self.cursor.execute(query, (url, headers, metadata, event, session_id))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
