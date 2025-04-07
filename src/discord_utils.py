import discord
from morse_utils import morse_to_text, text_to_morse
from collections import defaultdict
from random import randint
import datetime
import os
from db.Attempt import Attempt
from db.User import User, TimeMode
from db.db import conn
from dotenv import load_dotenv


class MorseBotCilent(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()

        self.words = [line for line in open(os.getenv('DATA_PATH')+'clean-words').readlines()]

        self.registered_commands = {
            'help': self.help,
            'morse': self.morse,
            'text': self.text,
            'get': self.get,
            'rank': self.rank,
            'stats': self.stats,
            'sql': self.sql
        }

        self.user_cache: dict[str, tuple[str, datetime.datetime]] = dict()

        self.random_cache = defaultdict(bool)

    def sql(self, _, args):
        cur = conn.cursor()
        try:
            res = cur.execute(' '.join(args)).fetchall()
        except Exception as e:
            cur.close()
            return e
            
        cur.close()
        conn.commit()

        return '\n'.join([str(r) for r in res])


    def help(self, _, args):
        return """
        Razpoložljive komande:
        !help - Prikaz pomoč
        !morse <text> - Pretvori besedilo v Morsejevo abecedo 
        !text <morse> - Pretvori besedo v Morsejevi abecedo v slovensko abecedo 
        !rank [day/mon/overall] - Prikaz rezultatov za [dan/mesec/skupno]
        !stats [day/mon/overall] - Prikaz statistike za [dan/mesec/skupno]
     """

    def morse(self, _, args):
        text = ' '.join(args)
        morse = text_to_morse(text)
        # wrap the morse code in a code block
        return f'```{morse}```'

    def text(self, _, args):
        morse = ' '.join(args)
        return morse_to_text(morse)

    def get(self, msg: discord.Message, args):
        n_words = int(args[0]) if len(args) > 0 and args[0].isdigit() else 1

        idxs = [randint(0, len(self.words) - 1) for _ in range(n_words)]

        string = ' '.join([self.words[idx].strip() for idx in idxs])
        str_for_cache = string.replace(' ', '')

        self.user_cache[(msg.author.id, msg.channel.id)] = (str_for_cache, datetime.datetime.now())

        return string

    def rank(self, _, args):
        mode = TimeMode.ALLTIME

        if len(args) > 0:
            if args[0] == 'day':
                mode = TimeMode.DAILY
            elif args[0] == 'mon':
                mode = TimeMode.MOTHLY
            elif args[0] == 'overall':
                mode = TimeMode.ALLTIME

        rankings_string = User.get_ranking(mode)

        return rankings_string

    def stats(self, msg, args):
        mode = TimeMode.ALLTIME

        if len(args) > 0:
            if args[0] == 'day':
                mode = TimeMode.DAILY
            elif args[0] == 'mon':
                mode = TimeMode.MOTHLY
            elif args[0] == 'overall':
                mode = TimeMode.ALLTIME
            
        user = User.get_by_discord_name(msg.author.name)
        return user.get_stats(mode)
        
    def evaluate_message(self, msg: discord.Message):
        msg.content = msg.content.strip()

        decoded = morse_to_text(msg.content)
        orig_msg, time = self.user_cache[(msg.author.id, msg.channel.id)]

        attempt_time = datetime.datetime.now() - time

        user = User.get_by_discord_name(msg.author.name)
        if not user:
            user = User.create(msg.author.name, msg.author.display_name)

        out_msg = ""
        if decoded == orig_msg:
            out_msg = f'Pravilno. Prejmeš {len(decoded)} točk. Čas: {attempt_time.total_seconds()}s'
            Attempt.create(user.id, datetime.datetime.now(), attempt_time.total_seconds(), len(decoded), True)
        else:
            out_msg = f'Napačno:\n\tPričakovan odgovor:\t{self.user_cache[(msg.author.id, msg.channel.id)][0]}\n\tVaš odgovor:\t\t\t\t\t{decoded}'
            Attempt.create(user.id, datetime.datetime.now(), 0, 0, False)

        return out_msg
        


    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if (message.author.id, message.channel.id) in self.user_cache.keys():
            msg = self.evaluate_message(message)
            self.user_cache.pop((message.author.id, message.channel.id))

            await message.channel.send(msg)
            return

        if message.content[0] != '!':
            return

        command = message.content[1:].split(' ')
        command_name = command[0]

        if command_name not in self.registered_commands.keys():
            await message.channel.send('Command not found')
            return

        response = self.registered_commands[command_name](message, command[1:])

        await message.channel.send(response)
