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
- [Contact](#contact)
- [License](#license)

<br/>

## About
This bot was initially made as a midterm project for Programming Methodology I. What you are seeing in this repository is the extension of that project. However, I still keep improving its feature sets while I learn new aspect of Python and programming.
<br/><br/>

## The name
The word **"Cherng"** in the name of this bot came from a transliteration of **เชิง** /t͡ɕʰɤːŋ/, a word in Thai language which means something close to "finesse" or "artifice" in English. Yes, I want this bot to be clever, cunning, and tact. Also, my friends use this word a lot in our conversation.
(I guess it sounds very wrong, but for Thai people, please ignore it. Something was surely lost in translation.)

## Features *(version 0.0.1)*
For elaborate feature list and future features, see the [Trello](https://trello.com/b/zkk36IIC/bot-features) page
- Custom prefix
- Dynamic help function
- Clear message command in text channel
- [Invite friends with searched games](./cogs/steam.py) (Only works for Steam)
- [Bonk](./cogs/funny.py) command
- Quick reload cogs
- More to comes...  

See [`README.md`](./cogs/) file in cogs folder for more elaborate version.
<br/><br/>

## Requirements
I wrote this bot using Python 3.9.5 on debian 10 system.
The minimum required version of Python is 3.6 (determined using [Vermin](https://github.com/netromdk/vermin))
I also use MongoDB Atlas as a database service of my choice.
#### Required Python modules
The version listed below represents the environment I am working with, I cannot guarantee the compatability for older version of these modules
- [aiohttp](https://docs.aiohttp.org/) - 3.7.4.post0
- [discord.py](https://discordpy.readthedocs.io/) - 1.7.2
- [dnspython](https://www.dnspython.org/) - 2.1.0
- [google-api-python-client](https://github.com/googleapis/google-api-python-client) - 2.6.0
- [motor](https://github.com/mongodb/motor) - 2.4.0

##### For Funny Cog
- [numpy](https://numpy.org/) - 1.20.3
- [Pillow](https://python-pillow.org/) - 8.2.0

##### For Steam Cog
- [steam](https://github.com/ValvePython/steam) - 1.2.0 (Planned to replace due to blocking nature of the library)
<br/><br/>

## Setting up
You have to provide these secrets (credentials) to [`.env`](./.env) file.
1. [Discord bot token](https://discord.com/developers/applications)
2. [Steam Web API key](https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey)
3. [Mongo cluster access key](https://docs.atlas.mongodb.com/connect-to-cluster/#connect-to-a-cluster)
4. [Google API key](https://console.cloud.google.com/apis/credentials?_ga=2.234237150.1566059940.1622774822-1399153718.1622774822)
<br/><br/>

## Contact
Discord: [best4281](https://discordapp.com/users/283765324401344514) (Please DM me first, I don't want to add people randomly)

## LICENSE
I don't know how this thing work, please help.
