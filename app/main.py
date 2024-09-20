import subprocess
import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from threading import Thread
from app.assets.ModelParameters import ModelParameters


import os


def load_system_context(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()


system_context_path = os.path.join('assets', 'instructions.txt')

system_context = load_system_context(system_context_path)

try:
    print(f"Pulling the {ModelParameters.model_name} model...")
    subprocess.run(["ollama", "pull", ModelParameters.model_name], check=True)
    print(f"{ModelParameters.model_name} model pulled successfully!")
except subprocess.CalledProcessError as e:
    print(f"Error pulling {ModelParameters.model_name} model: {e}")
    exit(1)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

llm = Ollama(model=ModelParameters.model_name, temperature=ModelParameters.temperature, top_k=ModelParameters.top_k,
             top_p=ModelParameters.top_p)
conversations = {}
stop_generating = {}


def get_conversation_chain(channel, system_context):
    if channel not in conversations:
        memory = ConversationBufferMemory()
        chain = ConversationChain(llm=llm, memory=memory)

        chain.predict(input=system_context)

        conversations[channel] = chain
    return conversations[channel]


def send_dynamic_message(client, channel, ts):
    dots = ""
    while not stop_generating.get(channel, False):
        dots = "." * ((len(dots) % 3) + 1)
        client.chat_update(channel=channel, ts=ts, text=f"Generating{dots}")
        time.sleep(1)


@app.event("app_mention")
def handle_mention(event, say, client):
    global stop_generating

    channel = event["channel"]
    user = event["user"]
    text = event["text"].replace(f"<@{event['bot_id']}>", "").strip()

    conversation = get_conversation_chain(channel, system_context)  # Pass the system_context

    generating_message = client.chat_postMessage(channel=channel, text="Generating...")

    stop_generating[channel] = False
    thread = Thread(target=send_dynamic_message, args=(client, channel, generating_message["ts"]))
    thread.start()

    response = conversation.predict(input=text)

    stop_generating[channel] = True

    client.chat_update(
        channel=channel,
        ts=generating_message["ts"],
        text=f"<@{user}> {response}"
    )


@app.event("message")
def handle_message(event, say, client):
    global stop_generating

    if event.get("channel_type") == "im":
        channel = event["channel"]
        user = event["user"]
        text = event["text"]

        conversation = get_conversation_chain(channel, system_context)  # Pass the system_context

        generating_message = client.chat_postMessage(channel=channel, text="Generating...")

        stop_generating[channel] = False
        thread = Thread(target=send_dynamic_message, args=(client, channel, generating_message["ts"]))
        thread.start()

        response = conversation.predict(input=text)

        stop_generating[channel] = True

        client.chat_update(
            channel=channel,
            ts=generating_message["ts"],
            text=response
        )


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
