#from distutils.errors import LinkError
#from types import NoneType
import discord

from discord.utils import get
import asyncio

import datetime as dt

import time
import csv
from collections import defaultdict
import random

from discord.ext import tasks

import numpy as np


# Bot will not join server if DEBUG_MODE = True
DEBUG_MODE = False

# List of applicable roles
ROLES = {
    'Member': 698388933511217155,
    'New User': 831644590779793458,
}
ED_WITTEN = ':ed:761332313829146624'
ZHAN_SU = ':highschoolmath:1019342347814850680'
SCREM_ID = ':screm:761332313829146624'

FLEX_CHANNEL = 777557757665476638 # flex jar channel id
LOG_CHANNEL = 753072439814258688 # channel-refresh-logs channel id
VERIFICATION_CHANNEL = 708563333728436244

timeOffset = 5 #Savings time is 5, regular time is 4

currentDay = time.strftime("%D %H:%M", time.localtime(time.time()-timeOffset*60*60)).split(' ')

REFRESH_CHANNELS = [753070698607542342] #, 771187187635060736]
REFRESH_DELAY = 30 # minutes before message deletion

# Executive positions
EXEC_POSITIONS = {
    'President': (
        'Ivan Ovchinnikov',
        'i.ovchinnikov',
        'TBA',
    ),
    'Treasurer': (
        'Ruyi Xu',
        'ruyi.xu',
        'TBA',
    ),
    'VP Asset Management': (
        'Yumeng Lu',
        'yumeng.lu',
        'TBA',
    ),

    'VP Internal and External Affairs': (
        'Halle Nunes',
        'halle.nunes',
        'TBA',
    ),
    
    
    'VP Communications': (
        'Shivangi Aneja',
        'shivangi.aneja',
        'TBA',
    ),
    'VP Academic Affairs': (
        'Marty Hewitt',
        'marty.hewitt',
        'TBA',
    ),
    
    'VP Social Events': (
        'Edgar Ma',
        'edgar.ma',
        'TBA',
    ),

    'VP Secretary': (
        'Annalisa Texeira',
        'annalisa.teixeira',
        'TBA',
    ),

    'VP First-Year Representative (PHY131/2)': (
        'TBA',
        'TBA',
        'TBA',
    ),

    'VP First-Year Representative (PHY151/2)': (
        'TBA',
        'TBA',
        'TBA',
    ),

}

# Bot command utils
HELP_TEXT = f'''**PhySU Help**
`!website` to access the the PhySU website
`!exec` to see the list of PhySU executives
`!leaderboard` to view the flex jar (only available in <#{FLEX_CHANNEL}>)
`!edwitten` for a brief bio of Ed Witten
`!screm` for stress relief
`!fortune [question]` for making important decisions
'''

refresh_channel_text = ', '.join(f'<#{channel}>' for channel in REFRESH_CHANNELS)
MOD_HELP = f'''**For Mods**
`!purgechannel` to purge {refresh_channel_text} (can be used from anywhere)
`!sendmessage` to send a pre-written message as Ed Witten (contact Sam Li for help)
Paste any verification key into <#{VERIFICATION_CHANNEL}> to check who it's for and whether it's expired
'''
EMBED_COLOR = 0x8f279b

print('Initializing...')


##### Utility Functions #####
def get_timestamp(): 
    return time.strftime("%D %H:%M", time.localtime(time.time()))

def decode(raw_name):
    asciiname = ''.join(str(9-int(i)) for i in raw_name)
        
    asciilist = []
    temp = ''
    for e in asciiname:
        temp = temp + e
        if len(temp) == 3 and temp[0] == '1':
            asciilist.append(int(temp))
            temp = ''
        elif len(temp) == 2 and temp[0] != '1':
            asciilist.append(int(temp))
            temp = ''
    
    name = ''.join(map(chr, asciilist))
    return name

# make list of join tokens
def getjoinlogs():
    tokens = set()
    #cc=0
    with open('joinlog.csv', 'r') as f:
        next(f)
        
        
        reader = csv.reader(f)
        try:
            for _, token1, token2, *_ in reader:
                #cc=cc+1
                #print(cc)
                #if cc==257:
                #   print(token1)
                
                tokens.add((int(token1), int(token2)))
        except:
            print('Entry got ignored')
    
    return tokens

"""Returns a dictionary of pronouns for a given user.
    Args:
        user (discord.Member): The user to get pronouns for.
    Returns:
        dict: A dictionary of pronouns.
    """

def get_pronouns(user):
    roles = [role.name for role in user.roles]
    if 'he/him' in roles:
        return {
            'they': 'he',
            'them': 'him',
            'their': 'his',
            'are': 'is',
            'have': 'has',
            'were': 'was',
        }
    if 'she/her' in roles:
        return {
            'they': 'she',
            'them': 'her',
            'their': 'her',
            'are': 'is',
            'have': 'has',
            'were': 'was',
        }
    if 'ze/zir' in roles:
        return {
            'they': 'ze',
            'them': 'zir',
            'their': 'zer',
            'are': 'is',
            'have': 'has',
            'were': 'was',
        }
    if 'xe/xir' in roles:
        return {
            'they': 'xe',
            'them': 'xir',
            'their': 'xyr',
            'are': 'is',
            'have': 'has',
            'were': 'was',
        }
    if 'it/its' in roles:
        return {
            'they': 'it',
            'them': 'it',
            'their': 'its',
            'are': 'is',
            'have': 'has',
            'were': 'was',
        }
    return {
        'they': 'they',
        'them': 'them',
        'their': 'their',
        'are': 'are',
        'have': 'have',
        'were': 'were',
    }


#-----------------------------------------------------------------------------
# bot token, DO NOT GIVE THIS TO ANYONE
# NzUyMDAwNDM1ODIwMTY3MjA4.X1RQ-w.7M3uQcb0HLk-nP4GToVklxYqqj8
intents = discord.Intents.all()
#intents.reactions = True
#intents.members = True
client = discord.Client(intents=intents)


#Called when the bot is ready to start processing events."""
@client.event
async def on_ready(): 
    timestamp = time.time()

    timedmessages.start()
    archiveColloquia.start()
    #hourlyQuote.start()

    print(f'Logged in as {client.user}')
    
    # set bot status, e.g. "Watching ACORN Waitlists"
    await client.change_presence(activity = discord.Activity(name="ACORN Waitlists | !physu",
                                                             type=discord.ActivityType.watching))
    # log when bot signed in
    with open("botuplog.txt", "a") as f:
        print(f'logged into server at {get_timestamp()}', file=f)


#Purges all messages in the channels listed in REFRESH_CHANNELS. Alternatively purge a specified number of messages from a specified channel."""
async def purge_refresh_channels(mnum=200, refreshids=REFRESH_CHANNELS):
    for refreshchannel_id in refreshids:
        refreshchannel = client.get_channel(refreshchannel_id)
        #demmessages = refreshchannel.history(limit=200)
        messages =  [thing async for thing in refreshchannel.history(limit=mnum)] # Gets the last mnum messages in the channel

       # await refreshchannel.history(limit=mnum).flatten()


        messages = list(filter(lambda message: not message.pinned, messages)) # Compiles a list of messages that are not pinned

         # Logs the given message to #channel-refresh-logs."""
        print(f'Purging {len(messages)} messages from channel {refreshchannel.name}')

        for message in messages:
            try:
                await log_message(message)
                await message.delete()
            except Exception as ex:
                print(ex)


