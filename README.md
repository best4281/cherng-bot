<h1 align="center">CherngBot</h1>
<p align="center">
  <img src="https://cdn.discordapp.com/avatars/729564576559005707/b17810e2e0fd18c6a7c604bfe7e51b3d.png?size=128" />
</p>

------------
### **Table of Contents**

- [About](#About)
- [The name](#The-name)
- [Features](#features-version-001)
- [Requirements](#Requirements)
  - [Required Python modules](#Required-Python-modules)
    - [For Funny Cog](#For-Funny-Cog)
    - [For Steam Cog](#For-Steam-Cog)
- [Setting up](#Setting-up)
- [Invite my bot](#Invite-my-bot)
- [Contact](#contact)
- [License](#license)


## About
This bot was initially made as a midterm project for Programming Methodology I. What you are seeing in this repository is the extension of that project. However, I still keep improving its feature sets while I learn new aspect of Python and programming.


## The name
The word **"Cherng"** in the name of this bot came from a transliteration of **เชิง** /t͡ɕʰɤːŋ/, a word in Thai language which means something close to "finesse" or "artifice" in English. Yes, I want this bot to be clever, cunning, and tact. Also, my friends use this word a lot in our conversation.
(I guess it sounds very wrong, but for Thai people, please ignore it. Something was surely lost in translation.)


## Features *(version 0.0.2)* ?
For elaborate feature list and future features, see the [Trello](https://trello.com/b/zkk36IIC/bot-features) page
- Custom prefix
- Dynamic help function
- Clear message command in text channel
- [Invite friends with searched games](./cogs/steam.py) (Only works for Steam)
- [Bonk](./cogs/funny.py) command
- [Reddit memes](./cogs/funny.py)
- Quick reload cogs for owner
- More to comes...  


## Requirements
I wrote this bot using Python 3.9.5 on Debian 10 system.
The minimum required version of Python is 3.6
I also use MongoDB Atlas as a database service of my choice.
#### Required Python modules
The version listed below represents the environment I am working with, I cannot guarantee the compatability for older version of these modules.
- [aiohttp](https://docs.aiohttp.org/) - 3.7.4.post0
- [discord.py](https://discordpy.readthedocs.io/) - 1.7.2 (Might get rewrite in the future since discord.py v2.0 is coming)
- [dnspython](https://www.dnspython.org/) - 2.1.0
- [google-api-python-client](https://github.com/googleapis/google-api-python-client) - 2.6.0
- [motor](https://github.com/mongodb/motor) - 2.4.0

##### For Funny Cog
- [numpy](https://numpy.org/) - 1.20.3
- [Pillow](https://python-pillow.org/) - 8.2.0
- [asyncpraw](https://asyncpraw.readthedocs.io/) - 7.3.0

##### For Steam Cog
- [steam](https://github.com/ValvePython/steam) - 1.2.0 (Planned to replace due to blocking nature of the library)


## Setting up
1. You have to provide these secrets (credentials) to [`.env`](./.env) file.
    - [Discord bot token](https://discord.com/developers/applications)
    - [Steam Web API key](https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey)
    - [Mongo cluster access key](https://docs.atlas.mongodb.com/connect-to-cluster/#connect-to-a-cluster)
    - [Google API key](https://console.cloud.google.com/apis/credentials?_ga=2.234237150.1566059940.1622774822-1399153718.1622774822)
    - [reddit related credentials](https://www.reddit.com/prefs/apps/), see more in [`.env`](./.env) file.

2. Install required python modules using [`requirements.txt`](./requirements.txt). For example, if you are using pip in your environment, run
```Shell
pip install -r requirements.txt
```

3. Configure the name of MongoDB collections inside [`configs.py`](./configs.py) to match your database structure. This is my structure as an example, you should change the code to match your structure, not change your structure to match my stucture.  
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

4. Configure anything that you want, add your own taste, or change color palette.  
Prevent any extentsion (cog) from loading by adding _ in front of the file name (For example: `_funny.py`)

Then, just run [`main.py`](./main.py),and don't forget to invite your own bot into your own Discord server to use it.


_I highly recommend inviting your bot to the server while it's running. Or else it will force you to create your own `prefixes.json` file (with server id as keys, and prefix as values) inside the root of this directory, since I haven't implement any check yet in this version_


## Invite my bot
If you don't want to fiddle with my messy code files for some setting that might not even exist, my bot is currently running 24/7 on Google Cloud Platform, you can invite it to your server using [this link](https://discord.com/api/oauth2/authorize?client_id=729564576559005707&permissions=8&scope=bot).

## Contact
Discord: [best4281](https://discordapp.com/users/283765324401344514) (Please DM me first, I don't want to add people randomly)
