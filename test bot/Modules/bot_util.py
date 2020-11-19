import discord, io, aiohttp

session = aiohttp.ClientSession()

async def get_embed(title, description):
    try:
        embed = discord.Embed(
            title = title,
            description = description,
            colour = 0xE6462E
        )

        return embed
    except:
        print('[send_embed] Failed to send embed')

async def get_image_file_from_url(url):
    try:
        async with session.get(url) as response:
            stream = io.BytesIO(await response.read())
            return discord.File(stream, filename='image.png')
    except:
         print('[send_image_from_url] Invalid URL')
         return False

async def get_role_by_name(guild, rolename):
    for role in guild.roles:
        if role.name == rolename:
            return role

async def is_staff(user):
    if user.guild_permissions.administrator:
        return True
