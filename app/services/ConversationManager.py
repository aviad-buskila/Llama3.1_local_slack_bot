import time
from threading import Thread
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


class ConversationManager:
    def __init__(self, llm):
        self.llm = llm
        self.conversations = {}
        self.stop_generating = {}

    def get_conversation_chain(self, channel):
        if channel not in self.conversations:
            memory = ConversationBufferMemory()
            self.conversations[channel] = ConversationChain(llm=self.llm, memory=memory)
        return self.conversations[channel]

    def send_dynamic_message(self, client, channel, ts):
        dots = ""
        while not self.stop_generating.get(channel, False):
            dots = "." * ((len(dots) % 3) + 1)
            client.chat_update(channel=channel, ts=ts, text=f"Generating{dots}")
            time.sleep(1)

    def start_dynamic_message_thread(self, client, channel, generating_message_ts):
        self.stop_generating[channel] = False
        thread = Thread(target=self.send_dynamic_message, args=(client, channel, generating_message_ts))
        thread.start()

    def stop_dynamic_message_thread(self, channel):
        self.stop_generating[channel] = True
