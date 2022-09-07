import nextcord
from nextcord.ui import Button, View 
from nextcord.utils import get
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import wikipedia
import smtplib
import datetime
import webbrowser
import youtube_dl
import humanfriendly
import time
import random
import asyncio

intents=nextcord.Intents.default()
intents.members = True 
client = commands.Bot(command_prefix="*", help_command=None, intents=intents)

player1 = ""
player2 = ""
turn = ""
tic_time = 0
gameOver = True
GameOver = True
board = []
rps_p1 = ""
rps_p2 = ""
rps1 = ""
rps2 = ""
kli = 0

winningConditions = [
    [ 0, 1, 2],
    [ 3, 4, 5],
    [ 6, 7, 8],
    [ 0, 3, 6],
    [ 1, 4, 7],
    [ 2, 5, 8],
    [ 0, 4, 8],
    [ 2, 4, 6]
]

@client.command()
async def on_ready():
    print("Bot just landed on the server!")

@client.command()
async def on_error(error):
    print(error)
    
@client.command()
async def tictactoe(ctx, p1 : nextcord.Member, p2 : nextcord.Member ):
    global player1
    global player2
    global turn
    global gameOver
    global count
    global tic_time
    
    if gameOver and p1 != await client.fetch_user(949215188672974871) and p2 != await client.fetch_user(949215188672974871) :
        await tictactoeplay(ctx,p1,p2)
    else:
        await ctx.send("A game is already in progress! \n Finish it before starting a new one! \n You cannot play with the Bot itself!")       
        
async def tictactoeplay(ctx,p1,p2):        
        global player1
        global player2
        global turn
        global gameOver
        global count
        global tic_time
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0
        player1 = p1
        player2 = p2
        #print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]
                
        #determines who goes first!
        num =random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send(f"It is {player1.mention} turn!")
        elif num == 2:
            turn = player2
            await ctx.send(f"It is {player2.mention} turn!")
            
        #calculates time
        tic_time=0
        while True:
            if gameOver == False:
                await asyncio.sleep(1)
                tic_time+=1
            else:
                break
                   
@client.command()
async def place(ctx, pos : int):
    global turn
    global board
    global count
    global player1 
    global player2
    global gameOver
    global tic_time
    
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0<pos<10 and board[pos - 1] == ":white_large_square:":
                board[pos-1] = mark
                count+=1
                
                #print board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]
                
                checkWinner(winningConditions, mark)
                if gameOver == True:
                    await asyncio.sleep(2)
                    if mark == ":regional_indicator_x:":
                        myEmbed = nextcord.Embed(title="TICTACTOE❌⭕", description=f"{player1.mention} :regional_indicator_x: Wins the Game!", color=0xffff00)
                        myEmbed.add_field(name="Game Stats!", value=f"Time taken:{tic_time} seconds\n Total Moves:{count}",inline = True)
                        myEmbed.set_author(name="M1ke Bot#7179")
                        await ctx.send(embed=myEmbed)
                        await playagain(ctx)
                    elif mark == ":o2:":
                        myEmbed = nextcord.Embed(title="TICTACTOE❌⭕", description=f"{player2.mention} :o2: Wins the Game in just {count} moves!", color=0xffff00)
                        myEmbed.add_field(name="Game Stats!", value=f"Time taken:{tic_time} seconds\n Total Moves:{count}",inline = True)
                        myEmbed.set_author(name="M1ke Bot#7179")
                        await ctx.send(embed=myEmbed)
                        await playagain(ctx)
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")
                    await playagain(ctx)
                
                #switch turns
                if turn == player1: 
                    turn = player2
                elif turn == player2:
                    turn = player1
                
            else:
                await ctx.send("Be sure to change an integer between 1 and 9 and an unmarked tile!")
        else:
            await ctx.send("It is not you turn!")
    else:
        await ctx.send("Please start a new game!")

async def playagain(ctx):
    global player1
    global player2
    global kli
    kli=0
    button = Button(label="Yes", style = nextcord.ButtonStyle.green, emoji="👍")
    view = View(timeout=10)
    view.add_item(button)
    async def button_callback(interaction):
        global kli
        kli+=1
    button.callback = button_callback
    await ctx.send("Would like to play the game again with same player?",view=view)
    await asyncio.sleep(10)
    await check_rsp(ctx)

async def check_rsp(ctx):
    global kli
    global player1
    global player2
    if kli == 2:
        p1=player1
        p2=player2
        await tictactoeplay(ctx,p1,p2)
    else:
        await ctx.send("Game Request Rejected!")
        
@client.command()
async def clear(ctx):
    global player1
    global player2
    global gameOver
    if ctx.author == player1 or ctx.author == player2:
        num =random.randint(1, 2)
        if num == 1:
            await ctx.send(f"{player1.mention} Wins the Game By Random choice")
        else:
            await ctx.send(f"{player2.mention} Wins the Game By Random choice")
        gameOver = True
        await ctx.send("Game Over!")
    else:
        await ctx.send("You can only end the game played by you!")
            
