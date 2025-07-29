#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from new_latte.crew import NewLatte

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Ask for repo URL if not provided as a command-line argument
    if len(sys.argv) > 1:
        github_repo_url = sys.argv[1]
    else:
        github_repo_url = input("Enter the GitHub repository URL to analyze: ").strip()

    inputs = {
        'current_year': str(datetime.now().year),
        'github_repo_url': github_repo_url
    }
    
    try:
        NewLatte().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'current_year': str(datetime.now().year),
        # 'github_repo_url': 'https://github.com/atharrvv/pasportaservo.git'
    }
    try:
        NewLatte().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        NewLatte().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "current_year": str(datetime.now().year),
        # 'github_repo_url': 'https://github.com/atharrvv/pasportaservo.git'
        
    }
    
    try:
        NewLatte().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
