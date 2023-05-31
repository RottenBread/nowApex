import requests
import discord
from bs4 import BeautifulSoup
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Lists
rank_champions = []
rank_pickrate = []
rank_map = []

# Get - Champions data
def champions():
    url = 'https://apex.tracker.gg/apex/insights'
    response = requests.get(url)

    if response.status_code == 200:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        ul = soup.findAll(attrs={"class":"insight-bar__label"})
        num = soup.findAll(attrs={"class":"insight-bar__value"})
        for i in range(24):
            rank_champions.append(ul[i].text)
            rank_pickrate.append(num[i].text)
    
    return rank_champions, rank_pickrate

# Get - nowrank map data
def nowMap():
    url = 'https://apexlegendsstatus.com/current-map/battle_royale/ranked'
    response = requests.get(url)

    if response.status_code == 200:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        ul = soup.findAll("h3")
        for i in range(3):
            rank_map.append(ul[i].text)
    
    return rank_map

@bot.command()
async def 에이펙스(ctx, context):
    if context == "챔피언":
        embed = discord.Embed(title="📈 에이펙스 랭크 캐릭터 픽률", color=discord.Color.green())
        rank_championss, rank_pickrates = champions()
        for i in range(24):
            embed.add_field(name="", value=f"{i+1}위 : {rank_championss[i]} ({rank_pickrates[i]})", inline=False)
        embed.set_thumbnail(url="https://i.etsystatic.com/21013861/r/il/aea26a/2035868637/il_570xN.2035868637_la7i.jpg")
        await ctx.send(embed=embed)

    if context == "맵":
        embed = discord.Embed(title="📈 에이펙스 랭크맵", color=discord.Color.green())
        map = nowMap()
        embed.add_field(name="", value=f"현재 : {map[0]}", inline=False)
        embed.set_thumbnail(url="https://i.etsystatic.com/21013861/r/il/aea26a/2035868637/il_570xN.2035868637_la7i.jpg")
        await ctx.send(embed=embed)

bot.run('your-token')
