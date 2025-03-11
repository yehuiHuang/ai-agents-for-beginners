# main.py
import asyncio
from IPython.display import display, HTML
from agents.travel_agent import create_travel_agent
from config import GITHUB_TOKEN  # assuming you defined it in config.py

from semantic_kernel.contents import ChatHistory
from semantic_kernel.contents.function_call_content import FunctionCallContent
from semantic_kernel.contents.function_result_content import FunctionResultContent
from semantic_kernel.functions import KernelArguments, kernel_function

async def main():
    # Initialize and run your agent
    agent = create_travel_agent(github_token=GITHUB_TOKEN)
    # Add your chat logic or other workflows here
    # Define the chat history and user inputs
    # Define the chat history
    chat_history = ChatHistory()

    # Respond to user input
    user_inputs = [
        "Plan me a day trip.",
        "I don't like that destination. Plan me another vacation.",
    ]

    for user_input in user_inputs:
        # Add the user input to the chat history
        chat_history.add_user_message(user_input)

        # Start building HTML output
        html_output = f"<div style='margin-bottom:10px'>"
        html_output += f"<div style='font-weight:bold'>User:</div>"
        html_output += f"<div style='margin-left:20px'>{user_input}</div>"
        html_output += f"</div>"

        agent_name: str | None = None
        full_response = ""
        function_calls = []
        function_results = {}

        # Collect the agent's response with function call tracking
        async for content in agent.invoke_stream(chat_history):
            if not agent_name and hasattr(content, 'name'):
                agent_name = content.name

            # Track function calls and results
            for item in content.items:
                if isinstance(item, FunctionCallContent):
                    call_info = f"Calling: {item.function_name}({item.arguments})"
                    function_calls.append(call_info)
                elif isinstance(item, FunctionResultContent):
                    result_info = f"Result: {item.result}"
                    function_calls.append(result_info)
                    # Store function results
                    function_results[item.function_name] = item.result

            # Add content to response if it's not a function-related message
            if (hasattr(content, 'content') and content.content and content.content.strip() and
                not any(isinstance(item, (FunctionCallContent, FunctionResultContent))
                        for item in content.items)):
                full_response += content.content

        # Add function calls to HTML if any occurred
        if function_calls:
            html_output += f"<div style='margin-bottom:10px'>"
            html_output += f"<details>"
            html_output += f"<summary style='cursor:pointer; font-weight:bold; color:#0066cc;'>Function Calls (click to expand)</summary>"
            html_output += f"<div style='margin:10px; padding:10px; background-color:#f8f8f8; border:1px solid #ddd; border-radius:4px; white-space:pre-wrap;'>"
            html_output += "<br>".join(function_calls)
            html_output += f"</div></details></div>"

        # Add agent response to HTML
        html_output += f"<div style='margin-bottom:20px'>"
        html_output += f"<div style='font-weight:bold'>{agent_name or 'Assistant'}:</div>"
        html_output += f"<div style='margin-left:20px; white-space:pre-wrap'>{full_response}</div>"
        html_output += f"</div>"
        html_output += "<hr>"

        # Display formatted HTML Jupyter notebook
        # display(HTML(html_output))

        # Display formatted HTML python script
        # We're in a standard Python environment
        # Option 1: Save to a file
        with open("output.html", "a") as f:
            f.write(html_output)
        print(f"HTML output appended to output.html")
            

if __name__ == "__main__":
    asyncio.run(main())
