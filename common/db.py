import json  # Add this for JSON serialization

import psycopg2


class Database:
    def __init__(self, config: dict):
        self.config = config
        self.conn = psycopg2.connect(**self.config)
        self.cursor = self.conn.cursor()

    def store_network_call(self, network_call):
        query = """
            INSERT INTO network_calls (url, headers, metadata)
            VALUES (%s, %s, %s)
        """
        url = network_call["url"]
        headers = json.dumps(network_call["headers"])  # Serialize dict to JSON
        metadata = json.dumps(network_call["metadata"])  # Serialize dict to JSON

        self.cursor.execute(query, (url, headers, metadata))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
