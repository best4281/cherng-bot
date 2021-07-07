<h1 align="center">CherngBot</h1>
<p align="center">
  <img src="https://cdn.discordapp.com/avatars/729564576559005707/b17810e2e0fd18c6a7c604bfe7e51b3d.png?size=128" />
</p>
<h3 align="center">Experimental Heroku auto depoyment branch</h3>

------------
## Remark
**This branch is basically parallel to main branch, except I am trying to make this branch works with Heroku automatic deploy from GitHub.**

## Major change
- `.env` file was removed. All of the secrets keys are stored in Heroku project Config Vars.

## Setting up
**Do this only if you want to deploy your bot on Heroku service. Otherwise, go back to the [main branch](https://github.com/best4281/cherng-bot).**

1. You have to provide these secrets (credentials) to your Heroku project Config Vars.
    - [DISCORD_TOKEN](https://discord.com/developers/applications) - Your Discord bot token
    - [STEAM_WEB_API_KEY](https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey) - Your steam WebAPI key, if you want to use [steam cog](./cogs/steam.py)
    - [MONGO_CLUSTER](https://docs.atlas.mongodb.com/connect-to-cluster/#connect-to-a-cluster) - Your MongoDB cluster access key
    - [GOOGLE_API_KEY](https://console.cloud.google.com/apis/credentials?_ga=2.234237150.1566059940.1622774822-1399153718.1622774822) - Your Google API key, , if you want to use [steam cog](./cogs/steam.py)
    - [REDDIT_CLIENT_ID](https://www.reddit.com/prefs/apps/) - Your reddit script ID, if you want to use [meme command](./cogs/funny.py)
    - [REDDIT_CLIENT_SECRET](https://www.reddit.com/prefs/apps/) - Your reddit script SECRET, if you want to use [meme command](./cogs/funny.py)
    - [REDDIT_SCRIPT_NAME](https://www.reddit.com/prefs/apps/) - Your reddit script name, if you want to use [meme command](./cogs/funny.py)

2. Configure the name of MongoDB collections inside [`configs.py`](./configs.py) to match your database structure. This is my structure as an example, you should change the code to match your structure, not change your structure to match my stucture.  
Also, you might have to change your database query (Found in [`configs.py`](./configs.py) and [`steam.py`](./cogs/steam.py))
```
Cluster
├─── userData
│    └─── steam
│         ├── { _id:<discord_user_id1> ...
│         ├── { _id:<discord_user_id2> ...
│         │   ...
│   
└─── server
     └─── settings
          ├── { _id:<discord_server_id1> ...
          ├── { _id:<discord_server_id2> ...
          │   ...
```

3. Configure anything that you want, add your own taste, or change color palette.  
Prevent any extentsion (cog) from loading by adding _ in front of the file name (For example: `_funny.py`)

Then, just setup GitHub auto deploy on Heroku, and don't forget to invite your own bot into your own Discord server to use it.


_I highly recommend inviting your bot to the server while it's running. Or else it will force you to create your own `prefixes.json` file (with server id as keys, and prefix as values) inside the root of this directory, since I haven't implement any check yet in this version_


## Invite my bot
If you don't want to fiddle with my messy code files for some setting that might not even exist, my bot is currently running 24/7 on Heroku, you can invite it to your server using [this link](https://discord.com/api/oauth2/authorize?client_id=729564576559005707&permissions=8&scope=bot).

## Contact
Discord: [best4281](https://discordapp.com/users/283765324401344514) (Please DM me first, I don't want to add people randomly)
