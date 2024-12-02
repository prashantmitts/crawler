import json
import os

from monitoring.managers import Crawler


def main():
    print("Starting the crawler...")

    # Load inputs from environment variables
    # app_url = os.getenv("APP_URL")
    app_url = "https://news.google.com"
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if not app_url:
        raise ValueError("APP_URL environment variable is required.")
    print(f"Session starting for URL: {app_url}")

    # crawler = Crawler(chrome_driver_path="/usr/bin/chromedriver")
    crawler = Crawler()

    try:
        result = crawler.crawl(app_url, username, password)
        # print(json.dumps(result, indent=2))  # Print or save the result as needed
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Stopping the browser session...")
        crawler.stop()


if __name__ == "__main__":
    main()
