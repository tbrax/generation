# Work with Python 3.6
import discord
import time
from game import Game
client = discord.Client()
#Token not current
TOKEN = 'token goes here'

Mchannel = None

Mgame = Game()

def getMsg(m,a):
    send = []
    send += Mgame.takeInput(m,a)
    return send


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!me'):
        msg = getMsg(message.content,message.author)
        for x in msg:
            await message.channel.send(x)

client.run(TOKEN)