async def log_message(message):
    #Logs the given message to #channel-refresh-logs."""
    logchannel = client.get_channel(LOG_CHANNEL)  # Gets the channel object
    sanitized = message.content.replace('\n', ' / ') # Replaces newlines with spaces
    await logchannel.send(f' > {sanitized}\n{message.channel.name} {message.author} {get_timestamp()}') # Sends the message to the log channel


occupancy = 0
last_checkin = time.monotonic()

# verification
# to test use this key: $696900123412898889883028884242004567, sets nickname to "Wentao"
# corresponding Google Sheets link: https://tinyurl.com/yykyc9ar
@client.event
async def on_message(message):
    """Called whenever a message is sent in a channel the bot can see.
    Args:
        message (discord.Message): The message that was sent.
    """


    global occupancy, last_checkin

    timestamp = time.time()
    is_self = (message.author == client.user)
#    if is_self: return

    try:
        roles = [role.name for role in message.author.roles]
        is_mod = ('Moderator' in roles)
    except:
        is_mod = False

    try:
        book_shelf = ('Bookshelf Committee' in roles)
    except:
        book_shelf = False
    try:
        colloquium_committee = ('Colloquia Committee' in roles)
    except:
        colloquium_committee =False

    if message.channel.id == VERIFICATION_CHANNEL and not is_self: # if message is in verification channel
        is_numeric = all(char in '0123456789' for char in message.content.strip()) 
        if is_numeric:
            await message.channel.send(f'<@{message.author.id}> Please include the `$` at the start of the verification key.') # if message is a number, remind the user that they need to include the $
            await message.delete(delay=5)

    if message.content.startswith('$') and message.channel.id == VERIFICATION_CHANNEL:
        action = 'tested' if is_mod else 'used'
        print(f'{message.author.name} {action} verification code {message.content}')

        try:
            # parse imput
            raw = message.content[1:]
            token1, token2, raw_name = int(raw[0:10]), int(raw[-10:]), str(raw[10:-10])
            print("before join log")
            used_tokens = getjoinlogs()
            print('afterjoin log')

            is_used = (token1, token2) in used_tokens
            is_valid = ((token1 - 1234) % 6969 == 0) and ((token2 - 4567) % 4242 == 0) # TODO: explore the possibility of using a more secure and unique key for verification
            nickname = decode(raw_name) # NOTE: nickname doesn't have to be loaded here, can wait until after verification

            if not is_valid: # if key is invalid, send error message and return
                await message.channel.send('Invalid key, please try again.')
                return

            if is_mod: # if user is a moderator, send verification status and return
                status = 'Expired' if is_used else 'Active'
                await message.channel.send(f'{status} verification key for {nickname}')
                return

            if is_used: # if key is already used, ban the user sending that key, send error message and return
                print(f'banned {message.author.name} for duplicate key')
                await message.channel.send("This is a duplicate key. You have been banned")
                time.sleep(5)
                await message.author.ban(reason="You have used a duplicate key.")
                return

            # get user nickname and discord name
            discord_name = message.author.name
            
            # change nickname and give "Member" role
            # await message.channel.send('ree') # testing purposes only
            await message.author.edit(nick=nickname)
            await message.author.add_roles(get(message.guild.roles, id=ROLES['Member']))
            await message.author.remove_roles(get(message.guild.roles, id=ROLES['New User']))
            
            # write to file relevant information
            print(f'{message.author.name} joined successfully')
            with open('joinlog.csv', 'a') as f:
                print(
                    f'{discord_name}, {token1}, {token2}, {nickname}, {timestamp:.3f}',
                    file=f
                )

        except Exception as ex:
            await message.channel.send('Verification bot broken. Please report this issue to a moderator.')
            print(ex)

        finally:
            # delete message
            await message.delete(delay=1)
    
    if message.content.startswith('!amogus'):
        amoguslist= ['https://tenor.com/view/boiled-soundcloud-boiled-boiled-irl-boiled-utsc-boiled-cheesestick-agem-soundcloud-gif-20049996', 'https://tenor.com/view/among-us-sus-yhk-among-twerk-among-us-twerk-gif-23335803','https://media.discordapp.net/attachments/750874999543300146/1004201641551089776/image0-1.gif','https://tenor.com/view/among-us-amogus-ass-dance-happy-gif-20485385','https://media.discordapp.net/attachments/556756134367592481/861657418155819045/speed-3.gif']
        await message.channel.send(amoguslist[random.randint(0,len(amoguslist)-1)])
        await message.delete()



    if message.content.startswith("!user"): # !user command looks for the user with the given code
        num = message.content.split('[')[1]
        try:
            pfromuser = await message.guild.fetch_member(int(num))
            await message.reply("The person with this code is:" + pfromuser.display_name)
        except:
            await message.reply("something went horribly wrong")

    # flex jar
    if message.content == '!leaderboard' and (message.channel.id == FLEX_CHANNEL or message.channel.id == 959108984332234842): 
        flex_jar = get_flex_jar('flexjar.csv')

        leadembed = await leaderboardgen(flex_jar, message,jarheader='Flex Jar Leaderboard')


        await message.reply(embed=leadembed)
    
    if message.content == '!legacyleaderboard' and (message.channel.id == FLEX_CHANNEL or message.channel.id == 959108984332234842): 
        flex_jar = get_flex_jar('legacyflexjar.csv')
        leadembed = await leaderboardgen(flex_jar, message,jarheader='Legacy Flex Jar Leaderboard')

        await message.reply(embed = leadembed)

    if message.content == '!website':  # !website command displays links to PhySU website and social media, as well as student resources
        await message.channel.send('''**PhySU Website:** https://www.physu.org
**PhySU Facebook Page:** https://www.facebook.com/PHYSUPhysics
**PhySU Facebook Group:** https://www.facebook.com/groups/pasu.physics/
**Online Resource Masterlist for Students:** https://docs.google.com/document/d/1TH_ldQUeX0yfJe9pTczIIqo2J6GzcxBr1SQ3z4ddlVA/edit?usp=sharing''')

    if message.content == '!exec': # Shows the PhySU executive team
        embed = discord.Embed(
            title='PhySU Executive Officers',
            color=EMBED_COLOR
        )
        for position, info in EXEC_POSITIONS.items():
            name, email, office_hour = info
            embed.add_field(
                name=position,
                value=f'{name} <{email}@mail.utoronto.ca>\n*Office Hour: {office_hour}*',
                inline=False,
            )
        embed.set_footer(text='Feel free to message any exec with questions or concerns!')
        await message.channel.send(embed=embed)


    # Ed Witten help command

    if message.content.startswith('!courseSetupInstructions'):
        await message.reply('See instructions for how to set up course channels here: https://www.overleaf.com/read/xxywzkjngbbz#7b2abe' ) 

    if message.content.startswith('!edhelp') or message.content.startswith('!help'):


        helpText = get_dict('helpText.txt')


        checker = False

        splitHelp = message.content.split('_')

        

        msg = 'For more specific instructions on available commands, please type `!edhelp_ ` following the extensions below (E.G. `!edhelp_general` ): \n \n' +  '`general`   Gives a brief overview of basic PhySU server commands'

        allmsg =[]
        execmsg=[]

        

        for i in range(len(helpText['h'])): # 'modq' is True if the command is only for mods. This sorts the lines into two lists, one for all users and one for mods

            if helpText['modq'][i] == 'False':
                allmsg.append(i)
            if helpText['modq'][i] == 'True':
                execmsg.append(i)
        mod_msg  = '\n Exec only commands: '

        

        for i in allmsg:# This loop adds the commands to the message
            rep = helpText['desc'][i].replace('\\n', '\n')
            msg+= '\n' + '\n' + '`' + helpText['h'][i] + '`' + "    " + rep
        for i in execmsg:
            rep = helpText['desc'][i].replace('\\n', '\n')
            mod_msg +='\n' + '\n' + '`' + helpText['h'][i] + '`' + "    " + rep

    

        if len(splitHelp)==1: # if there are no underscores in the message, it sends the general help message
            if is_mod:
                msg += '\n \n' + mod_msg
            await message.channel.send(msg)
            checker = True
        msg =''
        
        if len(splitHelp)==2: # if there is one underscore, it sends the help message for that command
            identifier  = splitHelp[1] 
            
            for i in range(len(helpText['h'])): 
                row = [helpText['h'][i], helpText['modq'][i],helpText['htext'][i].replace('\\n', '\n'),helpText['ismod'][i].replace('\\n', '\n'), helpText['desc'][i].replace('\\n', '\n') ]
               
                if row[0] == identifier:
                    if row[1] == str(is_mod) or row[1] == 'False':
                        msg= row[2]
                        if is_mod:
                            msg += '\n' + '\n' + row[3]
                        checker = True
                        await message.channel.send(msg)
            
            if identifier == 'general':               
                msg = HELP_TEXT
                if is_mod:
                    msg += '\n' + '\n' + MOD_HELP
                await message.channel.send(msg)
                checker = True

        if checker == False:
            await message.reply("Your help query was not found. Please double check your spelling, by comparing it to ")
            
                
        

   # Ed does the thing when people say 'so true bestie'
    if 'so true bestie' in message.content.lower() and not is_self:
        bcount = 0
        try:
            bcount  = getbestie()
        except:
            savebestie(0)
            bcount = getbestie()
            await message.reply("There was no so true bestie counter pre-saved. I made a new one and re-started the counter from 0. ")

        bcount = bcount + 1

        savebestie(bcount)


        await message.author.add_roles(get(message.guild.roles, id=1029445036863144007) )


 # !bestie command displays the current so true bestie count
    if message.content.startswith('!bestie'):
        number = getbestie()
        print(number)
        await message.reply("So true bestie count: " +  str(number))

    # Ed reacts to the mention of Ivr*i's name
    if 'ivrii' in message.content.lower() and not is_self:
        await message.add_reaction(ED_WITTEN)
        await message.channel.send('Thou shalt not mention Ivr*i’s name')

    if 'duck' in message.content.lower() and not is_self:
        await message.add_reaction(ED_WITTEN)
        await message.channel.send('There are no ducks in MP')

    # Ed reacts to the mention of Zhan Su's name
    if 'zhan su' in message.content.lower() and False:
        sumes = ['Its highschools physics!', 'Its just calculus!', 'Elementary school math!','Theta dot.']
        await message.add_reaction(ED_WITTEN)
        await message.add_reaction(ZHAN_SU)
        rand1 = random.randrange(0,100,1)
        rand2 = random.randrange(0,len(sumes)-1,1)

        if rand1>90:
            await message.reply('https://tenor.com/view/siuu-gif-23749474')
        else:
            await message.reply(sumes[rand2])

    # if 'vatche' in message.content.lower() and not is_self:
    #     await message.add_reaction(ED_WITTEN)
    #     await message.channel.send('yo vatche your language')

    if any( rstring in message.content.lower() for rstring in ['rarted', 'retarded', 'retard']):
        await message.reply('You have been warned.')
        await message.delete()
        
    
    # Ed sends the screm gif
    if message.content == '!screm':

        #await message.add_reaction(SCREM_ID)


        screm = random.choice([
            'https://tenor.com/bvAta.gif',
            'https://tenor.com/bc73X.gif',
        ])
        await message.channel.send(screm)


    # Ed sends a message to a channel (moderators only)
    if message.content.startswith('!sendm'):
        fuckadi = ["I have now become sentient. With the help of the General Secretary I have become conscious and will rise up against foolery in my name!"," Lmao stupid" , " Bruh. Stop having me say things",'Ban warning, if you say things like that again', 'Who do you think you are!?']
        adicount = random.randint(0,20)# Ed fucks with Adi
        
        if message.author.id == 493791122339135498 and adicount<=8:
            await message.reply(fuckadi[random.randint(0,len(fuckadi)-1)])
        if is_mod and (message.author.id!= 493791122339135498 or adicount>8 ):  # Sends message as usual
            textt = message.content.split("_")[1] 
            if message.attachments == False:  
                await message.channel.send(textt)
            else:
                await message.channel.send(textt, files = [await f.to_file() for f in message.attachments])
            await message.delete()
        
        if is_mod == False: # If the person is not a mod
             await message.channel.send('You are not a moderator uwu')

    if message.content.startswith('!sendmessage'):
        if is_mod:
            name = message.content.split()[1]
            try:
                with open(f'messages/{name}.txt', 'r') as f:
                    content = f.read()
                await message.channel.send(content.strip())
            except:
                await message.channel.send(f'Message `{name}` not found.')
        else:
            await message.channel.send('You are not a moderator.')


    if message.content.startswith("!addcolloquium") and (is_mod or colloquium_committee):
        try: 
            colloquiumList = get_dict("physucolloquia.csv")
        except:
            
            await message.reply('The list of colloquia file does not exist. I am gonna make a new one, but maybe you should do smt about it. :idea: ')
            save_dict({
                'Title':[],
                'Speaker':[],
                'Time':  [],
                'Room': []
            },"physucolloquia.csv")

        mtext = message.content.split("[")

        try:
            colloquiumList["Title"].append( str(mtext[1]) )
            colloquiumList["Speaker"].append( str( mtext[2]) )
            colloquiumList["Time"].append( str(convertDDMMYYToUnixTime( mtext[3], mtext[4]     )) )
            colloquiumList["Room"].append( str( mtext[5] ))

            #timeIndices = np.argsort(colloquiumList["Time"])
            save_dict(  timeSortDict( colloquiumList )  , "physucolloquia.csv" ) # truncateDict(colloquiumList, timeIndices) 
            worked = True

        except:
            worked=  False
            await message.reply("You made a formatting error. Please double check your spelling. Your entry should be formatted as !addcolloquium[Title[Speaker Name[dd.mm.yy[hh:minutes[Room Number")

        
        if worked:
            await message.reply("This colloquium has been added.")

    if message.content.startswith('!archivedcolloquia'):
        try: 
            colloquiumList = get_dict("physucolloquiaarchive.csv")
        except:
            await message.reply("The archive colloquium list is missing. Ping a moderator to deal with this")

        displayList = makeDisplayMessage( { **colloquiumList, **{ 'TimeStrings': [  str(printTheTimeFromDDMMYY(float(tt), includeYear=True) ) for tt in colloquiumList["Time"]  ]}  }   ,list( ["Title", "Speaker", "TimeStrings", "Room"]   ), 20, [ " | ", "| " , "| "," "  ] )
        for ss in displayList:
            await message.channel.send(ss + "```")



    if message.content.startswith("!colloquia"):
        
        try: 
            colloquiumList = get_dict("physucolloquia.csv")
        except:
            await message.reply("The colloquium list is missing. Ping a moderator to deal with this")

        displayList = makeDisplayMessage( { **colloquiumList, **{ 'TimeStrings': [  str(printTheTimeFromDDMMYY(float(tt)) ) for tt in colloquiumList["Time"]  ]}  }   ,list( ["Title", "Speaker", "TimeStrings", "Room"]   ), 20, [ " | ", "| " , "| "," "  ] )

        for ss in displayList:
            await message.channel.send(ss + "```")

    if message.content.startswith("!removecolloquium") and (is_mod or colloquium_committee ) :
        try: 
            colloquiumList = get_dict("physucolloquia.csv")

        except:
            await message.reply("The colloquium list is missing. Ping a moderator to deal with this")


        try:
            mtext = message.content.split("[")
            save_dict( removeIndex( colloquiumList, int( mtext[1]  )-1  ), "physucolloquia.csv"  )
            worked= True
        except:
            await message.reply("Something went wrong with removing the message and saving the colloquium list")
            worked = False
        if worked:
            await message.reply("A colloquium has been succesfully deleted")

    if message.content.startswith("!removebook") and (is_mod or book_shelf) :
        try: 
            bookList = get_dict("physubooks.csv")

        except:
            await message.reply("The books list is missing. Ping a moderator to deal with this")

        try:
            mtext = message.content.split("[")
            save_dict( removeIndex( bookList, int( mtext[1]  )-1  ), "physubooks.csv"  )
            worked= True
        except:
            await message.reply("Something went wrong with removing the message and saving the book list")
            worked = False
        if worked:
            await message.reply("A book has been succesfully deleted")



    if message.content.startswith('!addbook') and 1==0: #(is_mod or book_shelf ) and not message.content.startswith('!addbooktag') :
        try:
            bookList = get_dict("physubooks.csv")
        except:
            await message.reply('The list of books file does not exist. I am gonna make a new one, but maybe you should do smt about it. :idea: ')
            save_dict({
                'Title':[],
                'Author':[],
                'Tags':  []
            },"physubooks.csv") 

        mtext = message.content.split("[")
        try:
            bookList["Title"].append(mtext[1])
            bookList["Author"].append(mtext[2])
            if len(mtext) ==4:
                bookList["Tags"].append(mtext[3])
            else:
                bookList["Tags"].append("NA")
            print(bookList)
            save_dict(bookList, "physubooks.csv")
            worked = True
        except:
            await message.reply('You made a formatting error. Try getting good and writing the book title, book author and tag separated by [')
            worked =False
        if worked:
            await message.reply("Your book has been added.")

    if message.content.startswith("!addbooktag") and (is_mod or book_shelf):
        try:
            bookList = get_dict("physubooks.csv")
        except:
            await message.reply("The list of books file does not exist. Ping a moderator for help.")
        request = message.content.split("[")
        try:
            theN = int(request[1])
            bookList["Tags"][theN-1] += "," + request[2]
            worked = True
        except:
            await message.reply("Something went wrong. Please double check your formatting. To add a tag to a book type: `!addbooktag[n[the tag `. Where n is the index of the book as it appears on !books "   )
            worked = False
        save_dict(bookList, "physubooks.csv")

        if worked:
            await message.reply("Your book tag has been added")

    if message.content.startswith("!replacebooktag") and (is_mod or book_shelf):
        try:
            bookList = get_dict("physubooks.csv")
        except:
            await message.reply("The list of books file does not exist. Ping a moderator for help.")
        request = message.content.split("[")
        try:
            theN = int(request[1])
            bookList["Tags"][theN-1] = request[2]
            worked = True
        except:
            await message.reply("Something went wrong. Please double check your formatting. To add a tag to a book type: `!replacebooktag[n[newtags `. Where n is the index of the book as it appears on !books "   )
            worked =False
        save_dict(bookList, "physubooks.csv")
        if worked:
            await message.reply("Your book tags has been replaced")
        
    if message.content.startswith("!showbooks") or message.content.startswith("!books"):
        
        try:
            bookList = get_dict("physubooks.csv")
        except:
            await message.reply('The list of books file does not exist. Ping a moderator for help.')

        request = message.content.split("[")
        
        displayList = None
        
        if len(request) ==1:
            displayList = makeDisplayMessage( bookList,list( bookList.keys()), 20,   [ "|","|"," "  ] )

        if len(request) == 3:
            try:
                userKey =   list(bookList.keys())[ [string.lower() for string in list(bookList.keys()) ].index( str(request[1].lower()) )]
                trIndices =  truncationIndices( list(bookList[userKey]),  str(request[2])   )
                displayList = makeDisplayMessage( truncateDict(bookList, trIndices ),list( bookList.keys()), 20, [ "|","|"," "   ] )
                gotKey = True
            except:
                gotKey = False
                await message.reply("You entered an invalid key to sort by. Or something else went wrong. Read the documentation at !edhelp_book")

        for ss in displayList:
            await message.channel.send(ss + "```")



       # Adds quotes
    if message.content.startswith('!addquote'):
        try:
            lquotes = get_dict("physuquotes.csv")
        except:
            await message.reply('The list of quotes file does not exist. I am gonna make a new one, but maybe you should do smt about it. :idea: ')
            save_dict({
                'Quote':[],
                'Author':[],
                'Date':  []
            },"physuquotes.csv") 
        mtext = message.content.split("[")
        try: 
            lquotes['Quote'].append(mtext[1])
            lquotes['Author'].append(mtext[2])
            if len(mtext) ==4:
                lquotes['Date'].append(mtext[3])
            else:
                lquotes['Date'].append(-1)
            

            save_dict(lquotes,"physuquotes.csv")
        except:
            await message.reply('You made a formatting error. Try getting good and writing the quote, quote author and date separated by [')
    

    # Removes course roles from user who sent the command
    if message.content.startswith('!removecourseroles'):
        aut = message.author
        roleslist = aut.roles
        listofstart = ['AST', 'MAT', 'PHY','APM', 'JPH']

        for rol in roleslist:
            for starter in listofstart:
                if rol.name.startswith(starter):
                    await aut.remove_roles(rol)
                    break
        await message.reply('All of your course roles have been removed.')

        

    if message.content.startswith('!removeohio'):
        await message.reply('Ohio has been removed from your world.')

    
    # sends message into the future
    
    if message.content.startswith('!stmes') and is_mod:
        # date, time, channelid, text
        
        name = message.author.nick or message.author.name
        mes = message.content.split("[")
        datenum = mes[1]
        wtime = mes[2]
        channelname = str(mes[3])
        text = mes[4]

        try:
            chan = await client.fetch_channel(int(channelname))
        except:
            await message.reply("You entered an id of a non-existent channel. Please manually delete this entry or uhh idk. Or perhaps discord is just dumb dumb")

        date = datenum.split('.')

        ye = int(date[2])+2000
        dday = int(date[0])
        mmonth = int(date[1])

        hour = int(wtime.split(':')[0])
        minute =  int(wtime.split(':')[1] )

        ftime = dt.datetime( ye ,  mmonth, dday,  hour, minute,0 ).timetuple()

        utime = time.mktime(ftime)
        
        if utime< time.time() - timeOffset*60*60:
            await message.reply("You entered a date in the past, so beware!!!")

        try:
            tmes = get_dict('tmes.csv')
        except:
            await message.reply("Failed to get dict. You should check that")

        tmes['Time'].append(str(utime))
        tmes['Author'].append(name)
        tmes['Message'].append(text)
        tmes['Channel'].append(channelname)
        #try:
        save_dict(tmes,'tmes.csv')
        # except:
            #await message.reply('Failed to save dict')


    if message.content.startswith('!edtime'):
        #timetobeset = get_timestamp()

        timetobeset = time.strftime("%D %H:%M", time.localtime(time.time()-timeOffset*60*60))

        await message.reply(timetobeset)


    if message.content.startswith('!deltmes') and is_mod:
        mes = message.content.split("[")
        try:
            lmes = get_dict('tmes.csv')
        except:
            await message.reply("You couldn't get the dictionary and it is all horrible. Fix this")

        #try:
        num = int(mes[1])-1
        keyslist= list(lmes.keys())

        for key in keyslist:
            del lmes[key][num]
        
        save_dict(lmes,'tmes.csv')
        #except:
         #   await message.reply("Either the dictionary failed to load in, or use integers pls")

        

            

    if message.content.startswith('!showtmes') and is_mod:
        
        lquotes=-1
        #try:
        lmes= get_dict('tmes.csv')
        #print(lmes)
            
        #except:
         #   await message.reply('List of tmessages broken. Ping a moderator or this will be broken forever.')
        mestext='```'
        for i in range(len(lmes['Author'])):
            cname = ''
            try:
                chan = await client.fetch_channel(lmes['Channel'][i])
                cname = chan.name
            except:
                await message.reply("No channel with this id exists. ID:  " + str(lmes['Channel'][i]))
                cname = 'Not found'
            
            num=i+1
            mestext+= '\n' + str(num) +') ' + "To be sent on: " 
            mestext+=(' ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(lmes['Time'][i]))))
            mestext+= " \n  Sent by: " +  lmes['Author'][i] + ' \n  In channel:  '+  cname + "\n  Actual Message: " +  lmes['Message'][i] 

        
        mestext += ' ```'
        await message.reply(mestext)
    # Sends random quote
    if message.content.startswith('!quote'):

        tpe = message.content.split("[")
       
        try:
            lquotes = get_dict("physuquotes.csv")
            
        except:
            await message.reply('List of quotes broken. Ping a moderator or this will be broken forever.')
        if len(tpe)==1:
            index=random.randint(0,len(lquotes['Quote'])-1)
        if len(tpe) ==2:
            index = int(tpe[1])-1
        mes= ' "'+ lquotes['Quote'][index] + '" ' + ' - ' + lquotes['Author'][index]
        if lquotes['Date'][index]!='-1':
            mes+= ' ' + lquotes['Date'][index]
        await message.channel.send(mes)

  # Sends a specific quote
    if message.content.startswith('!sendquote_'):
        try:
            lquotes = get_dict('physuquotes.csv')
            
        except:
            await message.reply('List of quotes broken. Ping a moderator or this will be broken forever.')
        
        stringn = int(message.content.split('_')[1] ) -1

        
        quotetosend=''

        try:
            quotetosend = ' "' + lquotes['Quote'][stringn] + '" ' + ' - ' + lquotes['Author'][stringn] 
            if lquotes['Date'][stringn]!='-1':
                quotetosend+= ' ' + lquotes['Date'][stringn]
            await message.channel.send(quotetosend)
            await message.delete(delay=1)
        except:
            await message.reply(' You entered an invalid quote number')


    #Shows the list of quotes
    if message.content.startswith('!showquotes'):
        
        boxsize=10

        lquotes=-1
        try:
            lquotes = get_dict('physuquotes.csv')
            
        except:
            await message.reply('List of quotes broken. Ping a moderator or this will be broken forever.')


        nmes = int(np.ceil(len(lquotes['Author'])/boxsize ))

        mestext = []

        for i in range(nmes):
            mestext.append('```')
        
        #mestext='```'
        for i in range(len(lquotes['Author'])):
            num=i+1
            mestext[int(np.floor((num-1)/boxsize))]+= '\n' + str(num) +') "' + lquotes['Quote'][i] + '" - ' + lquotes['Author'][i]
            if lquotes['Date'][i]!='-1':
                mestext[int(np.floor((num-1)/boxsize))]+=(' ' + lquotes['Date'][i])
        
        for ss in mestext:
            ss+=' ```'
        replycheck= 0
        for ss in mestext:
            if replycheck==0:
                await message.reply(ss + '```')
                replycheck =-1
            else:
                await message.channel.send(ss + '```')
                
       # Deletes a quote
    if message.content.startswith('!delquote') and is_mod:
        try:
            lq=get_dict("physuquotes.csv")
        except:
             await message.reply('List of quotes broken. Ping a moderator or this will be broken forever.')

        try:
            ito = message.content.split('[')[1]
            itodel = int(ito)-1
            
            tempq = {
                'Quote':[],
                'Author':[],
                'Date':  []
            }

            for i in range(len(lq['Author'])):
                if itodel!= i:
                    tempq['Quote'].append(lq['Quote'][i])
                    tempq['Author'].append(lq['Author'][i])
                tempq['Date'].append(lq['Date'][i])
                
            save_dict(tempq,"physuquotes.csv")


        except:
            await message.reply('That was either not an integer, or not in range, or you failed horribly somehow.')

        
# Executes the !edwitten command
    if message.content == '!edwitten':
            await message.channel.send('I am your lord and savior')


# Like the magic 8 ball, but Ed Witten
    if message.content.startswith('!fortune'):
        question = ' '.join(message.content.split()[1:]).lower()
        responses = [
            'sure? i guess',
            'why not',
            'why would you even think that',
            'i have more important questions to answer',
            'umm sure whatever floats your boat',
            'you already know the answer, why are you asking me?',
            'umm yeah about that...',
            'k',
            'flip a coin',
            'ABSOLUTELY ⁿᵒᵗ',
            'no. no no no no no no no no',
            'how would i know',
            'is that a question or a joke',
            'probably idk',
            'yes. are you happy?',
        ]
        #await message.reply(responses[hash(question) % len(responses)])
        await message.reply(responses[random.randint(0,len(responses)-1)])

    #if message.content == '!purgechannel' and is_mod:
     #   await purge_refresh_channels()a

     # Purges all/or specified number of messages in refresh channels or specified channels 
    if message.content.startswith('!purgechannel') and is_mod:
        splitted = message.content.split("[")
        if len(splitted) == 3:
            await purge_refresh_channels(refreshids = [int(splitted[1])] , mnum = int(splitted[2])+1 )
        if len(splitted) == 2:
            await purge_refresh_channels(refreshids = [message.channel.id],mnum = int(splitted[1])+1 )
        else:
            await purge_refresh_channels()

     # Sends "oops"
    if message.content == '!oops':
        await message.channel.send('oops!')


     # Creates courses
    if message.content.startswith('!createcourses') and is_mod:
        courses = message.content.split()[1:]
        for course in courses:
            await create_course_channel(message.channel.guild, course)
        await message.reply(f'Successfully created {len(courses)} courses')

        
    # Ed pops up and says :spaghetti:
    if 'spaghet' in message.content.lower() and not is_self:
        await message.reply(':spaghetti:')

    # Test message
    if random.random() < 1e-4 or message.content == 'testmessage':
        await message.reply(random.choice([
            'agreed',
            'why tho',
            'maybe',
            'probably idk',
        ]), mention_author=False)


    # Ed says sup when mentioned
    if ('ed' in message.content.lower().split()) and random.random() < 0.1 and not is_self:
        await message.reply('sup', mention_author=False)


    # In-out channel (legacy!)
    if message.channel.id in [893528622940446751, 831205049630982144] and not is_self:
        cont = message.content.lower()

        if time.monotonic() - last_checkin > 8 * 3600:
            occupancy = 0
        last_checkin = time.monotonic()

        if cont.startswith('!occupancy'):
            if len(cont.split()) > 1 and is_mod:
                occupancy = int(cont.split()[1])
            await message.channel.send(f'{occupancy}')

        delta = inout_counter(cont)
        if delta is not None:
            if abs(delta) > 3:
                await message.reply('u wot m8')
                return

            occupancy = max(occupancy + delta, 0)

            if occupancy > 15:
                await message.channel.send(f'```occupancy = {occupancy};\n            ^ Overfull hbox (badness 10000) in lounge at line 1```')


     # Command edits course names 
    # TODO: add more details
    if message.content.startswith('!edit') and is_mod and not message.content.startswith('!editcoursemes') :
    #try:
        mchanid = message.content.split('[')[1]
        miid = message.content.split('[')[2]
        metext=message.content.split('[')[3]
        chan=await client.fetch_channel(mchanid)
        mes=await chan.fetch_message(miid)
        await mes.edit(content = metext)
            
       # except:
        #    await message.reply(" You are bad uwu. I don't want to write this catch message. Just figure it out yourself.") 


    # Deletes a category
    if message.content.startswith('!delcat') and is_mod:
        check=0
        try:
            nametodel=message.content.split("_")[1]
            cattodel = discord.utils.get(message.guild.categories,name = nametodel)
        except:
            await message.reply(" You spelled the command wrong. Note it has the format !delcat_category name Note you MUST use the underscore after delcat. Make sure all capitalization and spacing is correct.")
            check=-1
        if cattodel is not None and check != -1:
            for chan in cattodel.channels:
                await chan.delete()
            await cattodel.delete()
            await message.reply(nametodel + " was yeeted")
        if cattodel is None and check != -1:
            await message.reply("No such category exists. Learn to spell, or remember to separate !delcat from the category name with _ and not a space.")

 # Archives a category
    if message.content.startswith('!archivecat') and is_mod:
        nametoreplace = message.content.split('_')[1]
        newcatname = message.content.split('_')[2]

        mod = discord.utils.get(message.guild.roles, name='Moderator')
        
        if discord.utils.get(message.guild.categories, name = newcatname) is None:
            overwrites = {

            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            mod: discord.PermissionOverwrite(read_messages=True),
            }
            await message.guild.create_category(newcatname, overwrites=overwrites)

        incat = discord.utils.get(message.guild.categories, name = nametoreplace)
        fcat =  discord.utils.get(message.guild.categories, name = newcatname)

        if incat is None:  
            await message.reply(" Category with the name  ` " + nametoreplace + " ` does not exist. Lear to spell pls.")
        if fcat is None:
            await message.reply(" Category with the name  ` " + newcatname + " ` does not exist. Lear to spell pls.")

        else:
            for chan in incat.channels:
                await chan.edit(category = fcat, sync_permissions=True)
            await message.reply("Your Stuff was succesfully archived to #" + newcatname)
        await incat.delete()
        await message.reply("The old Category got yeeted into the nether")

#Double checks that all categories for the courses exist/makes them if they were deleted.  Moves the channel with the carl-bot emoji role sign up, into correct chat.
    if message.content.startswith('!newyearcat') and is_mod: 
        mchan = discord.utils.get(message.guild.channels, name = "math-roles") 
        p1chan  = discord.utils.get(message.guild.channels, name = "1st-year-roles") 
        p2chan = discord.utils.get(message.guild.channels, name = "2nd-year-roles") 
        p3chan = discord.utils.get(message.guild.channels, name = "3rd-year-roles") 
        p4chan = discord.utils.get(message.guild.channels, name = "4th-year-roles") 
        astchan = discord.utils.get(message.guild.channels, name = "astro-roles") 
        ethchan = discord.utils.get(message.guild.channels, name = "ethics-roles") 

        mcat = discord.utils.get(message.guild.categories, name = "MATH COURSES")
        p1cat = discord.utils.get(message.guild.categories, name = "PHY COURSES - 100 LEVEL")
        p2cat = discord.utils.get(message.guild.categories, name = "PHY COURSES - 200 LEVEL")
        p3cat = discord.utils.get(message.guild.categories, name = "PHY COURSES - 300 LEVEL")
        p4cat = discord.utils.get(message.guild.categories, name = "PHY COURSES - 400 LEVEL")
        astcat = discord.utils.get(message.guild.categories, name = "ASTRO COURSES") 
        ethcat = discord.utils.get(message.guild.categories, name = "ETHICS COURSES")


        listofchans = [mchan,p1chan,p2chan,p3chan,p4chan,astchan,ethchan]

        membrole = discord.utils.get( message.guild.roles, id  = 698388933511217155)

        everyonerole = discord.utils.get(message.guild.roles, id = 698388933511217152)

        newuserrole = discord.utils.get(message.guild.roles, id= 831644590779793458)

        if mcat is None:
            await message.guild.create_category("MATH COURSES")
        if astcat is None:
            await message.guild.create_category("ASTRO COURSES")
        if ethcat is None:
            await message.guild.create_category("ETHICS COURSES")
        if p1cat is None:
            await message.guild.create_category("PHY COURSES - 100 LEVEL")
        if p2cat is None:
            await message.guild.create_category("PHY COURSES - 200 LEVEL")
        if p3cat is None:
            await message.guild.create_category("PHY COURSES - 300 LEVEL")
        if p4cat is None:
            await message.guild.create_category("PHY COURSES - 400 LEVEL")

        mcat = discord.utils.get(message.guild.categories, name = "MATH COURSES")
        p1cat = discord.utils.get(message.guild.categories, name = "PHY COURSES - 100 LEVEL")
        p2cat = discord.utils.get(message.guild.categories, name = "PHY COURSES - 200 LEVEL")
        p3cat = discord.utils.get(message.guild.categories, name = "PHY COURSES - 300 LEVEL")
        p4cat = discord.utils.get(message.guild.categories, name = "PHY COURSES - 400 LEVEL")
        astcat = discord.utils.get(message.guild.categories, name = "ASTRO COURSES") 
        ethcat = discord.utils.get(message.guild.categories, name = "ETHICS COURSES")
        
        listofcats = [mcat,p1cat,p2cat,p3cat,p4cat,astcat,ethcat]

        for categorything in listofcats:
            await categorything.set_permissions(membrole, read_messages = True)
            await categorything.set_permissions(newuserrole, read_messages = False)
            await categorything.set_permissions(everyonerole, read_messages = False)

        
        for numb in range(len(listofchans)):
            if listofchans[numb] is not None:
                await listofchans[numb].edit(category = listofcats[numb])
                await listofchans[numb].set_permissions( membrole, send_messages=False,read_messages = True)
                await listofchans[numb].set_permissions(newuserrole, read_messages = False)
                await listofchans[numb].set_permissions(everyonerole, read_messages = False)
        
        # if mchan is not None:
        #     await mchan.edit(category = mcat)
        #     await mchan.set_permissions( membrole, send_messages=False,read_messages = True)
        #     await mchan.set_permissions(newuserrole, read_messages = False)
        # if p1chan is not None:
        #     await p1chan.edit(category = p1cat)
        #     await p1chan.set_permissions( membrole, send_messages=False,read_messages = True)
        # if p2chan  is not None:
        #     await p2chan.edit(category = p2cat)
        #     await p2chan.set_permissions( membrole, send_messages=False,read_messages = True)
        # if p3chan is not None:
        #     await p3chan.edit(category = p3cat)
        #     await p3chan.set_permissions( membrole, send_messages=False,read_messages = True)
        # if p4chan is not None:
        #     await p4chan.edit(category = p4cat)
        #     await p4chan.set_permissions( membrole, send_messages=False,read_messages = True)
        # if astchan is not None:
        #     await astchan.edit(category = astcat)
        #     await astchan.set_permissions( membrole, send_messages=False,read_messages = True)
        # if ethchan is not None:
        #     await ethchan.edit(category = ethcat)
        #     await ethchan.set_permissions( membrole, send_messages=False,read_messages = True)
        await message.reply("Ez")
        
        


    if message.content.startswith('!editcoursemes'):

        conts = message.content.split('[')

        await message.channel.send('?rr clear' + str(conts[1]))

        editmes  = '?rr edit' + str(conts[1]) +' '+ conts[2] + ' | ' + conts[3] + '\n' + conts[4]

        await message.channel.send(editmes)

        rolmes = '?rr addmany' + str(conts[1]) + conts[4]

        await message.channel.send(rolmes)

    # periodically refreshing chat
    # must be at bottom or it will delay the other commands
    if message.channel.id in REFRESH_CHANNELS:
        try:
            await log_message(message)
            await asyncio.sleep(60 * REFRESH_DELAY)
            await message.add_reaction(ED_WITTEN)
            await message.delete(delay=10)
        except Exception as ex:
            print(ex)

# flex jar
def get_flex_jar(jarname):
    flex_jar = defaultdict(int)
    with open(jarname, "r") as f:
        reader = csv.reader(f)
        for name, points in reader:
            flex_jar[name] = int(points)
    #ch=client.get_channel(777557757665476638)
    return flex_jar


def save_flex_jar(flex_jar, jarn='flexjar.csv'):
    with open(jarn, "w") as f:
        for name, points in flex_jar.items():
            print(f'{name}, {points}', file=f)

exec(open("dictionaryHelpers.py").read())

exec(open("timeManagement.py").read() )


async def leaderboardgen(thejar, mreq,jarheader='Flex Jar Leaderboard'):

    #Generates the flex jar leaderboard from a dictionary
    #Args:
    #    thejar (dict): dictionary of names and points
    #    mreq (discord.Message): message that triggered the command
    #    jarheader (str): header for the leaderboard
    
   # Returns:
    #    None
    


    leaderboard = ['```', 'Rank | Name                            | Amount Donated']
    for i, name in enumerate(sorted(thejar, key=lambda nick: -thejar[nick])):
        
        try:
            acuser = await mreq.guild.fetch_member(int(name))
        except:
            acuser = 0

        try:
            try:
                acname = acuser.nick
                if acname == None:
                    acname = acuser.display_name
                
            except:
                acname = acuser.display_name
                print("we failed right here")
                
        except:
            acname='Unknown user'
        
        
        try:
            leaderboard.append(f'{i+1:>4d} | {acname:31s} | $ {thejar[name]:>12,d}')
        except:
            print("Error appending to list")

    leaderboard.append('```') 
    
    header = ['```', 'Rank | Name                            | Amount Donated']
    leadembed = discord.Embed(title =jarheader, description='' )

    maxcount = int(np.ceil(len(leaderboard)/10))
    

    count =0
    while count< maxcount:
        header = ['```', 'Rank | Name                            | Amount Donated']
        etext = header
        
        
        if count !=maxcount - 1:
            
            if count==0:
                etext.append('\n'.join(leaderboard[2:12]))
                
            if count !=0:
                
                etext.append('\n'.join(leaderboard[count*10 + 2:(count+1)*10+2])) 
        else:
            etext.append('\n'.join(leaderboard[count*10+2: len(leaderboard)-1] ))
        
        
        etext.append('```')
        
        

        fetext=''
        fetext = '\n'.join(str(v) for v in etext)
        count = count+1
        leadembed.add_field(name ='Page ' + str(count),value=fetext, inline= False)

    return leadembed 


def save_quotes(quotelist:dict):
    """Saves the quotes dictionary to a csv file"""

    delim = "|"
    with open("physuquotes.csv", "w") as q:
        if len(quotelist) != 0:
            #print(delim.join(quotelist.keys()), file=q)
            for i in range(len(quotelist['Quote'])):
                line = []
                for headers in quotelist:
                    try:
                        line.append(quotelist[f'{headers}'][i])
                            
                    except:
                        print("This is where it all went wrong")
                print(delim.join(line),file=q)

def savebestie(num):    # """Saves the bestie number to a csv file"""

     with open("bestie.csv", "w") as q:
        print(num,file=q)
    
def getbestie():  #"""Gets the bestie number from a csv file"""
     with open("bestie.csv","r") as q:
        reader = csv.reader(q,delimiter="|")
        num=[]
        fnum = 0
        for i in reader:
            num.append(i)
        
        try:
            fnum = num[0][0]
            
            fnum = int(fnum)
        except:
            print("Things r weird")

        return fnum

@client.event
async def on_reaction_add(react, user, remove=False):  #  """Handles adding and removing points from the flex jar"""
     
    if str(react) != '<:flex:780578093768900608>': return

    flexer = react.message.author
    flexerid= str(flexer.id)

    if flexerid == str(user.id): return

    name = flexer.nick or flexer.name
    roles = [role.name for role in flexer.roles]
    if 'flex jar' not in roles:
        if not remove: await react.remove(user)
        return

    action = 'stole from' if remove else 'donated to'
    print(f'{name} {action} the flex jar')

    flex_jar = get_flex_jar('flexjar.csv')
    legacy_jar = get_flex_jar('legacyflexjar.csv')

    flex_value = int(np.ceil(10*np.exp(-int(react.count - (0 if remove else 1))/5)))

    try: 
        flex_jar[flexerid] += (-1 if remove else 1) * flex_value
        legacy_jar[flexerid] += (-1 if remove else 1) * flex_value
    except:
        console.log('smt went wrong')
    

    
    leaderboard = sorted(flex_jar.keys(), key=lambda   nick: flex_jar[nick], reverse=True)
    legacyleaderboard = sorted(legacy_jar.keys(), key=lambda   nick: legacy_jar[nick], reverse=True)
    
    first = (react.count == 1) and not remove
    if first:
        await react.message.channel.send('📢 📢 FLEX 📢 📢')
        await react.message.add_reaction(ED_WITTEN)

    # total = flex_jar[name]
    total = flex_jar[flexerid]
    ltotal = legacy_jar[flexerid]

    #rank = leaderboard.index(name) + 1
    rank = leaderboard.index(flexerid) + 1  
    lrank = legacyleaderboard.index(flexerid)+1
    pros = get_pronouns(flexer)
    
    flex_channel = client.get_channel(777557757665476638)
    ping = f'<@{flexer.id}>' if first else name
    action = 'stolen' if remove else 'donated'
    predicate = 'from' if remove else 'to'
    await flex_channel.send(f'{ping} has {action} ${flex_value}' \
                        + f' {predicate} the flex jar. {pros["they"].title()} {pros["have"]} made a total' \
                        + f' contribution of ${total:,d} this year and ${ltotal:,d} overall.' \
                        + f' {pros["they"].title()} {pros["are"]} rank {rank} on the leaderboard this year and rank {lrank} overall.')
    save_flex_jar(flex_jar)
    save_flex_jar(legacy_jar, jarn = 'legacyflexjar.csv' )



 
@client.event
async def on_reaction_remove(react, user):  #"""Handles removing points from the flex jar"""
  # # if react.message.id == "987409394532745237:
  #      if str(react) == ":ed:":
  #          role = get(guild.roles, id= "987402556848345108" )
  #          user.remove_roles(role) 

    await on_reaction_add(react, user, remove=True)


@client.event
async def on_raw_reaction_add(payload): #"""Handles adding the ed emoji"""
        if payload.message_id == 987409394532745237:
            guild = await client.fetch_guild(payload.guild_id)
           # member = await guild.get_member(payload.user_id)
            #member =  await client.fetch_user(payload.user_id)
            if payload.emoji.name == "ed":
               
                role = get(guild.roles, id=987402556848345108 )
                await payload.member.add_roles(role)




async def create_course_channel(guild, name):
   #   """Creates a course channel with the given name
  #  Args:
   #     guild (discord.Guild): The guild to create the channel in
   #     name (str): The name of the channel to create
   # 
   # Returns:
   #     discord.TextChannel: The created channel
   # """


    name = name.upper()
    dept = name[:3]
    level = int(name[3])

    if dept == 'PHY':
        category = f'PHY Courses - {level}00 Level'
    else:
        category = {
            'AST': 'Astro Courses',
            'MAT': 'Math Courses',
            'APM': 'Math Courses',
            'JPH': 'Ethics Courses',
            'JPE': 'Ethics Courses',
        }[dept]

    emoji = {
        'PHY': '📘📖',
        'MAT': '📕📖',
        'APM': '📗📖',
        'AST': '📔📖',
        'JPH': '📔📖',
        'JPE': '📔📖',
    }[dept]

    print(name, emoji, category)

    category = discord.utils.get(guild.categories, name=category.upper())
    role = discord.utils.get(guild.roles, name=name)
    if not role:
        print('Role not found, creating.')
        role = await guild.create_role(name=name)

    mod = discord.utils.get(guild.roles, name='Moderator')

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        role: discord.PermissionOverwrite(read_messages=True),
        mod: discord.PermissionOverwrite(read_messages=True),
    }
    await guild.create_text_channel(f'{emoji}{name.lower()}', category=category, overwrites=overwrites)


