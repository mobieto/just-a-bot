import discord, io, aiohttp, math

session = aiohttp.ClientSession()

async def nCr(n, r):
    return math.factorial(n)/(math.factorial(r)*math.factorial(n - r))

async def quadratic(a, b, c):
    try:
        d = b**2 - 4*a*c
        x1 = (-b + math.sqrt(d)) / (2*a)
        x2 = (-b - math.sqrt(d)) / (2*a)
        return x1, x2
    except:
        return False

async def get_embed(title, description):
    try:
        embed = discord.Embed(
            title = title,
            description = description,
            colour = 0xE6462E
        )

        return embed
    except:
        return False

async def get_image_file_from_url(url):
    try:
        async with session.get(url) as response:
            stream = io.BytesIO(await response.read())
            return discord.File(stream, filename='image.png')
    except:
        return False

async def get_role_by_name(guild, rolename):
    for role in guild.roles:
        if role.name == rolename:
            return role
    return False

async def is_staff(user):
    return user.guild_permissions.administrator
