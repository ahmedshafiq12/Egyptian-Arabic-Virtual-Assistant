from Recorder.VideoRecorder import *
from Models.ChatBot.ArabicChatBot import ArabicChatBot

if __name__ == "__main__":
    filename = "Default_user"
    file_manager(filename)
    chatbot = ArabicChatBot('./files/hf.env')
    start_AVrecording(filename)
    time.sleep(50)
    stop_AVrecording(filename)

    # video2rec =
    # speech2text =
    # x = speech2text w video2rec

    response = chatbot.respond(x)
    print(response)
