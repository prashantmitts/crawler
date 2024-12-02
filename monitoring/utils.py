def get_response_body(driver, request_id):
    """Fetch the response body using Network.getResponseBody."""
    try:
        response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
        return response_body.get('body', None) if response_body else None
    except Exception as e:
        print(f"Error fetching response body: {e}")
        return None
