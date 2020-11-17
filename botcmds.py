import discord
import requests
import json
import os

async def test(msg):
    await msg.channel.send('Hello, ' + msg.author.name + '!')
