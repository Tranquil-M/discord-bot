Introducing...

# CatBot Source!

This repository contains the source code to my discord bot, CatBot!

## Table of contents:
| Categories    | What's shown?|
| ------------- |:-------------:|
| [What can it do?](#dowhat) | What can CatBot do? |
| [Installation](#install) | Directions to clone and use this repository! |
| [Used Python Packages](#pkgs) | All python used in this repo! |

<a name="dowhat">

## What can it do?

CatBot has several amazing commands/features, so let's go over all of them right now!

### Passive Features

* **Statuses** \
      &nbsp; &nbsp; &nbsp; CatBot shuffles through a library of statuses, all of which are held in `cogs/bot_statuses.txt`. Adding new statuses is simple, just put some new text on a new line and call it a day! It will shuffle through them every 30 seconds.

* **Syncing** \
    &nbsp;&nbsp;&nbsp; To avoid being rate limited, CatBot contains one context command, `sync`, which can be called using `!sync` on any discord channel. You must be the owner of your application in order for it to function. The sync command syncs together changes to slash commands globally, and those changes are applied after refreshing discord.

* **Auditing** \
    &nbsp;&nbsp;&nbsp; Catbot automatically tracks all slash commands and creates an audit channel if it doesn't exist already. Logs are sent into this channel containing the timestamp the command was ran, and who ran it. This channel is only visible to people with moderation permissions.

* **Error Handling** \
    &nbsp;&nbsp;&nbsp; Any errors CatBot encounters are sent to the user executing the command with an ephemeral, meaning that only the user can see the error and report it when necessary.

* **Member Joining/Leaving** \
    &nbsp;&nbsp;&nbsp; Upon new members joining or leaving the guild/server, CatBot will either welcome the user with a cute little graphic or cry uncontrollably, begging for the person to return to them if they choose to leave.

| Join | Leave |
|------|-------|
| ![member_join](https://github.com/Tranquil-M/CatBot-source/blob/main/Sample/Joining.png?raw=true) | ![member_leave](https://github.com/Tranquil-M/CatBot-source/blob/main/Sample/Leaving.png?raw=true) |

### Testing Commands

* **Pinging** \
    &nbsp;&nbsp;&nbsp; The ping command returns the latency in milliseconds betwen the bot and the script. This is handy if you don't have access to logs and your bot is running slowly.

### Moderation

* **Banning/Unbanning** \
    &nbsp;&nbsp;&nbsp; CatBot possesses the ability to banish users to the shadow realm and back. While the ban command does exist by default on discord, unbanning does not. Like, why? It's really useful! So users can now be easilly banned/unbanned with just their discord username through CatBot.

* **Kicking** \
    &nbsp;&nbsp;&nbsp; For unity, CatBot contains the ability to push people off the plank with just their username.

* **Muting/Unmuting** \
    &nbsp;&nbsp;&nbsp; When someone get's a little too rowdy, you can easily mute and unmute then for any given amount of time. You can also unmute them before their sentence ends just in case. This command utilizes discord's timeout function.

* **History Clearing** \
    &nbsp;&nbsp;&nbsp; If your chat messages is too much of a hassle to delete, then you can easily clear chat history with the clear command!

| Clearing |
|----------|
|![clearing](https://github.com/Tranquil-M/CatBot-source/blob/main/Sample/Clear.png?raw=true)|

### Funny Commands

* **PetPet** \
    &nbsp;&nbsp;&nbsp; Ever wanted to show your ever-burning affection for your friends on discord? No? Well, just in case you want to CatBot really loves to pet people! You can choose to either pet a specific user, or leave it unspecified to pet someone at random.

| PetPet |
|----------|
|![pet](https://github.com/Tranquil-M/CatBot-source/blob/main/Sample/Pet.png?raw=true)|

* **Meow** \
    &nbsp;&nbsp;&nbsp; What's a cat if it doesn't meow? The meow command tells CatBot to let out a cute little meow to ease your day. All sound affects are recorded and edited by my friends.

* **Memes** \
    &nbsp;&nbsp;&nbsp; Everybody needs some humor in their life! The meme command grabs a random, SFW, meme from the first 500 entries on `r/memes`.

| Memes |
|----------|
|![meme](https://github.com/Tranquil-M/CatBot-source/blob/main/Sample/Memes.png?raw=true)|

* **Cats** \
    &nbsp;&nbsp;&nbsp; Do you like-- no, _love_ looking at cat pictures? I mean, that's what the internet is built on! The cats command grabs up to 10 random cats from the [CAAS (Cats as a Service)](https://cataas.com/) API.

| Join | Limit |
|------|-------|
| ![cats_cmd](https://github.com/Tranquil-M/CatBot-source/blob/main/Sample/Cats.png?raw=true) | ![cats_limit](https://github.com/Tranquil-M/CatBot-source/blob/main/Sample/Cats_Limit.png?raw=true) |

* **Slap** \
    &nbsp;&nbsp;&nbsp; Feeling a little mischeivous? Who's stopping you from taking it up a notch? Specify a user and a reason to slap them! 👏👏👏 \
    &nbsp;&nbsp;&nbsp; Leave the user unspecified to randomize who you slap.

| Slap |
|----------|
|![slap](https://github.com/Tranquil-M/CatBot-source/blob/main/Sample/Slap.png?raw=true)|

* **Mimic** \
    &nbsp;&nbsp;&nbsp; Make CatBot say anything with the mimic command! Whatever you say, CatBot will mimic.

<a name="install">

## Installation

Before we can install this script, you must first create a discord application. [This video](https://youtu.be/Oy5HGvrxM4o?si=oyNEblmcLyoa_5J_&t=55) is a great and simple tutorial to get you started! It covers making a basic discord bot in node.js, however this project is written with discord.py, so the programming itself is different here.

1. Clone this repository into your home directory and cd into it
    ```bash
    git clone https://github.com/Tranquil-M/CatBot-source; cd CatBot-source
    ```

2. Create a file to house your token
    1. Create the file
       
       <details>
          <summary>Linux/MacOS</summary>
         
          ```bash
          touch token.env
          ```
          
       </details>

       <details>
          <summary>Windows</summary>
         
          ```powershell
          echo. > token.env
          ```
          
       </details>
       
    3. Use your favorite code editor to add this simple line
         ```
         TOKEN=<Your Token Here>
         ```
3. Install python packages through pip
    ```bash
    python -m pip install -r requirements.txt
    ```

> [!CAUTION]
> When using Arch based distributions of linux, install your pip packages through a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to avoid system-wide python conflicts. While rare, it does happen because Arch uses python for some of it's core scripts. Virtual environments must be initiated to use their installed pip packages.

<a name="pkgs">

## Python Pip Packages

* [discord.py](https://discordpy.readthedocs.io/en/stable/)
* [easy-pil](https://easy-pil.readthedocs.io/en/latest/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [pet-pet-gif](https://github.com/camprevail/pet-pet-gif)
