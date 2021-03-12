import discord, datetime
from discord.ext import commands
from Modules import bot_cmds, bot_util

TOKEN = ''
PREFIX = '-'

ALIASES = {
        'ppsize': ['peepeesize'],
        'fact': ['randomfact'],
        'lovecalculator': ['lcalculator', 'lc'],
        'eightball': ['8ball'],
        'binomialexpand': ['bexpand'],
        'amongus': ['amogus', 'sus', 'impostor'],
        'wikipedia': ['wiki']
    }

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "-help"))
    print('Bot online')

@client.event
async def on_member_join(user):
    await user.send('Welcome to '+user.guild.name)
    if user.guild.get_role(778695313677484089):
        await user.add_roles(user.guild.get_role(778695313677484089))

    content = f'**Username:** {user.mention} ({user.id})\n'
    content += f'**Time:** {datetime.datetime.utcnow().strftime("%d %b %Y, %H:%M:%S UTC")}'
    
    log_channel = client.get_channel(778365005056835624)
    Embed = await bot_util.get_embed('User Joined', content)
    await log_channel.send(embed=Embed)

@client.event
async def on_member_remove(user):
    content = f'**Username:** {user.name} ({user.id})\n'
    content += f'**Time:** {datetime.datetime.utcnow().strftime("%d %b %Y, %H:%M:%S UTC")}'
    
    log_channel = client.get_channel(778365005056835624)
    Embed = await bot_util.get_embed('User Left', content)
    await log_channel.send(embed=Embed)

@client.event
async def on_message_delete(msg):
    content = f'**User:** {msg.author.mention} ({msg.author.id})\n'
    content += f'**Channel:** {msg.channel.mention} ({msg.channel.id})\n'
    content += f'**Time:** {datetime.datetime.utcnow().strftime("%d %b %Y, %H:%M:%S UTC")}\n'
    content += f'**Message:** {msg.content}'

    log_channel = client.get_channel(778365005056835624)
    Embed = await bot_util.get_embed('Message Deleted', content)
    await log_channel.send(embed=Embed)

@client.event
async def on_message_edit(old, new):
    if old.content != new.content:
        content = f'**User:** {new.author.mention} ({new.author.id})\n'
        content += f'**Channel:** {new.channel.mention} ({new.channel.id})\n'
        content += f'**Time:** {datetime.datetime.utcnow().strftime("%d %b %Y, %H:%M:%S UTC")}\n'
        content += f'**Old Message:** {old.content}\n'
        content += f'**New Message:** {new.content}'

        log_channel = client.get_channel(778365005056835624)
        Embed = await bot_util.get_embed('Message Edited', content)
        await log_channel.send(embed=Embed)

@client.event
async def on_message(msg):
    if not isinstance(msg.channel, discord.channel.DMChannel):
        # Message sent in public channel
        if msg.content.startswith(PREFIX):
            args = msg.content.split(' ')
            cmd = args[0][1:len(args[0])].lower()
            del args[0]
            
            if hasattr(bot_cmds, cmd):
                await getattr(bot_cmds, cmd)(msg, args, client)
            else:
                # Check if command is an alias
                alias = ''
                for name in ALIASES.keys():
                    if cmd in ALIASES[name]:
                        alias = name
                        break

                if alias != ''  and hasattr(bot_cmds, alias):
                    await getattr(bot_cmds, alias)(msg, args, client)
                else:
                    await msg.add_reaction('❓')
        else:
            if msg.channel == client.get_channel(778616463530786826):
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')

client.run(TOKEN)
