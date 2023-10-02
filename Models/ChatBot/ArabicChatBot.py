from dotenv import dotenv_values
from hugchat import hugchat
from hugchat.login import Login
from googletrans import Translator


class ArabicChatBot:
    def __init__(self, secrets_path):
        self.secrets = dotenv_values(secrets_path)
        self.email = self.secrets['EMAIL']
        self.passwd = self.secrets['PASS']
        sign = Login(self.email, self.passwd)
        cookies = sign.login()
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        self.chatbot.switch_llm(3)
        self.translator = Translator()
        self.id = self.chatbot.new_conversation()
        self.chatbot.change_conversation(self.id)

    def respond(self, prompt_input):
        response = self.chatbot.chat(prompt_input)
        translated_text = self.translator.translate(response.text, dest='ar')
        return translated_text.text
