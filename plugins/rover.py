import random as rn
def run(bot):
    @bot.message_handler(commands=['rover'])
    def rover(message):
        bot.send_message(message.chat.id, f"Ваш ровер на сегодня: "
                                          f"{rover_prompts[rn.randint(0, len(rover_prompts)-1)]}")

with open('rover_prompts.txt', 'r', encoding="utf-8") as file:
    rover_prompts = file.readlines()
    rover_prompts = [line.rstrip() for line in rover_prompts]