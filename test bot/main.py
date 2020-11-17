import discord
from discord.ext import commands
import botcmds

TOKEN = 'NzMyNzQ2ODcwMDYwNzQ0ODI2.Xw5Fsw.fgDsyFsW_iwV_Ri2lQJuKAqefWQ'
PREFIX = '-'

client = discord.Client()

@client.event
async def on_ready():
    print('Bot online')

@client.event
async def on_message(msg):
    if msg.content[0] == PREFIX:
        cmd = msg.content[1:len(msg.content)]
        
        if hasattr(botcmds, cmd):
            result = await getattr(botcmds, cmd)(msg)

client.run(TOKEN)