def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@client.command()
async def rps(ctx, p1 : nextcord.Member, p2 : nextcord.Member):   
    global GameOver
    if GameOver and p1 != await client.fetch_user(949215188672974871) and p2 != await client.fetch_user(949215188672974871):
        global rps_p1
        global rps_p2
        global point1
        global point2
        GameOver = False
        point1 = 0
        point2 = 0
        rps_p1 = p1
        rps_p2 = p2
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description="🎮Rock, Paper, Scissor🎮", color=0xffff00)
        myEmbed.add_field(name="RULES:-" ,value=f"1.Press the button only once.\n2. {rps_p2.mention} should click the button after 2sec.\n3. Do not cry about cheating!\n4. The game is starting in 5 seconds. Maybe 2 by the time you read this!", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        time.sleep(6)
        await play(ctx)
    else:
        await ctx.send(f"A Game is already in progress between {p1.mention} and {p2.mention}!")
        
async def play(ctx):
    global rps_p1
    global rps_p2
    button = Button(label="Rock", style = nextcord.ButtonStyle.green, emoji="🥌")
    button2 = Button(label="Paper", style = nextcord.ButtonStyle.green, emoji="📰")
    button3 = Button(label="Scissor", style = nextcord.ButtonStyle.green, emoji="✂")
    view = View(timeout=100)
    view.add_item(button)
    view.add_item(button2)
    view.add_item(button3)
    async def button_callback(interaction):
        if interaction.user == rps_p1:
            abc = "stone"
            move1(ctx, abc)
            await asyncio.sleep(5)
            await match(ctx)
        elif interaction.user == rps_p2:
            ugh = "stone"
            move2(ctx, ugh)
    button.callback = button_callback
    async def button_callback(interaction):
        if interaction.user == rps_p1:
            abc = "paper"
            move1(ctx, abc)
            await asyncio.sleep(5)
            await match(ctx)
        elif interaction.user == rps_p2:
            ugh = "paper"
            move2(ctx, ugh)
    button2.callback = button_callback
    async def button_callback(interaction):
        if interaction.user == rps_p1:
            abc = "scissor"
            move1(ctx, abc)
            await asyncio.sleep(5)
            await match(ctx)
        elif interaction.user == rps_p2:
            ugh = "scissor"
            move2(ctx, ugh)
    button3.callback = button_callback
    await ctx.send(view=view)

def move1(ctx, abc):
    global rps1
    rps1 = abc

def move2(ctx, ugh):
    global rps2
    rps2 = ugh
    print(rps2)
    
async def match(ctx):
    global point1
    global point2
    global rps1
    global rps2
    global rps_p1
    global rps_p2
    print(rps2)
    print(rps1)
    if rps1 == "stone" and rps2 == "paper":
        point2 +=1
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Stone ⚔ Paper {rps_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = "" 
        rps2 = ""
        time.sleep(4)
        await pointcount(ctx)
    elif rps1 == "stone" and rps2 == "":
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} came victorious as {rps_p2.mention} failed to respond on time!", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "paper" and rps2 == "":
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} came victorious as {rps_p2.mention} failed to respond on time!", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "scissor" and rps2 == "":
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} came victorious as {rps_p2.mention} failed to respond on time!", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "stone" and rps2 == "scissor":
        point1 +=1
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Stone ⚔ Scissor {rps_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "stone" and rps2 == "stone":
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Stone ⚔ Stone {rps_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "paper" and rps2 == "paper":
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Paper ⚔ Paper {rps_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "paper" and rps2 == "stone":
        point1 +=1
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Paper ⚔ Stone {rps_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "paper" and rps2 == "scissor":
        point2+=1
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Paper ⚔ Scissor {rps_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "scissor" and rps2 == "stone":
        point2 +=1
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Scissor ⚔ Stone {rps_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "scissor" and rps2 == "paper":
        point1 +=1
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Scissor ⚔ Paper {rps_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
    elif rps1 == "scissor" and rps2 == "scissor":
        myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Scissor ⚔ Scissor {rps_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Points:", value=f"{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}", inline=True)
        myEmbed.set_author(name="M1ke Bot#7179")
        await ctx.send(embed=myEmbed)
        rps1 = ""
        rps2 = ""
        time.sleep(2)
        await pointcount(ctx)
 
async def pointcount(ctx):
    global point1
    global point2
    global rps_p1
    global rps_p2
    global point1
    global point2
    global GameOver
    if point1<5 and point2<5:
        await play(ctx)
    else:
        if point1==5:
            myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} beat the crap out of {rps_p2.mention}", color=0xffff00)
            myEmbed.add_field(name="Points:", value=f"💹{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}📉", inline=True)
            myEmbed.set_author(name="M1ke Bot#7179")
            await ctx.send(embed=myEmbed)
        else:
            myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p2.mention} beat the crap out of {rps_p1.mention}", color=0xffff00)
            myEmbed.add_field(name="Points:", value=f"📉{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}💹", inline=True)
            myEmbed.set_author(name="M1ke Bot#7179")
            await ctx.send(embed=myEmbed)
        GameOver = True
        
@client.command()
async def endgame(ctx):
    global rps_p1
    global rps_p2 
    global GameOver
    if GameOver:
        await ctx.send("No game is pending!\n You may start a new one!")
    else:
        if ctx.author == rps_p1 or ctx.author == rps_p2:
            num =random.randint(1, 2)
            if num == 1:
                myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p1.mention} Wins the Game by Random Choice!", color=0xffff00)
                myEmbed.set_author(name="M1ke Bot#7179")
                await ctx.send(embed=myEmbed)
            else:
                myEmbed = nextcord.Embed(title = "M1ke' Cult🐈", description=f"{rps_p2.mention} Wins the Game by Random Choice!", color=0xffff00)
                myEmbed.set_author(name="M1ke Bot#7179")
                await ctx.send(embed=myEmbed)
            GameOver = True
        else:
            await ctx.send(f"You can only end the game played by you!\nCurrently the game is being played between {rps_p1.mention} and {rps_p2.mention}")

@client.command()
async def help(ctx):
    myEmbed = nextcord.Embed(title = "Instructions for Games!", description=f"Follow these instructions correctly so that you enjoy the games!", color=0xffff00)
    myEmbed.add_field(name="For tictactoe...", value=f"1.**\*tictactoe [player1.mention] [player2.mention]** to start the game!\n2.**\*place [number1-9]** to place your mark!\n3.**\*clear** to end the game and the winner will be chosen randomly(This command can only be used by one of the players in the game.)",inline = False)
    myEmbed.add_field(name="For Rock-Paper-Scissor...", value=f"1.**\*rps [player1.mention] [player2.mention]** to start the game!\n2. Afterbuttons get displayed [player2.mention] should click the button immediately before [player1.mention].\n3. Both players should the button only once.\n4.**\*endgame **end the game and winner is chosen randomly. It can only be used by the mentioned players.\n5.", inline=False)
    myEmbed.set_author(name="M1ke Bot#7179")
    await ctx.send(embed=myEmbed)

@client.event
async def on_ready():
    print("Bot just landed on the server!")
  
@client.event
async def on_member_join(member):
    myEmbed = nextcord.Embed(title = "M1ke's Cult🐈", description="Welcome to the Server!", color=0xffff00)
    myEmbed.add_field(name="🤖" ,value = member.mention, inline=False)
    myEmbed.add_field(name="Description:-",value="The Offical Server of M1styM1ke on youtube", inline=False)
    myEmbed.set_footer(text="Explore outside while being inside \n #DISCORD😎")
    myEmbed.set_author(name="M1ke Bot#7179")
    chn = client.get_channel(883727293246234634)
    await chn.send(embed=myEmbed)
    
@client.event
async def on_member_remove(member):
    mem_rol = member.roles
    mem_id = member.id
    myEmbed = nextcord.Embed(title = "M1ke's Cult🐈", description=f"{member} has just left the server!", color=0xffff00)
    myEmbed.add_field(name= "ROLES:-" ,value=('\n'.join(map(str, mem_rol))), inline=False)
    myEmbed.add_field(name="❌",value="The above user with the concerned roles have left the server!", inline=False)
    myEmbed.set_author(name="M1ke Bot#7179")
    chn = client.get_channel(883727293246234634)
    await chn.send(embed=myEmbed)
    
@client.command()
async def private(ctx):
    myEmbed = nextcord.Embed(title = "M1ke's Cult🐈", description=f"Hello there {ctx.author.mention}\n In Private!", color=0xffff00)
    myEmbed.set_author(name="M1ke Bot#7179")
    await ctx.author.send(embed=myEmbed)
    
@client.command()
async def wiki(ctx,subject):
    mes_1 = await ctx.reply("Searching Google!")
    try:
        results = wikipedia.summary(subject, sentences = 10)
        await mes_1.edit(content="According to M1ke, "+results)
    except Exception as e:
        await mes_1.edit(content="Could not search what you were looking for!")
        
@client.command()
async def luckyroles(ctx, role_id :int):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=882402406804103168)#Owner Role
    if user_rol in user_give.roles:
        guild_mem = user_give.guild
        mem_list = []
        for member in guild_mem.members:
            mem_list.append(member)
            
        giveaway_mem = random.choice(mem_list)
        giv_role = get(user_give.guild.roles, id=role_id)
        await giveaway_mem.add_roles(giv_role)
        give_embed = nextcord.Embed(title="M1ke's Cult🐈", description = f"**{giveaway_mem.mention} \n You have just won the giveaway held by {ctx.author.mention}**\n You have got the *{giv_role.mention} !🎆🎊🎉*", color=0xffff00)
        await ctx.send(embed=give_embed)
        try:
            await giveaway_mem.send(embed=give_embed)
        except:
            await message.author.send("Cannot send message to the user who won the giveaway!")
            
client.run("*****BOT-TOKEN*****")
