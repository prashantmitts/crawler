from common.utils import load_json_file
from orchestrator.orchestrator import orchestrate


def main():
    """Main entry point for orchestrating monitoring tasks."""
    results = orchestrate(inputs=load_json_file("inputs.json"))

    # Print results in formatted JSON
    # for result in results:
    #     print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
