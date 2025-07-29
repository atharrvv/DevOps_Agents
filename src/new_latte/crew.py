from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tools import tool
from typing import List
import os
import subprocess
import requests
import json
from pathlib import Path
import tempfile
import shutil
from urllib.parse import urlparse

# Define all custom tools inline using @tool decorator
@tool
def clone_repository(repo_url: str, target_dir: str = "./cloned_repo") -> str:
    """Clone a Git repository to a local folder named 'cloned_repo'"""
    try:
        # Create target_dir if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

        # Clone the repository
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url, target_dir], 
            capture_output=True, 
            text=True, 
            timeout=300
        )

        if result.returncode != 0:
            return f"Failed to clone repository: {result.stderr}"
        
        return f"Successfully cloned repository to: {os.path.abspath(target_dir)}"

    except subprocess.TimeoutExpired:
        return "Repository cloning timed out after 5 minutes"
    except Exception as e:
        return f"Error cloning repository: {str(e)}"

# @tool
# def clone_repository(repo_url: str, target_dir: str = None) -> str:
#     """Clone a Git repository to analyze its structure and files"""
#     try:
#         if target_dir is None:
#             # Create a temporary directory
#             target_dir = tempfile.mkdtemp(prefix="repo_analysis_")
        
#         # Clone the repository
#         result = subprocess.run(
#             ['git', 'clone', '--depth', '1', repo_url, target_dir], 
#             capture_output=True, 
#             text=True, 
#             timeout=300
#         )
        
#         if result.returncode != 0:
#             return f"Failed to clone repository: {result.stderr}"
        
#         return f"Successfully cloned repository to: {target_dir}"
    
#     except subprocess.TimeoutExpired:
#         return "Repository cloning timed out after 5 minutes"
#     except Exception as e:
#         return f"Error cloning repository: {str(e)}"

@tool
def analyze_repository_structure(repo_path: str) -> str:
    """Analyze the structure of a cloned repository"""
    try:
        if not os.path.exists(repo_path):
            return f"Repository path does not exist: {repo_path}"
        
        structure_info = {
            "files_found": {
                "test_directories": {"exists": False, "locations": []},
                "build_configuration": {"exists": False, "files": []},
                "dependency_management": {"exists": False, "files": []}
            }
        }
        
        # Check for test directories
        test_dirs = ['tests', 'test', 'testing']
        for test_dir in test_dirs:
            test_path = os.path.join(repo_path, test_dir)
            if os.path.isdir(test_path):
                structure_info["files_found"]["test_directories"]["exists"] = True
                structure_info["files_found"]["test_directories"]["locations"].append(test_dir + "/")
        
        # Check for build configuration files
        build_files = ['pyproject.toml', 'setup.py', 'setup.cfg']
        for build_file in build_files:
            file_path = os.path.join(repo_path, build_file)
            if os.path.isfile(file_path):
                structure_info["files_found"]["build_configuration"]["exists"] = True
                structure_info["files_found"]["build_configuration"]["files"].append(build_file)
        
        # Check for dependency files
        dep_files = ['requirements.txt', 'pyproject.toml', 'Pipfile', 'poetry.lock']
        for dep_file in dep_files:
            file_path = os.path.join(repo_path, dep_file)
            if os.path.isfile(file_path):
                structure_info["files_found"]["dependency_management"]["exists"] = True
                structure_info["files_found"]["dependency_management"]["files"].append(dep_file)
        
        # Generate directory tree
        tree_output = []
        for root, dirs, files in os.walk(repo_path):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')
            
            level = root.replace(repo_path, '').count(os.sep)
            indent = '  ' * level
            tree_output.append(f"{indent}{os.path.basename(root)}/")
            
            subindent = '  ' * (level + 1)
            for file in files[:10]:  # Limit to first 10 files per directory
                tree_output.append(f"{subindent}{file}")
            
            if len(files) > 10:
                tree_output.append(f"{subindent}... and {len(files) - 10} more files")
        
        result = f"Repository Structure Analysis:\n"
        result += f"Directory Tree:\n" + "\n".join(tree_output[:50])  # Limit output
        result += f"\n\nStructure Summary:\n{json.dumps(structure_info, indent=2)}"
        
        return result
        
    except Exception as e:
        return f"Error analyzing repository structure: {str(e)}"

@tool
def read_file_content(file_path: str, max_lines: int = 100) -> str:
    """Read and return content of a specific file with line limit"""
    try:
        if not os.path.exists(file_path):
            return f"File does not exist: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        if len(lines) <= max_lines:
            content = ''.join(lines)
        else:
            content = ''.join(lines[:max_lines])
            content += f"\n... (File truncated. Showing first {max_lines} lines of {len(lines)} total lines)"
        
        return f"Content of {file_path}:\n{content}"
        
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

