from Models.ChatBot.ArabicChatBot import ArabicChatBot

chatbot = ArabicChatBot('./files/hf.env')
print('انا جاهز اسمعك')
while True:
    x = input()
    if x == 'سلام':
        print('سلام')
        break
    response = chatbot.respond(x)
    print(response)