whitespace = [' ', '\t', '\n']
discow_prefix = "cow "

from discord import ServerRegion
import datetime
from pytz import timezone
import pytz
import itertools
import asyncio

def format_response(string, **kwargs):
    if "_msg" in kwargs:
        message = kwargs["_msg"]
        kwargs["_msgcontent"] = message.content
        kwargs["_author"] = message.author
    if "_author" in kwargs:
        author = kwargs["_author"]
        kwargs["_name"] = author.display_name
        kwargs["_username"] = author.name
        kwargs["_mention"] = author.mention

    return string.format(**kwargs)

def parse_command(msg, num=-1):
    cont = msg[len(discow_prefix):].split(" ")
    if num is not -1:
        if len(cont)<num+1:
            raise IndexError("Not enough inputs")
        else:
            return cont[:num]+[' '.join(cont[num:])]
    else:
        return cont

def strip_command(msg):
    return parse_command(msg, 1)[1]

def get_localized_time(serv):
    return convertTime(datetime.datetime.utcnow(), serv)

def convertTime(time, serv):
    timezones = {
    ServerRegion.us_west:"America/Los_Angeles",
    ServerRegion.us_east:"America/New_York",
    ServerRegion.us_central:"US/Central",
    ServerRegion.eu_west:"Europe/Amsterdam",
    ServerRegion.eu_central:"Europe/Berlin",
    ServerRegion.singapore:"Singapore",
    ServerRegion.london:"Europe/London",
    ServerRegion.sydney:"Australia/Sydney",
    ServerRegion.amsterdam:"Europe/Amsterdam",
    ServerRegion.frankfurt:"Europe/Berlin",
    ServerRegion.brazil:"Brazil/Acre",
    ServerRegion.vip_us_east:"America/New_York",
    ServerRegion.vip_us_west:"America/Los_Angeles",
    ServerRegion.vip_amsterdam:"Europe/Amsterdam"
    }
    zone = timezone(timezones[serv.region])
    time_naive = time.replace(tzinfo=pytz.utc)
    loctime = time_naive.astimezone(zone)
    fmt = '%Y-%m-%d at %H:%M:%S %Z'
    return loctime.strftime(fmt)

@asyncio.coroutine
def send_embed(Discow, msg, embed):
    myinfo = yield from Discow.application_info()
    me = yield from Discow.get_user_info(myinfo.id)
    txt = "Created by "+me.display_name+" on "+get_localized_time(msg.server)+"."
    embed.set_footer(text=txt, icon_url=myinfo.icon_url)
    m = yield from Discow.send_message(msg.channel, embed=embed)
    return m

@asyncio.coroutine
def edit_embed(Discow, msg, embed):
    myinfo = yield from Discow.application_info()
    me = yield from Discow.get_user_info(myinfo.id)
    txt = "Edited by "+me.display_name+" on "+get_localized_time(msg.server)+"."
    embed.set_footer(text=txt, icon_url=myinfo.icon_url)
    m = yield from Discow.edit_message(msg, embed=embed)
    return m

def group(lst, n):
  return list(zip(*[itertools.islice(lst, i, None, n) for i in range(n)]))

def isInteger(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class Question:
    def __init__(self, q, o):
        self.question = q
        self.options = o
    def isCorrect(self, option):
        return list(self.options.values())[option-1]
    def getstr(self, selected=None, showCorrect=False):
        if showCorrect:
            outstr = "```css\n{Question: '"+self.question+"'}"
        else:
            outstr = "```markdown\n# "+self.question
        for a in range(len(self.options)):
            if a == selected:
                if showCorrect:
                    outstr+="\n."+chr(a+65)+":  "
                    if self.isCorrect(a+1):
                        outstr+="("+list(self.options.keys())[a].center(49)+")"
                    else:
                        outstr+="["+list(self.options.keys())[a].center(49)+"]"
                else:
                    outstr+="\n<["+chr(a+65)+"]> ["+list(self.options.keys())[a].center(46)+"]()"
            else:
                if showCorrect:
                    outstr+="\n{"+chr(a+65)+":} "
                    if self.isCorrect(a+1):
                        outstr+="("+list(self.options.keys())[a].center(49)+")"
                    else:
                        outstr+="["+list(self.options.keys())[a].center(49)+"]"
                else:
                    outstr+="\n<<"+chr(a+65)+">> ["+list(self.options.keys())[a].center(46)+"]()"
        return outstr+'```'
