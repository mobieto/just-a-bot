import os, discord, requests, json, random, aiohttp
from Modules import bot_util

CAT_API = 'https://api.thecatapi.com/v1/images/search'
FACT_API = 'https://uselessfacts.jsph.pl/random.json?language=en'
DAILY_FACT_API = 'https://uselessfacts.jsph.pl/today.json?language=en'
PANDA_API = 'https://some-random-api.ml/img/panda'
HUG_API = 'https://some-random-api.ml/animu/hug'
PAT_API = 'https://some-random-api.ml/animu/pat'

help_message = """
**I'm Swegbot! A general-purpose bot.**

**General Commands:**
 > help - dms you this message
 > ping - sends back a pong

**Fun Commands:**
 > cat - sends a random cat image (Provided by thecatapi.com)
 > panda - sends a random panda image (Provided by some-random-api.ml)
 > fact - sends a random fact (Provided by uselessfacts.jsph.pl)
 > dailyfact - sends a random DAILY fact
 > lovecalculator (name1 name2) - calculates love
 > ppsize - find out your pp size
 > hug ([@]name) - hug a person
 > pat ([@]name) - pat a person

**Moderation Commands:**
 > lock - locks current channel (default role will not be able to message)
 > unlock - unlocks current channel
 > serverlock - locks ALL channels
 > serverunlock - unlocks ALL channels

**My prefix is: -**
"""

session = bot_util.session

#function name == name of command

# GENERAL PURPOSE

async def ping(msg, args):
    await msg.channel.send('Pong!')

async def help(msg, args):
    Embed = await bot_util.get_embed("Hey, "+msg.author.name+"!", help_message)
    await msg.author.send(embed=Embed)
    await msg.add_reaction('👍')

# FUN

async def cat(msg, args):
    async with session.get(CAT_API) as response:
        data = await response.text()
        url = json.loads(data)[0]['url']

        embed = discord.Embed()
        embed.set_image(url=url)
        embed.set_footer(text='Provided by thecatapi.com')
        
        #imageFile = await bot_util.get_image_file_from_url(url)
        await msg.channel.send(embed=embed)

async def panda(msg, args):
    async with session.get(PANDA_API) as response:
        data = await response.text()
        url = json.loads(data)['link']

        embed = discord.Embed()
        embed.set_image(url=url)
        embed.set_footer(text='Provided by some-random-api.ml')

        await msg.channel.send(embed=embed)

async def hug(msg, args):
    if len(args) > 0:
        target = args[0]
        if '@' in args[0] and args[0] != '@':
            async with session.get(HUG_API) as response:
                data = await response.text()
                url = json.loads(data)['link']

                embed = discord.Embed(description=msg.author.mention+' hugs '+args[0]+'!')
                embed.set_image(url=url)
                embed.set_footer(text='Provided by some-random-api.ml')

                await msg.channel.send(embed=embed)
        else:
            await msg.channel.send('Please provide a valid name')

async def pat(msg, args):
    if len(args) > 0:
        target = args[0]
        if '@' in args[0] and args[0] != '@':
            async with session.get(PAT_API) as response:
                data = await response.text()
                url = json.loads(data)['link']

                embed = discord.Embed(description=msg.author.mention+' pats '+args[0]+'!')
                embed.set_image(url=url)
                embed.set_footer(text='Provided by some-random-api.ml')

                await msg.channel.send(embed=embed)
        else:
            await msg.channel.send('Please provide a valid name')

async def fact(msg, args):
    async with session.get(FACT_API) as response:
        data = await response.text()
        fact = json.loads(data)['text']

        await msg.channel.send(fact)

async def dailyfact(msg, args):
    async with session.get(DAILY_FACT_API) as response:
        data = await response.text()
        fact = json.loads(data)['text']

        await msg.channel.send(fact)

async def ppsize(msg, args):
    await msg.channel.send('8'+('='*random.randint(1, 50))+'D')

async def lovecalculator(msg, args):
    if len(args) > 1:
        percentage = random.randint(0, 100)
        content = f'**{args[0]}** and **{args[1]}**: {percentage}%\n'
        
        if percentage == 0:
            content += '*Impossible match*'
        elif 0 < percentage <= 20:
            content += '*Highly unlikely match*'
        elif 20 < percentage <= 50:
            content += '*Unlikely match*'
        elif 50 < percentage <= 80:
            content += '*Possible match*'
        elif 80 < percentage <= 99:
            content += '*Very likely match*'
        elif percentage == 100:
            content += '*Match made in heaven*'
        
        Embed = await bot_util.get_embed('Love Calculator', content)
        await msg.channel.send(embed=Embed)
    
# MODERATION

async def lock(msg, args):
    if await bot_util.is_staff(msg.author):
        channel = msg.channel
        await channel.set_permissions(msg.guild.default_role, send_messages=False)

async def unlock(msg, args):
    if await bot_util.is_staff(msg.author):
        channel = msg.channel
        await channel.set_permissions(msg.guild.default_role, send_messages=True)

async def serverlock(msg, args):
    if await bot_util.is_staff(msg.author):
        for channel in msg.guild.text_channels:
            await channel.set_permissions(msg.guild.default_role, send_messages=False)
                
async def serverunlock(msg, args):
    if await bot_util.is_staff(msg.author):
        for channel in msg.guild.text_channels:
            await channel.set_permissions(msg.guild.default_role, send_messages=True)
