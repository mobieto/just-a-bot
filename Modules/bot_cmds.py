import os, discord, json, random, aiohttp
from Modules import bot_util

CAT_API = 'https://api.thecatapi.com/v1/images/search'
DOG_API = 'https://some-random-api.ml/img/dog'
FACT_API = 'https://uselessfacts.jsph.pl/random.json?language=en'
DAILY_FACT_API = 'https://uselessfacts.jsph.pl/today.json?language=en'
PANDA_API = 'https://some-random-api.ml/img/panda'
HUG_API = 'https://some-random-api.ml/animu/hug'
PAT_API = 'https://some-random-api.ml/animu/pat'

eight_ball_replies = [
        'It is unlikely',
        'Definetly',
        'I am unsure',
        'The answer is yes',
        'Never',
        'Ask again later'
    ]

help_message = """
**I'm Swegbot! A general-purpose bot.**

**General Commands:**
 > help - dms you this message
 > ping - sends back a pong

**Fun Commands:**
 > 8ball - answers a yes/no question
 > dog - sends a random dog image (Provided by thecatapi.com)
 > cat - sends a random cat image
 > panda - sends a random panda image
 > fact - sends a random fact (Provided by uselessfacts.jsph.pl)
 > dailyfact - sends a random DAILY fact
 > lovecalculator (name1 name2) - calculates romance compatibility
 > ppsize - find out your pp size
 > hug (@name) - hug a person
 > pat (@name) - pat a person

**Moderation Commands:**
 > mute (@name @name ...) - mute target
 > unmute (@name @name ...) - unmute target
 > lock - locks current channel (default role will not be able to message)
 > unlock - unlocks current channel

**My prefix is: -**
"""

session = bot_util.session

#function name == name of command

# GENERAL PURPOSE

async def ping(msg, args, client=None):
    await msg.channel.send('Pong!')

async def help(msg, args, client):
    Embed = await bot_util.get_embed("Hey, "+msg.author.name+"!", help_message)
    await msg.author.send(embed=Embed)
    await msg.add_reaction('👍')

# FUN

async def eightball(msg, args, client=None):
    await msg.channel.send(random.choice(eight_ball_replies))

async def cat(msg, args, client=None):
    async with session.get(CAT_API) as response:
        data = await response.text()
        url = json.loads(data)[0]['url']

        embed = discord.Embed()
        embed.set_image(url=url)
        embed.set_footer(text='Provided by thecatapi.com')
        
        #imageFile = await bot_util.get_image_file_from_url(url)
        await msg.channel.send(embed=embed)

async def binomialexpand(msg, args, client=None):
    try:
        x, y, n = float(args[0]), float(args[1]), int(args[2])   
        n = n > 256 and 256 or n
        
        terms = []
        terms.append(str(x**n))
        
        for i in range(1, n+1):
            t1 = await bot_util.nCr(n, i)
            t2 = x**(n-i)
            t3 = y**i
            total = t1*t2*t3
            term = str(total)+'x'+(i != 1 and '^'+str(i) or '')
            terms.append(term)

        await msg.channel.send(' + '.join(terms))
    except:
        await msg.add_reaction('👎')
                               
async def kill(msg, args, client=None):
	await msg.channel.send('The mighty ' + msg.author.mention + ' has slain the mongrel ' + args[0] + ' what a filthy way to die!')

async def dog(msg, args, client=None):
    async with session.get(DOG_API) as response:
        data = await response.text()
        url = json.loads(data)['link']

        embed = discord.Embed()
        embed.set_image(url=url)
        embed.set_footer(text='Provided by some-random-api.ml')
        
        #imageFile = await bot_util.get_image_file_from_url(url)
        await msg.channel.send(embed=embed)

async def panda(msg, args, client=None):
    async with session.get(PANDA_API) as response:
        data = await response.text()
        url = json.loads(data)['link']

        embed = discord.Embed()
        embed.set_image(url=url)
        embed.set_footer(text='Provided by some-random-api.ml')

        await msg.channel.send(embed=embed)

async def roll(msg, args, client=None):
    sides = 0

    if len(args) > 0 and args[0].isdigit():
        sides = int(args[0]) < 1 and 1 or int(args[0]) > 100000 and 100000 or int(args[0])
    else:
        sides = 6

    await msg.channel.send('Rolled: '+str(random.randint(1, sides)))

async def hug(msg, args, client=None):
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

async def pat(msg, args, client=None):
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

async def fact(msg, args, client=None):
    async with session.get(FACT_API) as response:
        data = await response.text()
        fact = json.loads(data)['text']

        await msg.channel.send(fact)

async def dailyfact(msg, args, client=None):
    async with session.get(DAILY_FACT_API) as response:
        data = await response.text()
        fact = json.loads(data)['text']

        await msg.channel.send(fact)

async def ppsize(msg, args, client=None):
    await msg.channel.send('8'+('='*random.randint(1, 50))+'D')

async def lovecalculator(msg, args, client=None):
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

async def sexiest(msg, args, client=None):
    await msg.channel.send('<@292419376961814528>')
    
# MODERATION

async def mute(msg, args, client=None):
    if await bot_util.is_staff(msg.author):
        if len(args) > 0:
            targets = args

            for target in targets:
                target = target.strip('<!@>')
                if target.isdigit():
                    member = msg.channel.guild.get_member(int(target))
                    
                    if member:
                        if not await bot_util.get_role_by_name(msg.channel.guild, 'Muted') in member.roles:
                            await member.add_roles(await bot_util.get_role_by_name(msg.channel.guild, 'Muted'))
                    await msg.add_reaction('👍')
    else:
        await msg.add_reaction('👎')

async def unmute(msg, args, client=None):
    if await bot_util.is_staff(msg.author):
        if len(args) > 0:
            targets = args

            for target in targets:
                target = target.strip('<!@>')
                if target.isdigit():
                    member = msg.channel.guild.get_member(int(target))
                    
                    if member:
                        if await bot_util.get_role_by_name(msg.channel.guild, 'Muted') in member.roles:
                            await member.remove_roles(await bot_util.get_role_by_name(msg.channel.guild, 'Muted'))
                await msg.add_reaction('👍')
    else:
        await msg.add_reaction('👎')
                            
async def lock(msg, args, client=None):
    if await bot_util.is_staff(msg.author):
        channel = msg.channel
        await channel.set_permissions(msg.guild.default_role, send_messages=False)
    else:
        await msg.add_reaction('👎')
    

async def unlock(msg, args, client=None):
    if await bot_util.is_staff(msg.author):
        channel = msg.channel
        await channel.set_permissions(msg.guild.default_role, send_messages=True)
    else:
        await msg.add_reaction('👎')
