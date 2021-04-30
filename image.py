from PIL.Image import open
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

from utils import is_rightshare, parse_date, parse_miti

template = open('media/t.png')


def drow(text, size, fill, y, x=None, **kwargs):
    font = truetype('media/regular.ttf', size)
    draw = Draw(template)
    w, _ = draw.textsize(text, font)
    x = (template.width - w) / 2 if x is None else x
    draw.text(xy=(x, y),
              font=font, text=text, fill=fill, **kwargs)


def fix(given_text):
    text = given_text.split()
    for i in range(0, len(text), 3):
        if i != 0:
            text[i-1] = f"{text[i-1]}\n"
    return ' '.join(text)


def gen_image(issue):
    title = drow(f"New Upcoming {issue.stock_type} Alert!",
                 56, '#fea538', 46, align="center")
    name = drow(fix(issue.company_name),
                78, '#ffffff', 165, spacing=20, align="center")
    opening_date = drow(f"{parse_miti(issue.start_date)}\n{parse_date(issue.start_date)}",
                        size=56, fill='#fea538', x=295, y=432, align="right")
    closing_date = drow(f"{parse_miti(issue.end_date)} / {parse_date(issue.end_date)}",
                        size=56, fill='#f25c74', x=585, y=432, align="left")
    units = drow(is_rightshare(issue),
                 size=42, fill='#141414', y=592, align="center")
    issued = drow(f"SCRIP: {issue.stock_symbol}, ISSUED BY {issue.issued_by}",
                  size=38, fill='#ffffff', y=864, align="center")
    template.save(f'{issue.stock_symbol.lower()}.png')
