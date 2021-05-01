from PIL import Image, ImageDraw, ImageFont

from utils import break_this, is_rightshare, parse_date, parse_miti


def generate(issues: list):

    def drow(text, size, fill, y, draw, x=None, **kwargs):
        font = ImageFont.truetype('media/regular.ttf', size)
        w, _ = draw.textsize(text, font)
        x = (template.width - w) / 2 if x is None else x
        return draw.text(xy=(x, y), font=font, text=text, fill=fill, **kwargs)

    for issue in issues:
        template = Image.open('media/t.png')
        draw = ImageDraw.Draw(template)

        drow(
            text=f"New Upcoming {issue.stock_type} Alert!",
            size=56,
            fill='#fea538',
            y=46,
            align="center",
            draw=draw,
        )

        drow(
            text=break_this(issue.company_name),
            size=78,
            fill='#ffffff',
            y=165,
            spacing=20,
            draw=draw,
            align="center"
        )

        drow(
            text=f"{parse_miti(issue.start_date)}\n{parse_date(issue.start_date)}",
            size=56,
            fill='#fea538',
            x=295,
            y=432,
            draw=draw,
            align="right"
        )

        drow(
            text=f"{parse_miti(issue.end_date)}\n{parse_date(issue.end_date)}",
            size=56,
            fill='#f25c74',
            x=585,
            y=432,
            draw=draw,
            align="left"
        )

        drow(
            text=is_rightshare(issue),
            size=42,
            fill='#141414',
            y=592,
            draw=draw,
            align="center"
        )

        drow(
            text=f"SCRIP: {issue.stock_symbol}, ISSUED BY {issue.issued_by}",
            size=38,
            fill='#ffffff',
            y=864,
            draw=draw,
            align="center"
        )

        template.save(f'{issue.stock_symbol.lower()}.png')
