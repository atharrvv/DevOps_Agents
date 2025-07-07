from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class NewLatte():
    """NewLatte crew"""
    agents: List[BaseAgent]
    tasks: List[Task]
    
    # These agent names MUST match the names in your agents.yaml
    @agent
    def repository_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['repository_analyzer'],
            verbose=True
        )
    
    @agent
    def workflow_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['workflow_creator'],
            verbose=True
        )
    
     
    # These task names MUST match the names in your tasks.yaml
    @task
    def analyze_and_generate_files(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_and_generate_files'],
        )
    
    @task
    def generate_optimized_workflows(self) -> Task:
        return Task(
            config=self.tasks_config['generate_optimized_workflows'],
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
