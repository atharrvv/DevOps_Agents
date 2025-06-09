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
    def directory_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['directory_analyzer'],
            verbose=True
        )
    
    @agent
    def workflow_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['workflow_planner'],
            verbose=True
        )
    
    @agent
    def workflow_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['workflow_generator'],
            verbose=True
        )
    
    # These task names MUST match the names in your tasks.yaml
    @task
    def analyze_repository(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_repository'],
        )
    
    @task
    def plan_github_workflow(self) -> Task:
        return Task(
            config=self.tasks_config['plan_github_workflow'],
        )
    
    @task
    def generate_workflow_files(self) -> Task:
        return Task(
            config=self.tasks_config['generate_workflow_files'],
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