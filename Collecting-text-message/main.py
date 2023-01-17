import discord
import pandas as pd
from keep_alive import keep_alive
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime
from realText import textAna
import json

#mongodb server for collecting the scaped data
client = MongoClient()
client = MongoClient(
    "mongodb+srv://dbBot:dbBot4343@cluster0.ahhgb.mongodb.net/test")
db = client["disBotDB"]
collection = db["disBotDB"]

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
guild = discord.Guild
bot = commands.Bot(command_prefix='prefix', self_bot=True)

#connect Bot to Discord Server
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == 'TEP team':
            break
    print(f'{client.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')


#bot function1:greeting new member function
@client.event
async def on_member_join(member):
    try:
        await client.send_message(member, newUserMessage)
        print("Sent message to " + member.name)
    except:
        print("Couldn't message " + member.name)
    #
    #await member.dm_channel.send(f'Hello! {member.name}, welcome to our DisBot server! Key ? for instruction')


#bot fuction2: assitance function
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #help function
    elif message.content == '?':
        #this shouldnt be public answer !!!!!!!!!!!!!!!!!!!!!!!!!
        #await message.author.send('"_scan" to inspect the server')

        embed = discord.Embed(title="DisBot HELP",
                              description="Use _ follow with function key",
                              colour=0x7289da)
        embed.add_field(name="-",
                        value="--------------------------",
                        inline=False)
        embed.add_field(name="_serv :", value="server status", inline=False)
        embed.add_field(name="_dash :",
                        value="real-time visualization",
                        inline=False)
        embed.add_field(name="_upd :", value="update database", inline=False)
        embed.add_field(name="_exp :", value="generate cvs file", inline=False)
        embed.add_field(
            name="Links :",
            value=
            "[Dashboard](https://charts.mongodb.com/charts-disbot-fgnht/public/dashboards/60acf749-713d-4858-8c65-3980e916cbfa) | [Database](https://cloud.mongodb.com/v2/60accc02b145744fd0997ff5#host/replicaSet/60accdc59ed11b4a1b954b99)",
            inline=True)
        embed.set_footer(text="DisBot Generator",
                         icon_url=client.user.avatar_url)
        await message.channel.send(embed=embed)
        #await message.channel.send('"_scan" to inspect the server')

    #test database
    # elif "python" in str(message.content.lower()):
    #   post = {"_id": message.id, "score": 1}
    #   collection.insert_one(post)
    #   await message.channel.send('accepted!')

    #set function '_'
    elif message.content.startswith('_'):
        cmd = message.content.split()[0].replace("_", "")
        #server function
        if cmd == 'serv':
            channel = message.channel
            message.author.guild.member_count
            embed = discord.Embed(title="Server information",
                                  colour=0x7289da,
                                  timestamp=datetime.utcnow())
            embed.add_field(name="ID :", value=message.guild.id, inline=True)
            embed.add_field(name="Owner :",
                            value=message.guild.owner,
                            inline=True)
            embed.add_field(
                name="Created at :",
                value=message.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                inline=True)
            embed.add_field(name="Members :",
                            value=len(message.author.guild.members),
                            inline=True)
            embed.add_field(name="Banned members :",
                            value=len(await message.guild.bans()),
                            inline=True)
            embed.add_field(name="Text channels :",
                            value=len(message.guild.text_channels),
                            inline=True)
            embed.add_field(name="Roles :",
                            value=len(message.guild.roles),
                            inline=True)
            await message.channel.send(embed=embed)
            
    #update database function
        if cmd == 'upd':
            channel = message.channel
            myquery = {"_id": message.id}
            if (collection.count_documents(myquery) == 0):
                answer = discord.Embed(title="DisBot updating your database",
                                       description="Updating data....",
                                       timestamp=datetime.utcnow(),
                                       colour=0x7289da)
                await message.channel.send(embed=answer)

                def is_command(message):
                    if len(msg.content) == 0:
                        return False
                    elif msg.content.split()[0] == '_update':
                        return True
                    else:
                        return False

                async for msg in channel.history():
                    if msg.author != client.user:
                        if not is_command(
                                msg):  #should add more parameter such as role
                            data = {
                                'content': msg.content,
                                'time': msg.created_at,
                                'author': msg.author.name,
                                #'role' : msg.member.roles,
                                'channel': msg.channel.name
                            }
                            collection.insert_one(data)
                            #await message.channel.send('updating database!')
                await message.channel.send('database updated!')

    #dashboard function
        if cmd == 'dash':
            answer = discord.Embed(
                title="Real-time Dashboard",
                description=
                "[CLICK HERE....](https://charts.mongodb.com/charts-disbot-fgnht/public/dashboards/60acf749-713d-4858-8c65-3980e916cbfa)",
                timestamp=datetime.utcnow(),
                colour=0x7289da)
            answer.set_author(name="DisBot Data")
            answer.set_footer(text="DisBot Generator",
                              icon_url=client.user.avatar_url)
            answer.set_image
            file = discord.File("dash.JPG", filename="dash.JPG")
            answer.set_image(url="attachment://dash.JPG")
            await message.channel.send(embed=answer, file=file)

    #extract data function
        if cmd == 'exp':
            data = pd.DataFrame(
                columns=['content', 'time', 'author', 'channel'])
            channel = message.channel
            answer = discord.Embed(
                title="DisBot Creating your Message History Dataframe",
                description="Extacting data....",
                colour=0x7289da)
            await message.channel.send(embed=answer)

            def is_command(message):
                if len(msg.content) == 0:
                    return False
                elif msg.content.split()[0] == '_exp':
                    return True
                else:
                    return False

            async for msg in channel.history():
                if msg.author != client.user:
                    if not is_command(
                            msg):  #should add more parameter such as role
                        data = data.append(
                            {
                                'content': msg.content,
                                'time': msg.created_at,
                                'author': msg.author.name,
                                #how to add channel????
                                'channel': msg.channel.id
                            },
                            ignore_index=True)

            file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.csv"  # Determining file name andlocation
            data.to_csv(file_location)  # Saving the file as a .csv via pandas
            answer = discord.Embed(title="Here is your .CSV File",
                                   description=f""" please wait,
                                  `Server` : **{message.guild.name}**
                                  `Channel` : **{channel.name}**""")
            await message.author.send(embed=answer,
                                      file=discord.File(file_location,
                                                        filename='data.csv')
                                      )  # Sending the file
            await message.channel.send('file created!')

# Text analysis function
        if cmd == 'prep':
            #collection.remove({ "content" : "_dash" })
            #collection.remove({ "content" : "_upd" })
            #collection.remove({ "content" : "_serv" })
            #collection.remove({ "content" : "_prep" })
            #collection.remove({ "content" : "_exp" })
            textAna()

keep_alive()
client.run('ODM4Mjk3NTgwNjcxOTkxODA4.YI5Ddg.Gcw40Zak-eMuYz7juQ22LQWd2Ho')
