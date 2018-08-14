# @Author: Edmund Lam <edl>
# @Date:   15:55:15, 12-Aug-2018
# @Filename: wolframalpha.py
# @Last modified by:   edl
# @Last modified time: 21:29:42, 13-Aug-2018

import asyncio
import os
import pyimgur
from discow.utils import *
from discow.handlers import add_message_handler
from discord import Embed
import wolframalpha
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import itertools

_wakey = "discow/client/data/keys/wolframalphakey.txt"
_imgurkey = "discow/client/data/keys/imgurkey.txt"
wa_app_id = None

if not os.path.exists(_wakey):
    print("Missing wolfram alpha key. Add one for wolfram alpha API integration.")
else:
    wa_app_id = open(_wakey, 'r').read().strip()

imgur_app_id = None

if not os.path.exists(_imgurkey):
    print("Missing wolfram alpha key. Add one for wolfram alpha API integration.")
else:
    imgur_app_id = open(_imgurkey, 'r').read().strip()

wa_client = wolframalpha.Client(wa_app_id)
imgur_client = pyimgur.Imgur(imgur_app_id)

async def query(Discow, msg):

    question = strip_command(msg.content)
    em = Embed(title=question, description="Requesting Data", colour=0xe4671b)
    oldem = await send_embed(Discow, msg, em)
    res = wa_client.query(question)


    titles = []
    images = []

    for pod in res.pods:
        titles.append(pod.title)
        subimgs = []
        for sub in pod.subpods:
            subimgs.append(Image.open(BytesIO(requests.get(sub['img']['@src']).content)))
        images.append(subimgs)

    chained_imgs = list(itertools.chain.from_iterable(images))




    widths, heights = zip(*(i.size for i in chained_imgs))

    item_padding = 20
    font_size = 20


    max_width = max(widths)+2*item_padding
    total_height = sum(heights)+item_padding*(len(chained_imgs)+2)+(item_padding+font_size)*len(titles)

    new_im = round_rectangle((max_width, total_height), item_padding, "white")

    font = ImageFont.truetype("discow/client/data/Roboto-Regular.ttf", font_size)

    total_pods = 0

    draw = ImageDraw.Draw(new_im)
    y_offset = item_padding
    for i in range(len(titles)):
        pod = images[i]
        draw.text((item_padding*1.5, y_offset), titles[i], fill=(119, 165, 182), font=font)

        y_offset+=item_padding+font_size
        for im in pod:
            total_pods+=1
            new_im.paste(im, (item_padding,y_offset))
            y_offset += im.size[1]+item_padding
            if(total_pods < len(chained_imgs)):
                draw.line((0,y_offset-item_padding/2,max_width,y_offset-item_padding/2),fill=(233,233,233),width=1)


    new_im.save("discow/client/data/wa_save.png")

    res_img = imgur_client.upload_image("discow/client/data/wa_save.png", title=question)

    em = Embed(title=question, colour = 0xe4671b)
    em.set_image(url=res_img.link)
    await edit_embed(Discow, oldem, em)

add_message_handler(query, "wolfram")
add_message_handler(query, "wolframalpha")
add_message_handler(query, "wa")