from langchain.tools import BaseTool
from typing import Optional
from .repository_cloner import clone_and_analyze_repository


class RepositoryCloneTool(BaseTool):
    """Tool for cloning repositories locally for analysis"""
    
    name: str = "repository_clone_tool"
    description: str = """
    Clone a GitHub repository locally for analysis. 
    Use this tool when you need to analyze the actual files and structure of a repository.
    
    Input should be a GitHub repository URL (e.g., "https://github.com/user/repo")
    """
    
    def _run(self, repo_url: str) -> str:
        """
        Clone a repository and return analysis information
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            JSON string with repository analysis
        """
        import json
        
        result = clone_and_analyze_repository(repo_url)
        
        if result['success']:
            return json.dumps({
                'status': 'success',
                'repo_path': result['repo_path'],
                'repo_url': result['repo_url'],
                'analysis': result['analysis']
            }, indent=2)
        else:
            return json.dumps({
                'status': 'error',
                'error': result['error']
            }, indent=2)
    
    def _arun(self, repo_url: str) -> str:
        """Async version of the tool"""
        return self._run(repo_url)


class RepositoryAnalyzerTool(BaseTool):
    """Tool for analyzing cloned repositories"""
    
    name: str = "repository_analyzer_tool"
    description: str = """
    Analyze a cloned repository to extract detailed information about its structure, 
    dependencies, testing setup, and build configuration.
    
    Use this tool after cloning a repository to get detailed analysis.
    Input should be the repository path returned by the clone tool.
    """
    
    def _run(self, repo_path: str) -> str:
        """
        Analyze a cloned repository
        
        Args:
            repo_path: Path to the cloned repository
            
        Returns:
            JSON string with detailed analysis
        """
        import json
        import os
        from pathlib import Path
        
        if not os.path.exists(repo_path):
            return json.dumps({
                'status': 'error',
                'error': f'Repository path does not exist: {repo_path}'
            }, indent=2)
        
        analysis = {
            'status': 'success',
            'repo_path': repo_path,
            'structure': {},
            'dependencies': {},
            'testing': {},
            'build': {},
            'deployment': {}
        }
        
        try:
            # Analyze project structure
            analysis['structure'] = self._analyze_structure(repo_path)
            
            # Analyze dependencies
            analysis['dependencies'] = self._analyze_dependencies(repo_path)
            
            # Analyze testing setup
            analysis['testing'] = self._analyze_testing(repo_path)
            
            # Analyze build configuration
            analysis['build'] = self._analyze_build(repo_path)
            
            # Analyze deployment requirements
            analysis['deployment'] = self._analyze_deployment(repo_path)
            
        except Exception as e:
            analysis['status'] = 'error'
            analysis['error'] = str(e)
        
        return json.dumps(analysis, indent=2)
    
    def _arun(self, repo_path: str) -> str:
        """Async version of the tool"""
        return self._run(repo_path)
    
    def _analyze_structure(self, repo_path: str) -> dict:
        """Analyze the project structure"""
        import os
        
        structure = {
            'root_files': [],
            'directories': [],
            'python_files': [],
            'config_files': [],
            'main_entry_point': None
        }
        
        for item in os.listdir(repo_path):
            item_path = os.path.join(repo_path, item)
            if os.path.isfile(item_path):
                structure['root_files'].append(item)
                if item.endswith('.py'):
                    structure['python_files'].append(item)
                elif any(item.endswith(ext) for ext in ['.toml', '.yaml', '.yml', '.json', '.cfg', '.ini']):
                    structure['config_files'].append(item)
            elif os.path.isdir(item_path) and item != '.git':
                structure['directories'].append(item)
        
        # Try to find main entry point
        main_candidates = ['main.py', 'app.py', 'run.py', '__main__.py']
        for candidate in main_candidates:
            if candidate in structure['root_files']:
                structure['main_entry_point'] = candidate
                break
        
        return structure
    
    def _analyze_dependencies(self, repo_path: str) -> dict:
        """Analyze dependencies"""
        import os
        
        dependencies = {
            'requirements_files': [],
            'pyproject_toml': None,
            'setup_files': [],
            'pipfile': None,
            'poetry_lock': None
        }
        
        # Check for common dependency files
        dep_files = ['requirements.txt', 'requirements-dev.txt', 'requirements-test.txt']
        for file in dep_files:
            if os.path.exists(os.path.join(repo_path, file)):
                dependencies['requirements_files'].append(file)
        
        if os.path.exists(os.path.join(repo_path, 'pyproject.toml')):
            dependencies['pyproject_toml'] = 'pyproject.toml'
        
        if os.path.exists(os.path.join(repo_path, 'setup.py')):
            dependencies['setup_files'].append('setup.py')
        
        if os.path.exists(os.path.join(repo_path, 'setup.cfg')):
            dependencies['setup_files'].append('setup.cfg')
        
        if os.path.exists(os.path.join(repo_path, 'Pipfile')):
            dependencies['pipfile'] = 'Pipfile'
        
        if os.path.exists(os.path.join(repo_path, 'poetry.lock')):
            dependencies['poetry_lock'] = 'poetry.lock'
        
        return dependencies
    
    def _analyze_testing(self, repo_path: str) -> dict:
        """Analyze testing setup"""
        import os
        
        testing = {
            'test_directories': [],
            'test_files': [],
            'test_config_files': [],
            'framework': None
        }
        
        # Look for test directories
        test_dirs = ['tests', 'test', 'testsuite']
        for test_dir in test_dirs:
            test_path = os.path.join(repo_path, test_dir)
            if os.path.exists(test_path):
                testing['test_directories'].append(test_dir)
        
        # Look for test files
        for root, dirs, files in os.walk(repo_path):
            if '.git' in dirs:
                dirs.remove('.git')
            
            for file in files:
                if file.startswith('test_') or file.endswith('_test.py'):
                    rel_path = os.path.relpath(os.path.join(root, file), repo_path)
                    testing['test_files'].append(rel_path)
        
        # Look for test config files
        test_configs = ['pytest.ini', 'tox.ini', 'setup.cfg']
        for config in test_configs:
            if os.path.exists(os.path.join(repo_path, config)):
                testing['test_config_files'].append(config)
        
        # Determine framework
        if testing['test_files'] or testing['test_directories']:
            testing['framework'] = 'pytest'  # Default to pytest
        
        return testing
    
    def _analyze_build(self, repo_path: str) -> dict:
        """Analyze build configuration"""
        import os
        
        build = {
            'build_tools': [],
            'build_files': [],
            'package_type': None
        }
        
        # Check for build configuration files
        build_files = ['pyproject.toml', 'setup.py', 'setup.cfg']
        for file in build_files:
            if os.path.exists(os.path.join(repo_path, file)):
                build['build_files'].append(file)
        
        # Determine build tools
        if 'pyproject.toml' in build['build_files']:
            build['build_tools'].append('setuptools')
        elif 'setup.py' in build['build_files']:
            build['build_tools'].append('setuptools')
        
        # Determine package type
        if build['build_files']:
            build['package_type'] = 'package'
        
        return build
    
    def _analyze_deployment(self, repo_path: str) -> dict:
        """Analyze deployment requirements"""
        import os
        
        deployment = {
            'docker_files': [],
            'wsgi_files': [],
            'asgi_files': [],
            'static_files': False,
            'environment_files': []
        }
        
        # Look for Docker files
        docker_files = ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml']
        for file in docker_files:
            if os.path.exists(os.path.join(repo_path, file)):
                deployment['docker_files'].append(file)
        
        # Look for WSGI/ASGI files
        for root, dirs, files in os.walk(repo_path):
            if '.git' in dirs:
                dirs.remove('.git')
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if 'wsgi' in content or 'application' in content:
                            rel_path = os.path.relpath(file_path, repo_path)
                            deployment['wsgi_files'].append(rel_path)
                        if 'asgi' in content:
                            rel_path = os.path.relpath(file_path, repo_path)
                            deployment['asgi_files'].append(rel_path)
        
        # Look for static files
        static_dirs = ['static', 'assets', 'public']
        for static_dir in static_dirs:
            if os.path.exists(os.path.join(repo_path, static_dir)):
                deployment['static_files'] = True
                break
        
        # Look for environment files
        env_files = ['.env', '.env.example', '.env.template']
        for file in env_files:
            if os.path.exists(os.path.join(repo_path, file)):
                deployment['environment_files'].append(file)
        
        return deployment