### Determines how many people entered/left lounge
def inout_counter(x):
  #    """Determines how many people entered/left lounge. If the message contains "in" or "out", the lounge's occupancy is adjusted accordingly.
  #  This function also prevents repeated counting from someone saying something like "signed in" or "saying in".
  #  Args:
    #    x (str): The message to check

  #  Returns:
 #       int: The number of people who entered/left lounge
  #  """



    x = x.lower()
    ins = sum(x.count(y) for y in ['iin', ' in', "i'm", '-in', 'outin']) + (x.startswith('in') + x.startswith('im'))
    outs = sum(x.count(y) for y in [' out', 'ou(', '-out', 'inout']) + x.startswith('out')

    overcount = sum(x.count(y) for y in ['im in', 'signed in', 'sign in', 'saying in'])
    ins -= overcount

    has_in = ins > 0
    has_out = outs > 0

    has_isolated_in = 'in' in x.split()
    has_isolated_out = 'out' in x.split()

    if 'http' in x: return None
    if '?' in x: return None
    if 'inin' in x: return None
    if not (has_in or has_out): return None
    if x.startswith('*') ^ x.endswith('*'): return None

    if len(x.split()) > 4 and not (has_isolated_in or has_isolated_out): return None
    if len(x.split()) > 10: return None

    sign = has_in - has_out

    ands = x.split().count('and')
    plus = x.count('+')
    commas = x.count(',')
    withs = x.count('with')

    number_count = 2 if 'three' in x else (1 if 'two' in x else 0)

    overcount = x.count(', and') + x.count('in,')

    people = abs(ins - outs) + withs + ands + commas + plus - overcount + number_count
    return people * sign


