from slackbot.bot import Bot
import logging

def main():
    logging.basicConfig()
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('Starting Order Bot')
    main()