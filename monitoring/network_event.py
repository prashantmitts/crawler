import json
from abc import ABC, abstractmethod

from monitoring.utils import get_response_body


class NetworkEvent(ABC):
    def __init__(self, url, headers, metadata, event):
        self.url = url
        self.headers = headers
        self.metadata = metadata
        self.event = event

    def __repr__(self):
        return f"<NetworkEvent url={self.url}>"

    @classmethod
    @abstractmethod
    def from_message(cls, message, driver):
        raise NotImplementedError("This method should be implemented in subclasses.")


class RequestWillBeSentNetworkEvent(NetworkEvent):
    def __init__(self, url, headers, metadata, event):
        super().__init__(url, headers, metadata, event)

    @classmethod
    def from_message(cls, message, driver):
        request = message["params"].get("request", {})
        post_data = request.get("postData")  # POST request body
        return cls(
            url=request.get("url"),
            headers=request.get("headers", {}),
            metadata={
                "method": request.get("method"),
                "postData": post_data or "N/A",
            },
            event="requestWillBeSent"
        )


class ResponseReceivedNetworkEvent(NetworkEvent):
    def __init__(self, url, headers, metadata, event):
        super().__init__(url, headers, metadata, event)

    @classmethod
    def from_message(cls, message, driver):
        response = message["params"].get("response", {})
        request_id = message["params"].get("requestId")
        response_body = get_response_body(driver, request_id)
        return cls(
            url=response.get("url"),
            headers=response.get("headers", {}),
            metadata={
                "status": response.get("status"),
                "mime_type": response.get("mimeType"),
                "body": response_body or "N/A",  # Fetch body if available
            },
            event="responseReceived"
        )


class NetworkEventHandler:
    def __init__(self):
        pass

    @classmethod
    def handle_log(cls, log, driver):
        try:
            message = json.loads(log["message"])["message"]
            method = message.get("method")
            print("Processing log message:", method)

            network_event_map = {
                "Network.responseReceived": ResponseReceivedNetworkEvent,
                "Network.requestWillBeSent": RequestWillBeSentNetworkEvent,
            }
            if method in network_event_map:
                return network_event_map[method].from_message(message, driver)

            print(f"Unhandled network event: {method}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error processing log: {e}")
            return None
        except:
            return None
