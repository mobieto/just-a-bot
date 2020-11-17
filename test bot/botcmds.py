import os, discord, requests, json

async def test(msg):
    await msg.channel.send('Hello, ' + msg.author.name + '!')
