"""
Main entry point for Selenium Network Logger.

Demonstrates importing NetworkLogger as a core reusable module and running
selectable workflow modules (Basic Usage, CI Pipeline, Outlook Monitoring).
"""

import sys
import os

# Ensure project root is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from network_logger import NetworkLogger
from examples.basic_usage import run_connected_example
from examples.ci_pipeline import run_ci_network_test


def main():
    print("==========================================")
    print("🌐 Selenium Network Logger - Core Runner")
    print("==========================================")
    
    # 1. Run Connected Usage Workflow
    print("\n---> Running Basic Connected Workflow...")
    run_connected_example()

    # 2. Run CI Pipeline Quality Gate Workflow
    print("\n---> Running CI/CD Quality Gate Workflow...")
    run_ci_network_test()

    print("\n✅ All Network Logger workflows executed successfully!")


if __name__ == "__main__":
    main()
