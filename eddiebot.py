import discord
from discord.ext import commands
import random
import asyncio
import sqlite3
import logging
#My modules
from helper import *
import DbReader

#TODO
# Some logging possibly?
# Fix .aliases command to link to an HTML table. Play around with bootstrap I guess

class Globals:
    """Class for holding certain global variables.
    All global variables which will be used during the run of the bot
    are defined right from the beginning."""
    #DB variables
    dbConn = None
    dbCursor = None
    charNameAliases = dict()

#Bot has to be spawned early for all the commands.
bot = commands.Bot(command_prefix='.', description='prkbot v0.01')
bot.remove_command('help')

##############################################################################
# Initialization functions
##############################################################################

def initDB(filename):
    conn = sqlite3.connect(filename)
    Globals.dbConn = conn
    Globals.dbCursor = conn.cursor()


def loadCharAliases(filename):
    with open(filename, 'r') as f:
        for line in f:
            line = line.split(',')
            Globals.charNameAliases[line[0].lower()] = (line[1])[:-1] #Last elem is newline - remove


def getAuth(filename):
    with open(filename, 'r') as f:
        token = f.readline()

    return token


##############################################################################
# Bot functions
##############################################################################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')
    print('Connected to servers:')
    for server in bot.servers:
        print(server.name.encode('utf-8'))


async def sendMove(PM, move, simplify, ctx):
    msg = ""
    if simplify:
        msg = "```fix\n{0}: {1} | Startup: {2}f | Active: {3}f | \
Recovery: {4}f | Adv: {5} IB: {6} | Lvl: {7}```".format(move[1], move[2], \
                                                move[3], move[4], move[5], \
                                                move[6], move[7], move[8])
    else:
        msg = "```fix\nChar: {0} | Move: {1}\nStartup: {2}f | Active: {3}f | \
Recovery: {4}f\nFrame adv.: {5} | IB adv: {6} | Level: {7}\nGuard: {8} | \
Tension: {9} | RISC: {10} | Prorate: {11} | Invul: {12} | Damage: {13} | \
Notes: {14}```".format(move[1], move[2], move[3], move[4], move[5], move[6],\
                       move[7], move[8], move[9], move[10], move[11], move[12],\
                       move[13], move[14], move[15])

    if not PM:
        await bot.say(msg)
    else:
        await bot.send_message(ctx.message.author, msg)


async def sendGeneralData(data):
    msg = "```fix\n\
Def. mod.: {1} | GUTS: {2} | Stun res.: {3}\nJump startup: {4} | \
Backdash: {5} | Backdash invul.: {6}\n\
Facedown wakeup: {7} | Faceup wakeup: {8} | Weight: {9}```".format(data[1],\
                                                            data[3], data[4], data[5],\
                                                            data[6], data[7], data[8],\
                                                            data[9], data[10], data[11])
    await bot.say(msg)


async def sendLevel(data):
    msg = "```fix\nAttack level: {0}\n\
Hitstop: {1}f | Standing hitstun: {2}f | Crouching hitstun: {3}f | Air untech: {4}f\n\
Ground block: {5}f | Ground IB: {6}f | Ground FD: {7}f\n\
Air block: {8}f | Air IB: {9}f | Air FD: {10}f```".format(data[0], data[1],\
                                                data[2], data[3], data[4],\
                                                data[5], data[6], data[7],\
                                                data[8], data[9], data[10])
    await bot.say(msg)



async def obtainCharName(char):
    """Helper function which retrieves character name as used in the database.
    Uses the aliases first if possible, then tries to find a perfect fit. If
    a perfect fit cannot be found, uses STARTS WITH."""
    charAlias = Globals.charNameAliases.get(char.lower(), None)
    if charAlias:
        char = charAlias

    q = Globals.dbCursor.execute("select distinct charname from moves where charname=? collate nocase", (char,))
    chars = Globals.dbCursor.fetchall()
    if len(chars) == 1: #Perfect fit has been found, return the name
        return chars[0][0]

    #Couldn't find perfect fit, use starts with
    q = Globals.dbCursor.execute("select distinct charname from moves where charname like ? collate nocase", (char + '%',))
    chars = Globals.dbCursor.fetchall()
    if len(chars) == 1: #Found a candidate, return that
        return chars[0][0]
    elif len(chars) == 0: #No char found
        await bot.say("No possible character found.")
        return False
    else:
        await bot.say("Multiple characters found, specify character name better.")
        return False