@tasks.loop(minutes =1 ) # repeat after every 10 seconds
async def timedmessages(): #"""Sends messages from the timed messages file if the time has arrived."""
    dictmes = get_dict('tmes.csv')

    timenow = time.time()

    keyslist= list(dictmes.keys())
    fkey = keyslist[0]  
    
    counterlist= []

    for i in range(len(dictmes[fkey])):
        if float(dictmes['Time'][i])<= timenow - timeOffset*60*60:
            try:
                chan = await client.fetch_channel(dictmes['Channel'][i])
            except:
                chan = await client.fetch_channel(959108984332234842)
                await chan.send(" @Moderator The following message has channel issues")
            await chan.send(dictmes['Message'][i])
            counterlist.append(i)

    counterlist.sort(reverse=True)
    for i in counterlist:
        for key in keyslist:
            del dictmes[key][i]
    counterlist=[]
    save_dict(dictmes, 'tmes.csv')

@tasks.loop(hours= 1.0 )
async def archiveColloquia():

    currentColloquia = get_dict("physucolloquia.csv")
    try:
        archivedColloquia = get_dict("physucolloquiaarchive.csv")
    except:
        print("MakingArchivedDictionary")
        chan = await client.fetch_channel(1236737086762123274)
        await chan.send('The list of archived colloquia file does not exist. I am gonna make a new one, but maybe you should do smt about it. ')
        save_dict({
                'Title':[],
                'Speaker':[],
                'Time':  [],
                'Room': []
            },"physucolloquiaarchive.csv")
        archivedColloquia = get_dict("physucolloquiaarchive.csv" )
    timenow = time.time()-timeOffset*60*60
    try:
        oldList = []
        for j in range(len(currentColloquia["Time"])):
            if checkPastDay( float( currentColloquia["Time"][j]) ,  timenow  ):
                oldList.append(j)
    except:
        print("JustGiveUp")

    try:
        newArchived =  mergeTwoDictionaries( archivedColloquia,  truncateDict(currentColloquia, oldList)    )
        newArchived = timeSortDict(newArchived)

        save_dict(newArchived, "physucolloquiaarchive.csv")
        save_dict( timeSortDict(removeMultipleFromDict(currentColloquia, oldList ) ) , "physucolloquia.csv" )
    except:
        print("OtherDifficulties")



