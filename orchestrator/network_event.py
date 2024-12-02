# crawling/network_event.py

class NetworkEvent:
    def __init__(self, url, method, status, mime_type, headers, body=None, post_data=None):
        self.url = url
        self.method = method
        self.status = status
        self.mime_type = mime_type
        self.headers = headers
        self.body = body
        self.post_data = post_data

    def __repr__(self):
        return f"<NetworkEvent url={self.url} status={self.status} method={self.method}>"
