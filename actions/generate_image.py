from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont

from utils import (Stock, break_this, humanize_number, parse_date, parse_miti,
                   store)


def generate(issue: Stock):
    """Generate images based on the issue provided

    Args:
        issue (Stock): issue to be generated

    Returns:
        [BufferedReader]: generates readable image in bytes format supported by the `multipart/form-data`
    """
    from utils.const import current_dir

    def drow(text: str, size: int, fill: str, y: int, draw, x: int = None, **kwargs):
        # takes care of having to type all these defaults and variable font sizes
        font = ImageFont.truetype('media/regular.ttf', size)
        w, _ = draw.textsize(text, font)
        x = (template.width - w) / 2 if x is None else x
        return draw.text(xy=(x, y), font=font, text=text, fill=fill, **kwargs)

    template = Image.open('media/template.png')
    draw = ImageDraw.Draw(template)

    drow(
        text="New Upcoming IPO Alert!",
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
        text=f"{parse_miti(issue.opening_date)}",
        size=56,
        fill='#fea538',
        x=295,
        y=432,
        draw=draw
    )

    drow(
        text=f"{parse_date(issue.opening_date)}",
        size=56,
        fill='#fea538',
        x=295,
        y=485,
        draw=draw
    )

    drow(
        text=f"{parse_miti(issue.closing_date)}",
        size=56,
        fill='#f25c74',
        x=615,
        y=432,
        draw=draw
    )

    drow(
        text=f"{parse_date(issue.closing_date)}",
        size=56,
        fill='#f25c74',
        x=615,
        y=485,
        draw=draw
    )

    drow(
        text=f"Total Units: {humanize_number(issue.units)}",
        size=42,
        fill='#141414',
        y=592,
        draw=draw,
        align="center"
    )

    drow(
        text=f"Scrip: {issue.stock_symbol} · Issued By {issue.share_registrar}",
        size=38,
        fill='#ffffff',
        y=864,
        draw=draw,
        align="center"
    )

    file_name = str(uuid4())[:8]
    image_name = f'{file_name}.PNG'
    store.image_name = image_name
    the_image = current_dir / image_name
    template.save(image_name)
    return open(the_image, 'rb')
