import argparse
from .utils.logger import logger
from .agents.orchestrator import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="Agentic Report Runner")
    parser.add_argument("--once", action="store_true", help="Run once and exit (default)")
    args = parser.parse_args()
    logger.info("Starting Agentic Report Runner...")
    run_pipeline()

if __name__ == "__main__":
    main()
