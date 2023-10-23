import pandas as pd
import ast
import random
import discord
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
token = os.environ.get("KEY")

ds = pd.read_csv("./perfect_datasets/perfect_dataset_v2.csv")
ds_overview = pd.read_csv("./perfect_datasets/perfect_dataset_v1_overview.csv")
similarity = pd.read_csv("./perfect_datasets/perfect_datasets_v4.csv")

temp = pd.DataFrame()
temp["title"] = similarity["name"].str.lower().str.split()
temp["title"] = similarity["name"].apply(lambda x: x.replace(":", " :"))

for_sugg = pd.DataFrame()
for_sugg["title"] = similarity["name"].str.lower().str.split()
for_sugg["title"] = similarity["name"].apply(lambda x: x.replace("", ""))

movie_sugg = list()

c = 0

if __name__ == "__main__":

    async def recommend(movie, channel):
        global movie_sugg
        global c
        global movie_sugg

        if movie == "":
            await channel.send("Enter a movie name")
            return

        elif(ds[ds["title"].str.lower() == movie.lower()].empty):
            for i in temp["title"]:
                tmp = i.split(",")
                movi = tmp[0].lower().split()
                if(movie.lower() in movi) and c==0:
                    movie_sugg.append(tmp[0].replace(" :", ":"))
                if(movie.lower() in movi) and c>0:
                    movie_sugg.append(tmp[0].replace(" :", ":"))
            if movie_sugg != []:
                await channel.send("did you mean: ")
                for i in movie_sugg:
                    await channel.send(i)
            else:
                await channel.send("No movie found")
            movie_sugg.clear()
            c += 1
            return

        for_sugg["title"] = for_sugg["title"].apply(lambda x: x.split(","))

        index = ds[(ds["title"].str.lower()) == movie.lower()].index[0]

        moviess = for_sugg["title"][index][1:]

        rndm = [1,2,3,4,5,6]
        #------ generate random numbers for random movies
        '''
        rndm = []
        for i in range(0,5):
            rd = random.randint(1,10)
            rndm.append(rd if rd not in rndm else random.randint(1,10))
        '''

        for i in rndm:
            index2 = ds[(ds["title"].str.lower()) == moviess[i].lower()].index[0]
            await channel.send("TMDB id: " + str(ds.iloc[index2]["movie_id"]))
            await (channel.send("Movie Name: " + str(moviess[i].replace(" :", ":"))))
            # await channel.send(ds_overview.iloc[index2]["overview"])

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        print(message.author.name)
        msg_id = message.content
        print(msg_id[:11])
        if msg_id.startswith("$recommend") and len(msg_id) > 1:
            channel = message.channel
            await recommend(message.content[11:], channel)

    try:
        client.run(token)
    except discord.HTTPException as e:
        print("error")
        if e.status == 429:
            print(
                "The Discord servers denied the connection for making too many requests"
            )
            print(
                "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
            )
        else:
            raise e
