from PIL import Image
import requests
import numpy
import math
import discord
import os
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']

gscale1 = "`^\",:;Il!i~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
gscale2 = ".:-=+*#%@"
gscale3 = " ░▒▓"
rgscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`"
rgscale2 = "@%#*+=-:."
rgscale3 = "▓▒░ "

#cols should be updated later to ask for user input
artCols = 100

def getAverageL(image):
    im = numpy.array(image)
    w,h = im.shape
    return numpy.average(im.reshape(w*h))

def covertImageToAscii(image, cols, scale, charSet):
    #  saves the length of the gscale charset for optimization
    charSet_len = len(charSet)-1

    # store dimensions
    W, H = image.size[0], image.size[1]
    print("input image dims: %d x %d" % (W, H))
  
    # compute width of tile
    w = W/cols
  
    # compute tile height based on aspect ratio and scale
    h = w/scale
  
    # compute number of rows
    rows = int(H/h)
      
    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))
  
    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)
  
    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
  
        # correct last tile
        if j == rows-1:
            y2 = H
  
        # append an empty string
        aimg.append("")
  
        for i in range(cols):
  
            # crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
  
            # correct last tile
            if i == cols-1:
                x2 = W
  
            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))
  
            # get average luminance
            avg = int(getAverageL(img))
  
            # look up ascii char
            gsval = charSet[int((avg*charSet_len)/255)]

  
            # append ascii char to string
            aimg[j] += gsval + gsval
      
    # return txt image
    return aimg


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if  message.content.startswith('$ascii'):
        if message.content.startswith('$ascii help'):
            embedVar = discord.Embed(title="ASCII Bot Help", description="To convert a photo to ASCII symbols use the \"$ascii art\" command in the following format:\n$ascii art <number of coloumns> <style> <source URL>\n\nUse \"$ascii styles\" to discover different character sets", color=0xF0FFFF)
            await message.channel.send("", embed=embedVar)

        elif message.content.startswith('$ascii styles'):
            embedVar = discord.Embed(title="Styles Menu", description="**gscale1:**\n \"`^\",:;Il!i~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao\*#MW&8%B@$\"\n**gscale2:**\n \".:-=+\*#%@\"\n**gscale3:**\n \" ░▒▓\"", color=0xF0FFFF)
            await message.channel.send("", embed=embedVar)

        elif message.content.startswith('$ascii art '):
            try:
                #command format: $ascii art colnum style url
                command = message.content.split()
                style = gscale3
                if (command[3] == "gscale1"):
                    style = gscale1
                elif (command[3] == "gscale2"):
                    style = gscale2
                elif (command[3] == "gscale3"):
                    style = gscale3
                elif (command[3] == "rgscale1"):
                    style = rgscale1
                elif (command[3] == "rgscale2"):
                    style = rgscale2
                elif (command[3] == "rgscale3"):
                    style = rgscale3
                else:
                    embedVar = discord.Embed(title="ERROR: Invalid Style", description="ASCII Bot could not find the character set you were looking for. Try using \"$ascii style\" to find available character sets.",color=0xF0FFFF)
                    await message.channel.send("", embed=embedVar)
                    return

                # gets the photo from a url and turns it grayscale
                im = Image.open(requests.get(command[4], stream=True).raw).convert("L")

                #stores dimensions of picture
                width, height = im.size[0], im.size[1]

                #finding aspect ratio
                imgScale = width/height

                #making a list of strings for each row in the art
                textImg = covertImageToAscii(im,int(command[2]),imgScale,style)

                # open file
                with open("art.txt", 'w',encoding="utf-8") as f:
                    # write to file
                    for row in textImg:
                        f.write(row + "\n")

                # cleanup
                f.close()
                file = discord.File("art.txt", filename="art.txt")

                await message.channel.send(file=file)
            except:
                await message.channel.send("Formatting Error: make sure you are following the proper format of the art command. For more information use the \"$ascii help\" command")

        else: 
            embedVar = discord.Embed(title="Command ERROR", description="Make sure you are using an ASCII Bot command. For more information on ASCII Bot commands use \"$ascii help\"", color=0xF0FFFF)
            await message.channel.send("", embed=embedVar)

#keeps the bot up 24/7
keep_alive()
client.run(my_secret)
