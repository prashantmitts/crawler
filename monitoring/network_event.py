import json
from abc import ABC, abstractmethod

from utils import get_response_body


class NetworkEvent(ABC):
    def __init__(self, url, headers, metadata):
        self.url = url
        self.headers = headers
        self.metadata = metadata

    def __repr__(self):
        return f"<NetworkEvent url={self.url}>"

    @classmethod
    @abstractmethod
    def from_message(cls, message, driver):
        raise NotImplementedError("This method should be implemented in subclasses.")


class RequestWillBeSentNetworkEvent(NetworkEvent):
    def __init__(self, url, headers, metadata):
        super().__init__(url, headers, metadata)

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
            }
        )


class ResponseReceivedNetworkEvent(NetworkEvent):
    def __init__(self, url, headers, metadata):
        super().__init__(url, headers, metadata)

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
            }
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

            if method == "Network.responseReceived":
                return ResponseReceivedNetworkEvent.from_message(message, driver)
            elif method == "Network.requestWillBeSent":
                return RequestWillBeSentNetworkEvent.from_message(message, driver)
            else:
                print(f"Unhandled network event: {method}")
                return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error processing log: {e}")
            return None
