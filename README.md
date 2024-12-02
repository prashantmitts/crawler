# **Selenium-Based Crawler with Dockerized Orchestration**

This project provides a scalable, containerized solution to crawl web pages using Selenium WebDriver, orchestrated with
Python multiprocessing and Docker. The solution captures network traffic and optionally performs login operations based
on provided credentials (if the url requires to be authenticated).

## **Features**

- **Dockerized Crawlers**: Each crawl runs in an isolated Docker container.
- **Selenium Manager**: A centralized manager handles Selenium WebDriver setup, network traffic logging, and browser
  operations.
- **Concurrent Execution**: Utilize multiprocessing to handle multiple inputs concurrently.
- **Flexible Configuration**: Manage configuration settings using a configuration manager for scalability and
  customization.
- **Dynamic Inputs**: Accept environment variables and JSON files for dynamic input handling.
- **Postgres Storage**: Network call data stored in postgres table.

## **Assumptions**

1. The crawler is designed to work with Selenium WebDriver and Chrome browser.
2. Selenium provides multiple types of network events such as
    1. Network.dataReceived
    2. Network.loadingFailed
    3. Network.loadingFinished
    4. Network.policyUpdated
    5. **Network.requestWillBeSent**
    6. Network.requestWillBeSentExtraInfo
    7. Network.resourceChangedPriority
    8. **Network.responseReceived**
    9. Network.responseReceivedExtraInfo
    10. Page.domContentEventFired
    11. Page.frameNavigated
    12. Page.frameResized
    13. Page.frameStartedLoading
    14. Page.frameStoppedLoading
    15. Page.loadEventFired
    16. Page.navigatedWithinDocument

out of these only 2 are being extracted and stored (bold) in the database. which felt to be useful for the analysis.

3. We are not crawling the page, network calls are being captured and stored in the database until the page loads fully,
   crawling is out of scope though which can be implemented easily with current code.

## **Design choices**

1. **Dockerized Crawlers**: Each crawl runs in an isolated Docker container. This allows for a scalable and secure
   solution, as each crawl is independent of the others.
2. **Pool of Selenium Drivers**: A pool of Selenium drivers is suitable design choice as if there are 10k urls to scrawl
   on the number of containers need to be a fix size assuming 500-1000 containers running simultaneously.
3. **Postgres Storage**: Network call data is stored in a postgres table. This allows for easy querying and analysis of
   the data.

## **Future considerations**

1. We can add more network events to be stored in the database.
2. We can have priority based crawling, where we can crawl the pages based on the priority.
3. We can have suspendable jobs to ensure that there is no starvation of the jobs scheduled.

## **Installation**

### **Prerequisites**

- Python 3.9 or above
- Docker installed and running (for MacOs and Windows, Docker Desktop is recommended)
- Required Python libraries listed in `requirements.txt`

### **Setup**

1. **Clone the Repository**:

```bash
   git clone https://github.com/prashantmitts/crawler.git
   cd crawler
```

```
    pip install -r requirements.txt
```

2. **Configure inputs.json**:  
   Update the inputs.json file with the URLs and credentials for the crawlers. The file
   should contain a list of dictionaries, each containing the URL, username, and password for a crawl.

```
[
  {
    "url": "https://www.example.com",
    "username": "user1",
    "password": "password1"
  },
  {
    "url": "https://www.example.com",
    "username": "user2",
    "password": "password2"
  },
  {
    "url": "https://news.google.com"
  }
]
```

3. **Configure configs**:
    1. ``configs/db_configs.py`` for postgres database configs or create database in postgres
    2. ``configs/orchestrator_configs.py`` for orchestrator configurations

4. Create a postgres database and table using the following command:

```
CREATE TABLE network_calls (
    id SERIAL PRIMARY KEY,
    url TEXT,
    headers JSON,
    metadata JSON,
    event TEXT,
    session_id TEXT
);
```

5. **Run the program**:

```
    python main.py
```
