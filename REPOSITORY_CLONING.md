# Repository Cloning and Analysis

This document describes the repository cloning and analysis functionality added to the DevOps Agents system.

## Overview

The system now includes capabilities to:
1. **Clone repositories locally** for detailed analysis
2. **Analyze repository structure** including files, directories, and configurations
3. **Detect dependencies** and package management approaches
4. **Identify testing frameworks** and configurations
5. **Understand build tools** and packaging requirements
6. **Recognize deployment patterns** and requirements

## Components

### 1. Repository Cloner Tool (`src/new_latte/tools/repository_cloner.py`)

A utility class that handles cloning repositories to local directories:

```python
from new_latte.tools.repository_cloner import clone_and_analyze_repository

# Clone and analyze a repository
result = clone_and_analyze_repository("https://github.com/user/repo")

if result['success']:
    print(f"Repository cloned to: {result['repo_path']}")
    print(f"Analysis: {result['analysis']}")
else:
    print(f"Error: {result['error']}")
```

### 2. Custom Tools (`src/new_latte/tools/custom_tool.py`)

Two LangChain tools for use with CrewAI agents:

- **RepositoryCloneTool**: Clones repositories and returns analysis information
- **RepositoryAnalyzerTool**: Performs detailed analysis of cloned repositories

### 3. Repository Clone Analyzer Agent

A new agent (`repository_clone_analyzer`) that specializes in:
- Cloning repositories from various sources
- Analyzing project structure and file organization
- Identifying dependencies and package management approaches
- Detecting testing frameworks and configurations
- Understanding build tools and packaging requirements
- Recognizing deployment patterns and requirements

### 4. Clone and Analyze Repository Task

A new task (`clone_and_analyze_repository`) that:
- Uses the repository cloning tools
- Performs comprehensive analysis
- Outputs detailed YAML reports
- Provides information for workflow generation and deployment planning

## Usage

### Method 1: Direct Tool Usage

```python
from new_latte.tools.repository_cloner import clone_and_analyze_repository

# Clone and analyze a repository
result = clone_and_analyze_repository("https://github.com/user/repo")

if result['success']:
    print(f"Repository path: {result['repo_path']}")
    print(f"Files found: {len(result['analysis']['files'])}")
    print(f"Python files: {len(result['analysis']['python_files'])}")
    print(f"Config files: {len(result['analysis']['config_files'])}")
```

### Method 2: Using CrewAI Agents

```python
from new_latte.crew import NewLatte

# Initialize the crew
crew = NewLatte()

# The repository_clone_analyzer agent can be used in workflows
# with the clone_and_analyze_repository task
```

### Method 3: Running the Example

```bash
cd src/new_latte
python example_clone_analysis.py
```

## Analysis Output

The analysis provides detailed information in YAML format:

```yaml
repository_analysis:
  cloning_status:
    success: true
    repo_path: "/path/to/cloned/repo"
    
  project_structure:
    root_files: ["README.md", "requirements.txt", "main.py"]
    directories: ["src/", "tests/", "docs/"]
    python_files: ["main.py", "src/app.py"]
    config_files: ["pyproject.toml", "setup.py"]
    main_entry_point: "main.py"
    
  dependencies:
    requirements_files: ["requirements.txt", "requirements-dev.txt"]
    pyproject_toml: "pyproject.toml"
    setup_files: ["setup.py", "setup.cfg"]
    
  testing:
    test_directories: ["tests/", "test/"]
    test_files: ["tests/test_app.py"]
    test_config_files: ["pytest.ini"]
    framework: "pytest"
    
  build:
    build_tools: ["setuptools"]
    build_files: ["pyproject.toml", "setup.py"]
    package_type: "package"
    
  deployment:
    docker_files: ["Dockerfile"]
    wsgi_files: ["src/app.py"]
    static_files: true
    environment_files: [".env.example"]
```

## Features

### Repository Cloning
- Supports GitHub, GitLab, and other Git repositories
- Shallow cloning for faster downloads
- Error handling and cleanup
- Temporary directory management

### Structure Analysis
- Complete directory mapping
- File type detection (Python, config, etc.)
- Main entry point identification
- Configuration file detection

### Dependency Analysis
- Multiple dependency file formats (requirements.txt, pyproject.toml, etc.)
- Package management approach detection
- Development vs production dependencies

### Testing Framework Detection
- Test directory identification
- Test file pattern recognition
- Framework detection (pytest, unittest, etc.)
- Test configuration analysis

### Build Configuration Analysis
- Build tool detection (setuptools, poetry, etc.)
- Package type identification
- Build file analysis

### Deployment Requirements
- Containerization detection (Docker files)
- Web framework detection (WSGI/ASGI)
- Static file handling
- Environment configuration

## Integration with Existing Workflow

The repository cloning and analysis functionality integrates seamlessly with the existing workflow generation system:

1. **Clone and analyze** the target repository
2. **Extract detailed information** about structure, dependencies, and requirements
3. **Generate appropriate workflows** based on the analysis
4. **Create deployment configurations** tailored to the project

## Requirements

- Git must be installed on the system
- Internet connection for repository cloning
- Sufficient disk space for cloned repositories
- Python 3.8+ for the analysis tools

## Error Handling

The system includes comprehensive error handling:
- Network connectivity issues
- Repository access permissions
- Invalid repository URLs
- Disk space limitations
- File system permissions

## Cleanup

The system automatically manages temporary directories, but manual cleanup is also available:

```python
from new_latte.tools.repository_cloner import RepositoryCloner

cloner = RepositoryCloner()
# ... use the cloner ...
cloner.cleanup()  # Clean up temporary directories
```

## Future Enhancements

Potential improvements include:
- Support for private repositories with authentication
- Analysis of commit history and development patterns
- Integration with dependency vulnerability scanning
- Support for non-Git repositories
- Caching of analysis results
- Parallel analysis of multiple repositories 