@tool
def detect_python_frameworks(repo_path: str) -> str:
    """Detect Python testing frameworks and build tools in the repository"""
    try:
        frameworks_found = {
            "testing_framework": "none",
            "build_tool": "none",
            "web_framework": "none"
        }
        
        # Check requirements files and pyproject.toml for framework indicators
        req_files = ['requirements.txt', 'requirements-dev.txt', 'pyproject.toml']
        
        for req_file in req_files:
            file_path = os.path.join(repo_path, req_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    
                # Test framework detection
                if 'pytest' in content:
                    frameworks_found["testing_framework"] = "pytest"
                elif 'unittest' in content or 'test' in content:
                    frameworks_found["testing_framework"] = "unittest"
                
                # Build tool detection
                if 'poetry' in content:
                    frameworks_found["build_tool"] = "poetry"
                elif 'setuptools' in content or 'setup.py' in os.listdir(repo_path):
                    frameworks_found["build_tool"] = "setuptools"
                
                # Web framework detection
                if 'django' in content:
                    frameworks_found["web_framework"] = "django"
                elif 'flask' in content:
                    frameworks_found["web_framework"] = "flask"
                elif 'fastapi' in content:
                    frameworks_found["web_framework"] = "fastapi"
        
        return f"Detected Frameworks:\n{json.dumps(frameworks_found, indent=2)}"
        
    except Exception as e:
        return f"Error detecting frameworks: {str(e)}"

@tool
def generate_workflow_yaml(workflow_content: str, filename: str = "workflow.yaml") -> str:
    """Generate and save a YAML workflow file"""
    try:
        # Ensure the content is properly formatted
        if not workflow_content.strip().startswith('name:'):
            return "Invalid workflow content. Must start with 'name:' field."
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        
        return f"Workflow successfully saved to {filename}"
        
    except Exception as e:
        return f"Error saving workflow: {str(e)}"

@tool
def cleanup_temp_directory(dir_path: str) -> str:
    """Clean up temporary directories after analysis"""
    try:
        if os.path.exists(dir_path) and 'tmp' in dir_path:
            shutil.rmtree(dir_path)
            return f"Successfully cleaned up temporary directory: {dir_path}"
        else:
            return f"Directory not cleaned up (safety check failed): {dir_path}"
    except Exception as e:
        return f"Error cleaning up directory: {str(e)}"

@CrewBase
class NewLatte():
    """NewLatte crew"""
    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self):
        super().__init__()
        # Configure Azure OpenAI LLM
        self.llm = LLM(
            model="azure/gpt-4o",
            base_url=os.getenv("AZURE_API_BASE"),
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION")
        )
   
    # These agent names MUST match the names in your agents.yaml
    @agent
    def test_build_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['test_build_analyst'],
            tools=[
                clone_repository,
                analyze_repository_structure,
                read_file_content,
                detect_python_frameworks
            ],
            verbose=True,
            llm=self.llm
        )
   
    @agent
    def github_workflow_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['github_workflow_generator'],
            tools=[
                generate_workflow_yaml,
                read_file_content
            ],
            verbose=True,
            llm=self.llm
        )

    # These task names MUST match the names in your tasks.yaml
    @task
    def analyze_test_build_setup(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_test_build_setup'],
        )
   
    @task
    def generate_test_build_workflow(self) -> Task:
        return Task(
            config=self.tasks_config['generate_test_build_workflow'],
            output_file='workflows.yaml'
        )
   
    @crew
    def crew(self) -> Crew:
        """Creates the NewLatte crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )












# from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
# from crewai.agents.agent_builder.base_agent import BaseAgent
# # from langchain_openai import AzureChatOpenAI as LLM
# from crewai import Agent, Task, Crew, Process, LLM
# from typing import List
# import os
# from .tools.tool_registry import get_tool_registry, get_tool

# @CrewBase
# class NewLatte():
#     """NewLatte crew"""
#     agents: List[BaseAgent]
#     tasks: List[Task]
    
#     def __init__(self):
#         super().__init__()
#         # Configure Azure OpenAI LLM
#         # self.llm = LLM(
#         #     api_key=os.getenv("AZURE_API_KEY"),
#         #     azure_endpoint=os.getenv("AZURE_API_BASE"),
#         #     api_version=os.getenv("AZURE_API_VERSION"),
#         #     azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME")
#         # )

#         self.llm = LLM(
#             model="azure/gpt-4o",
#             base_url=os.getenv("AZURE_API_BASE"),
#             api_key=os.getenv("AZURE_API_KEY"),
#             api_version=os.getenv("AZURE_API_VERSION")
#                 )
   
#     # These agent names MUST match the names in your agents.yaml
#     @agent
#     def test_build_analyst(self) -> Agent:
#         return Agent(
#             config=self.agents_config['test_build_analyst'],
#             verbose=True,
#             llm=self.llm
#         )
   
#     @agent
#     def github_workflow_generator(self) -> Agent:
#         return Agent(
#             config=self.agents_config['github_workflow_generator'],
#             verbose=True,
#             llm=self.llm
#         )


#     # These task names MUST match the names in your tasks.yaml
#     @task
#     def analyze_test_build_setup(self) -> Task:
#         return Task(
#             config=self.tasks_config['analyze_test_build_setup'],
#         )
   
#     @task
#     def generate_test_build_workflow(self) -> Task:
#         return Task(
#             config=self.tasks_config['generate_test_build_workflow'],
#             output_file='workflows.yaml'
#         )

#     # @task
#     # def create_deployment_configurations(self) -> Task:
#     #     return Task(
#     #         config=self.tasks_config['create_deployment_configurations'],
#     #         output_file='deployment_config.yaml'
#     #     )
   
#     # @task
#     # def create_deployment_documentation(self) -> Task:
#     #     return Task(
#     #         config=self.tasks_config['create_deployment_documentation'],
#     #         output_file='deployment_docs.md'
#     #     )
   
#     @crew
#     def crew(self) -> Crew:
#         """Creates the NewLatte crew"""
#         return Crew(
#             agents=self.agents,
#             tasks=self.tasks,
#             process=Process.sequential,
#             verbose=True,
#         )
    
















    
