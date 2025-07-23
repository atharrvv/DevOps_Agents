from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
# from langchain_openai import AzureChatOpenAI as LLM
from crewai import Agent, Task, Crew, Process, LLM
from typing import List
import os

@CrewBase
class NewLatte():
    """NewLatte crew"""
    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self):
        super().__init__()
        # Configure Azure OpenAI LLM
        # self.llm = LLM(
        #     api_key=os.getenv("AZURE_API_KEY"),
        #     azure_endpoint=os.getenv("AZURE_API_BASE"),
        #     api_version=os.getenv("AZURE_API_VERSION"),
        #     azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME")
        # )

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
            verbose=True,
            llm=self.llm
        )
   
    @agent
    def github_workflow_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['github_workflow_generator'],
            verbose=True,
            llm=self.llm
        )
   
    # @agent
    # def cloud_deployment_specialist(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['cloud_deployment_specialist'],
    #         verbose=True,
    #         llm=self.llm
    #     )
   
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
   
    # @task
    # def create_deployment_configurations(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['create_deployment_configurations'],
    #         output_file='deployment_config.yaml'
    #     )
   
    # @task
    # def create_deployment_documentation(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['create_deployment_documentation'],
    #         output_file='deployment_docs.md'
    #     )
   
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
# from typing import List

# @CrewBase
# class NewLatte():
#     """NewLatte crew"""
#     agents: List[BaseAgent]
#     tasks: List[Task]
    
#     # These agent names MUST match the names in your agents.yaml
#     @agent
#     def repository_analyst(self) -> Agent:
#         return Agent(
#             config=self.agents_config['repository_analyst'],
#             verbose=True
#         )
    
#     # @agent
#     # def github_actions_specialist(self) -> Agent:
#     #     return Agent(
#     #         config=self.agents_config['github_actions_specialist'],
#     #         verbose=True
#     #     )
    
#     # @agent
#     # def cloud_deployment_specialist(self) -> Agent:
#     #     return Agent(
#     #         config=self.agents_config['cloud_deployment_specialist'],
#     #         verbose=True
#     #     )
    
#     # These task names MUST match the names in your tasks.yaml
#     @task
#     def analyze_repository(self) -> Task:
#         return Task(
#             config=self.tasks_config['analyze_repository'],
#         )
    
#     # @task
#     # def generate_github_workflows(self) -> Task:
#     #     return Task(
#     #         config=self.tasks_config['generate_github_workflows'],
#     #         output_file='workflows.yaml'
#     #     )
    
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