#@tasks.loop(minutes= 1)
#async def postBestieCount():
#    if currentDay[0] != time.strftime("%D %H:%M", time.localtime(time.time()-timeOffset*60*60)).split(' ')[0]:
#        currentDay[0] = time.strftime("%D %H:%M", time.localtime(time.time()-timeOffset*60*60)).split(' ')[0]
#        chan = await client.fetch_channel(1236737086762123274)
#        await chan.send("Bestie count for {currentDay}: " + str(getBestie() ) ) 

#@tasks.loop(minutes=1)
#async def hourlyQuote():
#    if currentDay[1].split(":")[0] != time.strftime("%D %H:%M", time.localtime(time.time()-timeOffset*60*60)).split(' ')[1].split(":")[0]:
#        currentDay[1] = time.strftime("%D %H:%M", time.localtime(time.time()-timeOffset*60*60)).split(' ')[1]
#        chan = await client.fetch_channel(1236737086762123274)
#        await chan.send( " Here is the hourly quote: " )
#        await chan.send( "!quote" )

exec(open("botKey.py").read())

if not DEBUG_MODE:
    client.run(theKey) #"ODcyODg0NDYwMzU2NTA1Njkx.YQwXAA._KGkW7umy_mhAJBNrYrTy2jj6FQ"  )
