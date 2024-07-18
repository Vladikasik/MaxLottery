import telebot
import config
import json

class Bot():

    def __init__(self, config):

        self.bot = telebot.TeleBot(config.token)
        self.users_age = {}

    def mainloop(self):

        @self.bot.message_handler(commands=['start'])
        def start(msg):

            if msg.text.startswith('/start'):
                age_ask = self.bot.send_message(msg.from_user.id, 'Hi, youre regestiring to the lottery.\nPlease enter your age first')
                self.bot.register_next_step_handler(age_ask, lambda x: self.age_check(x))
        
        self.bot.polling()
    
    def age_check(self, msg):
        if msg.text.isdigit():
            if int(msg.text) < 18:
                self.bot.send_message('You cannot register, you must be 18')
            else:
                self.users_age[msg.from_user.id] = int(msg.text)
                msg = self.bot.send_message(msg.from_user.id, 'Great! Now send money to this adress\n`oX11maxinch`\n\nAfteer sending money reply this bot with tx_id')
                self.bot.register_next_step_handler(msg, lambda x: self.tx_check(x))
        else:
            msg = self.bot.send_message(msg.from_user.id, 'You didnt reply with your age. Please write your age as a digit answer.')
            self.bot.register_next_step_handler(msg, lambda x: self.age_check(x))
            
    def tx_check(self, msg):
        with open('users.json', 'r', encoding='UTF-8') as file:
            data = json.load(file)
        full_name = msg.from_user.first_name + ' ' + msg.from_user.last_name
        print(full_name)
        user_info = {'Name': full_name,
                     'username': msg.from_user.username,
                     'age': self.users_age[msg.from_user.id],
                     'tx_id': msg.text}
        data['users'].append(user_info)
        with open('users.json', 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=4)
    print('data written')
        
if __name__ == '__main__':
    bot = Bot(config)
    bot.mainloop()