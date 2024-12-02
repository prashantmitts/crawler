from multiprocessing import Pool

from common.managers import ConfigManager
from orchestrator.managers import MonitoringContainerManager

# Initialize the global config manager
config_manager = ConfigManager(config_files=["configs/orchestrator_configs.json"])
container_manager = MonitoringContainerManager()


def run_task(input_data):
    """Run monitoring container for each input data."""
    return container_manager.create_monitoring_container(
        app_url=input_data.get('app_url'),
        username=input_data.get('username'),
        password=input_data.get('password')
    )


def orchestrate(inputs):
    """Orchestrate the monitoring process using multiprocessing."""
    # Use multiprocessing pool to parallelize the tasks
    with Pool(config_manager.get("pool_size", 2)) as pool:
        results = pool.map(run_task, inputs)

    return results
