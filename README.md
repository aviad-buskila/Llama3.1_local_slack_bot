# Slack LLaMA Bot

A Slack bot that utilizes the LLaMA model to provide insightful responses to user inquiries. This application is built using Python, Slack Bolt, and LangChain, allowing for interactive conversations in Slack channels and direct messages. Ever hit that annoying usage limit on ChatGPT or ClaudeAI? (We've all been there 🤭)
Say hello to a game-changer: A Slack bot powered by Meta's Llama3.1, *running right on your local machine, free of charge!* It responds to mentions and handles DMs directly in your Slack workspace, and can be ran on a common macbook pro.
While this repo includes Llama3.1, you can use any Ollama-supported LLM (like mistral-nemo, etc.).


## Features

- Responds to mentions in Slack channels and direct messages.
- Displays a dynamic "generating" message while processing requests.
- Customizable LLaMA model parameters (temperature, top-k, top-p).
- System context loaded from a text file for tailored responses.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7 or higher
- [Ollama](https://ollama.com/) CLI
- Slack API token and App token

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/slack-llama-bot.git
   cd slack-llama-bot
   ```

2. Install the required Python packages:

  ```bash
  pip install -r requirements.txt
```


3. Pull the LLaMA model using Ollama:

  ```ollama pull llama3.1
  ```

4. Set your Slack API tokens as environment variables:

  ```export SLACK_BOT_TOKEN='your-slack-bot-token'
  export SLACK_APP_TOKEN='your-slack-app-token'
```

5. Create a text file named system_context.txt in the assets directory with your desired system context.

## Usage
To run the bot, execute the following command:

  ```bash
  python main.py
```

Once the bot is running, you can mention it in any Slack channel or send it a direct message. The bot will respond based on the configured system context and model parameters.

## Customization

## Model Parameters
You can customize the model parameters in the `app/assets/ModelParameters.py` file:

```class ModelParameters:
    model_name = "llama3.1"
    temperature = 0.7  
    top_k = 50         
    top_p = 0.9        
```

## System Context
The system context that guides the model's behavior can be modified in the assets/system_context.txt file. Update the contents to suit your desired interaction style.


## Acknowledgements
Slack Bolt for building Slack apps.
LangChain for integrating with LLaMA and handling conversations.
Ollama for providing the LLaMA model.

