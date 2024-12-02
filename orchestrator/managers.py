import docker
from docker.errors import ImageNotFound, DockerException

from common.utils import generate_uuid


class MonitoringContainerManager:
    def __init__(self, image_name="monitoring:0.0.5", path_to_dockerfile="."):
        self.client = docker.from_env()
        self.image_name = image_name

        # Build the Docker image if it doesn't exist
        self.build_image(path_to_dockerfile=path_to_dockerfile)

    def build_image(self, path_to_dockerfile="."):
        try:
            self.client.images.get(name=self.image_name)
            print(f"Image '{self.image_name}' already exists. Skipping build.")
        except ImageNotFound:
            print(f"Building the Docker image '{self.image_name}'...")
            _, build_logs = self.client.images.build(path=path_to_dockerfile, tag=self.image_name)
            for log in build_logs:
                print(log.get('stream', '').strip())

    def create_monitoring_container(self, app_url, username=None, password=None):
        try:
            print(f"Starting container for URL: {app_url}...")
            name = f"monitoring-{generate_uuid()}"
            print(f"Container name: {name}")
            container = self.client.containers.run(
                image=self.image_name,
                detach=True,
                environment={
                    "APP_URL": app_url,
                    "USERNAME": username,
                    "PASSWORD": password
                },
                name=name
            )
            # Wait for the container to finish execution
            status_code = container.wait()
            logs = container.logs().decode("utf-8")
            container.remove()

            for log in logs.splitlines():
                print(log.strip())

            if status_code["StatusCode"] != 0:
                print(f"Container for {app_url} exited with errors.")
                return {"url": app_url, "status": "error", "logs": logs}

            return {"url": app_url, "status": "success", "logs": logs}

        except DockerException as e:
            error_message = f"Error while running container for {app_url}: {str(e)}"
            print(error_message)
            return {"url": app_url, "status": "error", "logs": error_message}
