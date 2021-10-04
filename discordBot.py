# bot.py
import os
import functools
import operator
import discord
import requests
import numpy

from discord.channel import CategoryChannel
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix = '!')
#client.load_extension('cog')

@bot.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='releasedate', help='NOT DONE YET. Will show the release date for a specific movie. Usage: !releasedate "movie title" (no quotation marks)') 
async def on_message(ctx, *arg): #arg will be movie name

    nameArray = numpy.asarray(arg)
    title = ''
    for i in range (len(nameArray)):
        if i == 0:
           # print("entered if i==0")
           # print(nameArray[i])
            title = title + nameArray[i]
        
        else:    
          #  print("entered else")
           # print(nameArray[i])
            title = title + ' ' + nameArray[i]
    
    #print(list(arg))
    #title = functools.reduce(operator.add, (arg)) 
    
    print("release date command recieved in active channel")

    #pass title string to API call to search for movie info

    #print(title)
    botResponse = searchMovieAPI(title)
    #'You searched for: ' + title + ". Unfortunately I can't find that information yet. Use !help for more information."
        
       
    await ctx.send(botResponse)
    

def searchMovieAPI(title):
    #this function accepts a string movie title 

    print ("title in search API function = " + title)
    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"

    querystring = {"s":title,"r":"json","page":"1"}

    headers = {
    'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com",
    'x-rapidapi-key': "e7784258e1msh9c5de369e9adc67p1e6182jsn666c246ff8bf"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return(response.text)




bot.run(TOKEN)