import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Load environment variables from .env file
load_dotenv()

# Access environment variables (if needed)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
print(f"Your GitHub Token is: {GITHUB_TOKEN}")
AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

# Setup keyless authentication with Azure
credential = DefaultAzureCredential()
print(f"DefaultAzureCredential: {credential}")
# Alternatively, if you want to use the interactive browser method:
# credential = InteractiveBrowserCredential()

# Now you can use `credential` to authenticate your Azure SDK clients


