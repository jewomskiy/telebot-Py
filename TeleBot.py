import telebot
import Functions


class BotStax:

    def __init__(self, token, mylink):
        self.bot = telebot.TeleBot(token)
        self.mylink = mylink
        self.users = {}
        self.keyboard = telebot.types.ReplyKeyboardMarkup()
        self.keyboard.row('Водитель', 'Сотрудник STAX', 'Инвестор')

        Functions.LoadDB(self.users, self.mylink)

        @self.bot.message_handler()
        def func(message):
            self.OnMessage(message)

        Flag = True
        while Flag:
            try:
                self.bot.polling()
                Flag = False
            except Exception as e:
                print(e)

    def OnMessage(self, message):
        try:
            self.users[message.chat.id]['isAuth']
            if message.text[0] == "/":
                self.OnCommand(message)
            else:
                self.bot.send_message(message.chat.id, "Извините, но я вас не поняла! Введите "
                                                       "команду ещё раз, пожалуйста :)")
        except:
            self.Auth(message)

    def OnCommand(self, message):
        # Тут пока ничего просто пусть будет c:
        pass

    def Auth(self, message):
        if message.chat.id in self.users:
            try:
                if self.users[message.chat.id]['typeuser'] == 'user':
                    if 'login' in self.users[message.chat.id]:
                        self.users[message.chat.id]['pass'] = message.text
                        if Functions.UserSignUpCred(self.mylink, self.users[message.chat.id]['login'],
                                                    self.users[message.chat.id]['pass'], message.chat.id):
                            self.users[message.chat.id]['isAuth'] = True
                            self.bot.send_message(message.chat.id, "Вы успешно авторизировались, "
                                                                   "можете начинать пользоваться"
                                                                   " командами!")
                        else:
                            del self.users[message.chat.id]
                            self.bot.send_message(message.chat.id, "К сожалению, мы не смогли вас"
                                                                   " авторизировать. Попробуй ещё"
                                                                   " раз! Если не получится и вновь"
                                                                   ", то обратитесь к нам!")
                    else:
                        self.users[message.chat.id]['login'] = message.text
                        self.bot.send_message(message.chat.id, "Введите пароль, будьте добры!")
                elif self.users[message.chat.id]['typeuser'] == 'driver':
                    phone = Functions.GetNumber(message.text)
                    if Functions.UserSignUpPhone(self.mylink, 'driver', 'work_drivers',
                                                 phone, message.chat.id):
                        self.users[message.chat.id]['isAuth'] = True
                        self.bot.send_message(message.chat.id, "Вы успешно авторизировались, "
                                                               "можете начинать пользоваться"
                                                               " командами!")
                    else:
                        del self.users[message.chat.id]
                        self.bot.send_message(message.chat.id, "К сожалению, мы не смогли вас"
                                                               " авторизировать. Попробуй ещё"
                                                               " раз! Если не получится и вновь"
                                                               ", то обратитесь к нам!")
                elif self.users[message.chat.id]['typeuser'] == 'investor':
                    phone = Functions.GetNumber(message.text)
                    if Functions.UserSignUpPhone(self.mylink, 'business', 'investors',
                                                 phone, message.chat.id):
                        self.users[message.chat.id]['isAuth'] = True
                        self.bot.send_message(message.chat.id, "Вы успешно авторизировались, "
                                                               "можете начинать пользоваться"
                                                               " командами!")
                    else:
                        del self.users[message.chat.id]
                        self.bot.send_message(message.chat.id, "К сожалению, мы не смогли вас"
                                                               " авторизировать. Попробуй ещё"
                                                               " раз! Если не получится и вновь"
                                                               ", то обратитесь к нам!")

            except:
                if message.text == 'Водитель':
                    self.users[message.chat.id]['typeuser'] = 'driver'
                    self.bot.send_message(message.chat.id, "Введите номер телефона, который вы указывали,"
                                                           " когда обращались в STAX, в формате "
                                                           " XXX-YYY-ZZ-WW, будьте добры!",
                                          reply_markup=telebot.types.ReplyKeyboardRemove())
                elif message.text == 'Инвестор':
                    self.users[message.chat.id]['typeuser'] = 'investor'
                    self.bot.send_message(message.chat.id, "Введите номер телефона, который вы указывали,"
                                                           " когда обращались в STAX, в формате "
                                                           " XXX-YYY-ZZ-WW, будьте добры!",
                                          reply_markup=telebot.types.ReplyKeyboardRemove())
                elif message.text == 'Сотрудник STAX':
                    self.users[message.chat.id]['typeuser'] = 'user'
                    self.bot.send_message(message.chat.id, "Введите логин, который вы используете на"
                                                           " stax.mcdir.ru, будьте добры!",
                                          reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            self.bot.send_message(message.chat.id, 'Здравствуйте, я бот Maria. Моя цель - уведомлять вас о '
                                                   'любых событиях. Для начала вам надо пройти авторизацию. '
                                                   'Кем вы являетесь?', reply_markup=self.keyboard)
            self.users[message.chat.id] = {}