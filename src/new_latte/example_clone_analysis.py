#!/usr/bin/env python3
"""
Example script demonstrating repository cloning and analysis functionality.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from new_latte.crew import NewLatte
from new_latte.tools.repository_cloner import clone_and_analyze_repository


def main():
    """Main function to demonstrate repository cloning and analysis."""
    
    # Example repository URL
    repo_url = "https://github.com/joaomdmoura/crewAI"
    
    print(f"🔍 Analyzing repository: {repo_url}")
    print("=" * 50)
    
    # Method 1: Direct tool usage
    print("📋 Method 1: Direct tool usage")
    print("-" * 30)
    
    result = clone_and_analyze_repository(repo_url)
    
    if result['success']:
        print(f"✅ Successfully cloned repository to: {result['repo_path']}")
        print(f"📊 Analysis summary:")
        print(f"   - Total files: {len(result['analysis']['files'])}")
        print(f"   - Python files: {len(result['analysis']['python_files'])}")
        print(f"   - Config files: {len(result['analysis']['config_files'])}")
        print(f"   - Directories: {len(result['analysis']['directories'])}")
    else:
        print(f"❌ Failed to clone repository: {result['error']}")
    
    print("\n" + "=" * 50)
    
    # Method 2: Using CrewAI agents
    print("🤖 Method 2: Using CrewAI agents")
    print("-" * 30)
    
    try:
        # Initialize the crew
        crew = NewLatte()
        
        # Create a task for repository analysis
        # Note: In a real scenario, you would use the crew.run() method
        # with the appropriate task configuration
        
        print("✅ Crew initialized successfully")
        print("📝 Available agents:")
        for agent_name in crew.agents_config.keys():
            print(f"   - {agent_name}")
        
        print("\n📝 Available tasks:")
        for task_name in crew.tasks_config.keys():
            print(f"   - {task_name}")
            
    except Exception as e:
        print(f"❌ Error initializing crew: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Repository cloning and analysis demonstration complete!")


if __name__ == "__main__":
    main() 