async def sendFramedata(ctx, char, simpleOutput):
    msg = ctx.message.content
    msg = ' '.join(msg.split()) #replace all whitespaces with a single one
    msg = msg.split(' ', 2)
    moveName = (' '.join(msg[2:])).lstrip()

    char = await obtainCharName(char) #Obtain character name in case an alias/abbreviation is used
    if char == False:
        return False #Wrong input

    if not moveName:
        #No move name specified, send user a list of all possible moves
        charMoves = await DbReader.getCharMoves(char, Globals.dbCursor)
        await bot.send_message(ctx.message.author, charMoves)
        return

    #If aliases are present in the db for the said move, change vals
    Globals.dbCursor.execute("select value from aliases where key=? collate nocase", (moveName,))
    q = Globals.dbCursor.fetchone()

    if q:
        moveName = q[0]

    if moveName.lower() == 'general':
        moves = DbReader.getFrameData(char, moveName, Globals.dbCursor)
        await sendGeneralData(moves[0]) #User asked for general fdata
        return

    # DbReader.getFrameData() sends a list of query responses. First elem of list taken.
    if moveName.lower() == '5s':
        moves = []
        moves.append(DbReader.getFrameData(char, 'f.s', Globals.dbCursor)[0])
        moves.append(DbReader.getFrameData(char, 'c.s', Globals.dbCursor)[0])
    else:
        moves = DbReader.getFrameData(char, moveName, Globals.dbCursor)

    if len(moves) > 2:
        await bot.say("Found 3 or more moves which satisfy the search query. Sending a PM.")
        for move in moves:
            await sendMove(True, move, simpleOutput, ctx)
    else:
        for move in moves:
            await sendMove(False, move, simpleOutput, None) #no need to pass ctx


@bot.command(pass_context=True)
async def fd(ctx, char):
    """Command used when user asks for full framedata."""
    await sendFramedata(ctx, char, False)


@bot.command(pass_context=True)
async def fds(ctx, char):
    """Command used when user asks for simplified framedata."""
    await sendFramedata(ctx, char, True)


@bot.command(pass_context=True)
async def charnames(ctx):
    msg = "```"
    Globals.dbCursor.execute("select distinct charname from moves")
    q = Globals.dbCursor.fetchall()
    for row in q:
        msg = msg + row[0] + "\n"
    msg = msg + "```"

    await bot.send_message(ctx.message.author, msg)


@bot.command(pass_context=True)
async def aliases(ctx):
    msg = "```"
    Globals.dbCursor.execute("select key, value from aliases")
    q = Globals.dbCursor.fetchall()
    for row in q:
        msg = msg + row[0] + " --> " + row[1] + "\n"
    msg = msg + "```"

    await bot.send_message(ctx.message.author, msg)


@bot.command(pass_context=True)
async def alias(ctx):
    msg = ctx.message.content
    msg = msg.split(' ', 1)
    msg = msg[1]

    Globals.dbCursor.execute('select value from aliases where key=? collate nocase', (msg,))
    q = Globals.dbCursor.fetchone()

    if q:
        await bot.say(q[0])


@bot.command(pass_context=True)
async def removealias(ctx):
    author = ctx.message.author.id
    if author == prkid:
        msg = ctx.message.content
        msg = msg.split(' ', 1)
        msg = msg[1]
        Globals.dbCursor.execute('delete from aliases where key=? collate nocase', (msg,))
        Globals.dbConn.commit()
        await bot.say("Alias removed.")
    else:
        await bot.say("Insufficient permissions to remove aliases.")


@bot.command(pass_context=True)
async def atklevel(ctx):
    msg = ctx.message.content
    msg = msg.split(' ', 1)
    
    if len(msg) == 1:
        await bot.say("Please specify the attack level (e.g. .atklevel 3)")
        return

    Globals.dbCursor.execute('select * from levels where level=?', (msg[1],))
    q = Globals.dbCursor.fetchone()

    if not q:
        await bot.say("Level not found.")
        return

    await sendLevel(q)


@bot.command()
async def changes():
    await bot.say("http://www.justibairthrow.lol/eddie/changelog")


@bot.command(pass_context=True)
async def addalias(ctx):
    msg = ctx.message.content
    if not '|' in msg:
        await bot.say("Forgot to add '|'")
        return

    msg = ' '.join(msg.split()) #replace all whitespaces with a single one
    msg = msg.split(' ', 1)
    msg = msg[1]
    msg = msg.split('|')
    k = msg[0].lstrip().rstrip()
    v = msg[1].lstrip().rstrip()

    if not k:
        await bot.say("No alias")
        return
    if not v:
        await bot.say("No move to set alias to")
        return

    if DbReader.moveNameInDB(k, Globals.dbCursor):
        await bot.say("Can't set an alias to an actual move name.")
        return

    Globals.dbCursor.execute("select value from aliases where key=? collate nocase", (k,))
    q = Globals.dbCursor.fetchone()

    if not q:
        Globals.dbCursor.execute("insert into aliases values(?, ?)", (k.lower(), v.lower()))
        Globals.dbConn.commit()
        await bot.say('Alias has been successfully added.')
    else:
        await bot.say('Alias already exists.')


@bot.command()
async def help(*kw):
    """Display help."""
    if len(kw) == 0:
        await bot.say("```{0}```".format(helper.getHelptext()))
    else:
        await bot.say("```{0}```".format(helper.getHelptext(kw[0])))


##### Entry point
logging.basicConfig(level=logging.INFO)

prkid = "85484505023909888" #used to check if message is coming from admin
helper = Helper()
initDB('prkbotbase.db')
loadCharAliases('charalias.txt')
bot.run(getAuth('token.txt'))

