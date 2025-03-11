# agents/travel_agent.py
import os
from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions import KernelArguments
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from plugins.destinations_plugin import DestinationsPlugin

def create_travel_agent(github_token: str, ai_model_id: str = "gpt-4o-mini", service_id: str = "agent") -> ChatCompletionAgent:
    # Initialize the client and kernel
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=github_token, base_url="https://models.inference.ai.azure.com/")

    kernel = Kernel()
    # Add the destinations plugin
    kernel.add_plugin(DestinationsPlugin(), plugin_name="destinations")

    # Setup chat completion service
    chat_completion_service = OpenAIChatCompletion(
        ai_model_id=ai_model_id,
        async_client=client,
        service_id=service_id
    )
    kernel.add_service(chat_completion_service)

    # Setup agent instructions and settings
    settings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    AGENT_NAME = "TravelAgent"
    AGENT_INSTRUCTIONS = "You are a helpful AI Agent that can help plan vacations for customers at random destinations"

    agent = ChatCompletionAgent(
        service_id=service_id,
        kernel=kernel,
        name=AGENT_NAME,
        instructions=AGENT_INSTRUCTIONS,
        arguments=KernelArguments(settings=settings)
    )
    return agent
