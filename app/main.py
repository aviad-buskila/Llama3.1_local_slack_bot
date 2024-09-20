import subprocess
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
# from langchain.llms import Ollama
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


try:
    print("Pulling the LLaMA 3.1 model...")
    subprocess.run(["ollama", "pull", "llama3.1"], check=True)
    print("LLaMA 3.1 model pulled successfully!")
except subprocess.CalledProcessError as e:
    print(f"Error pulling LLaMA 3.1 model: {e}")
    exit(1)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

llm = Ollama(model="llama3.1:8b")
# llm = Ollama(model="mistral-nemo")
print(llm)
conversations = {}


def get_conversation_chain(channel):
    if channel not in conversations:
        memory = ConversationBufferMemory()
        conversations[channel] = ConversationChain(llm=llm, memory=memory)
    return conversations[channel]


@app.event("app_mention")
def handle_mention(event, say):
    channel = event["channel"]
    user = event["user"]
    text = event["text"].replace(f"<@{event['bot_id']}>", "").strip()

    conversation = get_conversation_chain(channel)
    response = conversation.predict(input=text)

    say(f"<@{user}> {response}")


@app.event("message")
def handle_message(event, say):
    if event.get("channel_type") == "im":
        channel = event["channel"]
        user = event["user"]
        text = event["text"]

        conversation = get_conversation_chain(channel)
        response = conversation.predict(input=text)

        say(response)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
