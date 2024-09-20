import subprocess
import os
from langchain_community.llms import Ollama
from app.assets.ModelParameters import ModelParameters
from app.services.SlackBot import SlackBot

# Pull the model
try:
    print(f"Pulling the {ModelParameters.model_name} model...")
    subprocess.run(["ollama", "pull", ModelParameters.model_name], check=True)
    print(f"{ModelParameters.model_name} model pulled successfully!")
except subprocess.CalledProcessError as e:
    print(f"Error pulling {ModelParameters.model_name} model: {e}")
    exit(1)

llm = Ollama(
    model=ModelParameters.model_name,
    temperature=ModelParameters.temperature,
    top_k=ModelParameters.top_k,
    top_p=ModelParameters.top_p
)

slack_bot = SlackBot(
    slack_bot_token=os.environ.get("SLACK_BOT_TOKEN"),
    slack_app_token=os.environ.get("SLACK_APP_TOKEN"),
    llm=llm
)

if __name__ == "__main__":
    slack_bot.register_events()
    slack_bot.start(os.environ.get("SLACK_APP_TOKEN"))
