import discord, io, aiohttp, math
from PIL import Image, ImageDraw

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

async def encode(string):
    if not string or string == '': return ''
    encoded = ''
    prevchar = ''
    i = 1

    for char in string:
        if char != prevchar:
            if prevchar: encoded += str(i) + prevchar
            i = 1
            prevchar = char
        else:
            i += 1
    encoded += str(i) + prevchar
    
    return encoded

async def decode(string):
    decoded = ''
    i = ''

    for char in string:
        if char.isdigit():
            i += char
        else:
            decoded += char * int(i)
            i = ''

    return decoded

async def get_bytes_from_url(url):
    try:
        async with session.get(url) as response:
            stream = io.BytesIO(await response.read())
            return stream
    except Exception as e:
        return e

async def get_filtered_file(imgbytes, filter):
    im = Image.open(imgbytes)
    filtered = im.filter(filter)
    with io.BytesIO() as imgbinary:
        filtered.save(imgbinary, 'PNG')
        imgbinary.seek(0)
        return discord.File(imgbinary, filename='image.png')

async def greyscale_image(imgbytes):
    img = Image.open(imgbytes)
    r = img.convert('L')
    with io.BytesIO() as imgbinary:
        r.save(imgbinary, 'PNG')
        imgbinary.seek(0)
        return discord.File(imgbinary, filename='image.png')

async def blend_images(imgbytes1, imgbytes2):
    return

async def get_role_by_name(guild, rolename):
    for role in guild.roles:
        if role.name == rolename:
            return role
    return False

async def is_staff(user):
    return user.guild_permissions.administrator
