import asyncio
from discow.utils import *
from discow.handlers import *
from random import randint

@asyncio.coroutine
def hi(Discow, msg):
    yield from Discow.send_message(msg.channel, format_response("Hi **{_name}**, I'm Discow! Here's a tag: {_mention}", _msg = msg))

@asyncio.coroutine
def rps(Discow, msg):
    valid = ["rock", "paper", "scissors"]
    mine = valid[randint(0, 2)]
    yours = parse_command(msg.content, 1)[1]
    result = ""
    if mine == yours:
        result = "It's a tie!"
    else:
        comb = mine+yours
        if comb == "rockpaper" or "scissorsrock" or "paperscissors":
            result = format_response("{_mention} wins!", _msg=msg)
        else:
            result = "I win!"
    if yours in valid:
        yield from Discow.send_message(msg.channel, format_response("**{_mention}** chooses **{yours}**, while I choose **{mine}**. {result}", yours=yours, mine=mine, _msg = msg, result=result))
    else:
        yield from Discow.send_message(msg.channel, "Your input was invalid. Please choose **rock**, **paper**, or **scissors.**")

@asyncio.coroutine
def reaction(Discow, msg):
    num = int(parse_command(msg.content, 1)[1])
    msgs = yield from Discow.logs_from(msg.channel, limit=num)
    for m in msgs:
        for e in Discow.get_all_emojis():
            tmp = yield from Discow.add_reaction(m, e)

add_message_handler(hi, "hi")
add_message_handler(rps, "rps")
add_message_handler(reaction, "reaction")