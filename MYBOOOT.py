import telebot
import os
import importlib
from telebot import types
bot = telebot.TeleBot('7888167162:AAFaur7xiREy3cBebFCmSP0LQ8jmoGQ5zwo')
a = 0

# подключение всех доступных плагинов из папки
for f in os.listdir('plugins'):
    if f.endswith('.py'):
        module = importlib.import_module(f'plugins.{f[:-3]}')
        module.run(bot)

# класс Question осуществляет проверку правильности ответа на вопрос
class Question:
    def __init__(self, prompt: str, answer: str):
        self.prompt = prompt
        self.answer = answer

    def check_answer(self, user_answer: str) -> bool:
        return user_answer.strip().lower() == self.answer.lower()

# класс Quiz осуществляет логику всего квиза
class Quiz:
    def __init__(self, questions: list):
        self.bot = bot
        self.questions = questions
        self.score = 0
        self.result = lambda f: round(f*100/a)
        self.run()

    def run(self):
        @self.bot.message_handler(content_types=['text'])
        def start(message):
            self.sprosil(message)

    def sprosil(self, message):
        global a
        if a < len(self.questions):
            question = self.questions[a]
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(answer_prompts[2*a])
            btn2 = types.KeyboardButton(answer_prompts[2*a+1])
            markup.add(btn1, btn2)
            mesg = bot.send_message(message.chat.id, question.prompt, reply_markup=markup)
            bot.register_next_step_handler(mesg, self.otvetil)

    def otvetil(self, message):
        global a
        user_answer = message.text
        question = self.questions[a]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markupf = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("следующий вопрос")
        btnf = types.KeyboardButton("еще раз!")
        markup.add(btn1)
        markupf.add(btnf)
        if question.check_answer(user_answer):
            self.score += 1
        a = a+1
        if a < len(self.questions):
            bot.send_message(message.chat.id, 'ок👌', reply_markup=markup)
        if a == len(self.questions):
            bot.send_message(message.chat.id, f"Итого {self.result(self.score)}% правильных ответов!")
            self.show(message)
            a = 0
            self.score = 0
            bot.send_message(message.chat.id, "Можешь пройти квиз еще раз или потыкать другие функции",
                             reply_markup=markupf)

    def show(self, message):
        if self.result(self.score) == 100:
            bot.send_message(message.chat.id, "Идеально! В курсе всех новостей💻")
        elif self.result(self.score) >= 50:
            bot.send_message(message.chat.id, "Хорошо знаешь город, красавчик!")
        else:
            bot.send_message(message.chat.id, "Ваш результат: турист. Приезжайте в гости!")

# класс MyBot реализует действия (ответы) бота
class MyBot:
    def __init__(self):
        self.bot = bot
        self.reg()

    def reg(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.main(message)

        @self.bot.message_handler(commands=['quiz'])
        def quiz(message):
            self.minor(message)

    def main(self, message):
        welcome = "Нажми /quiz, чтобы начать квиз."
        self.bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
        self.bot.send_message(message.chat.id, welcome)

    def minor(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("поехали👆")
        markup.add(btn1)
        self.bot.send_message(message.chat.id, "Начнем!", reply_markup=markup)
        Quiz(questions).run()

    def run(self):
        self.bot.polling(none_stop=True)

# распаковка формулировок вопросов-ответов

with open('questions.txt', 'r', encoding="utf-8") as file:
    question_prompts = file.readlines()
    question_prompts = [line.rstrip() for line in question_prompts]
with open('answers.txt', 'r', encoding="utf-8") as file:
    answers = file.readlines()
    answers = [line.rstrip() for line in answers]
with open('answer_prompts.txt', 'r', encoding="utf-8") as file:
    answer_prompts = file.readlines()
    answer_prompts = [line.rstrip() for line in answer_prompts]

questions = [Question(prompt, answer) for prompt, answer in zip(question_prompts, answers)]
MyBot().run()

# бота можно расширять добавлением новых плагинов в папку с новым функционалом
# также можно построчно добавлять в текстовый документ новые вопросы/ответы/варианты для расширения квиза