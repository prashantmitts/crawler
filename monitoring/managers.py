import json
import uuid

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.db import Database
from common.managers import ConfigManager
from monitoring.utils import get_response_body


class SeleniumManager:
    def __init__(self, chrome_driver_path=None):
        self.chrome_driver_path = chrome_driver_path
        self.driver = None
        self.db = Database(ConfigManager(config_files=["configs/db_configs.json"]).get_all())

    def configure_driver(self):
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")  # Required for Docker
        options.add_argument("--disable-gpu")  # Disable GPU acceleration
        options.add_argument("--disable-dev-shm-usage")  # Handle shared memory issues
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # Capture logs

        if self.chrome_driver_path:
            service = Service(self.chrome_driver_path)  # Ensure Chromedriver path is set
        else:
            service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)

    def start_browser(self, url):
        if not self.driver:
            self.configure_driver()

        print(f"Opening URL: {url}")
        self.driver.get(url)

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def capture_network_traffic(self):
        logs = self.driver.get_log("performance")
        print(f"Captured {len(logs)} network logs.")
        network_calls = []

        for log in logs:
            try:
                message = json.loads(log["message"])["message"]
                print("processing log message: ", message["method"])
                if "Network.responseReceived" in message["method"]:
                    response = message["params"].get("response", {})
                    request_id = message["params"].get("requestId")
                    response_body = get_response_body(self.driver, request_id)

                    network_calls.append({
                        "url": response.get("url"),
                        "headers": response.get("headers", {}),
                        "metadata": {
                            "status": response.get("status"),
                            "mime_type": response.get("mimeType"),
                            "body": response_body or "N/A",  # Fetch body if available
                        }
                    })

                # Handle 'requestWillBeSent' event
                elif "Network.requestWillBeSent" in message["method"]:
                    request = message["params"].get("request", {})
                    post_data = request.get("postData")  # POST request body
                    network_calls.append({
                        "url": request.get("url"),
                        "headers": request.get("headers", {}),
                        "metadata": {
                            "method": request.get("method"),
                            "postData": post_data or "N/A",
                        }
                    })
            except Exception as e:
                print(f"Error processing log: {e}")

        for network_call in network_calls:
            self.db.store_network_call(network_call)

        return network_calls

    def quit_browser(self):
        if self.driver:
            print("Closing WebDriver session...")
            self.driver.quit()
            self.driver = None
        else:
            print("No WebDriver session found.")


class Crawler:

    def __init__(self, chrome_driver_path=None):
        self.selenium_manager = SeleniumManager(chrome_driver_path=chrome_driver_path)

    def crawl(self, app_url, username=None, password=None):
        session_id = str(uuid.uuid4())  # Generate a unique session ID
        print(f"Session starting for URL: {app_url}")

        # Start browser and navigate to app_url
        self.selenium_manager.start_browser(app_url)

        # Handle login if username and password are provided
        if username and password:
            print(f"Attempting login with username: {username}...")
            self.selenium_manager.wait_for_element(By.ID, "email").send_keys(username)
            self.selenium_manager.wait_for_element(By.ID, "pass").send_keys(password)
            self.selenium_manager.wait_for_element(By.NAME, "login").click()

        # Wait and capture network traffic
        print("Capturing network calls...")
        network_calls = self.selenium_manager.capture_network_traffic()

        return {
            "session_id": session_id,
            "app_url": app_url,
            "network_calls": network_calls,
        }

    def stop(self):
        self.selenium_manager.quit_browser()
