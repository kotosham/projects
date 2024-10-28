def run(bot):
    @bot.message_handler(commands=['news'])
    def news(message):
        bot.send_message(message.chat.id, 'Все новости Иннополиса '+'[здесь](https://t.me/innopolisnews_rus)', parse_mode='Markdown')
