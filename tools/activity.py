"""Validate GitHub's public contribution calendar and render a local landscape."""
import argparse
import io
import json
import os
import re
import tempfile
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont

IST = timezone(timedelta(hours=5, minutes=30))
INK, PAPER, MUTED, RED = '#111214', '#e5e1d8', '#aeaea7', '#ca5148'
OUTPUTS = ('activity-data.json', 'activity-landscape.png', 'activity-summary.md', 'activity-landscape-mobile.png')

def font(size, bold=False):
    candidates = ([Path('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf')]
                  + [Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')])
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    raise RuntimeError('Install Arial or fonts-dejavu-core; readable labels are required.')

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.cells = []
        self.tips = {}
        self.tip_id = None
        self.tip_parts = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a:
            self.cells.append(a)
        if tag == 'tool-tip':
            self.tip_id, self.tip_parts = a.get('for'), []

    def handle_data(self, data):
        if self.tip_id:
            self.tip_parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.tip_id:
            if self.tip_id in self.tips:
                raise ValueError('Duplicate contribution tooltip')
            self.tips[self.tip_id] = ''.join(self.tip_parts).strip()
            self.tip_id = None

def parse_calendar(html, today):
    parser = CalendarParser()
    parser.feed(html)
    if not 300 <= len(parser.cells) <= 400:
        raise ValueError('Incomplete or unexpected public calendar')
    days, seen = [], set()
    for cell in parser.cells:
        day = date.fromisoformat(cell['data-date'])
        if day in seen:
            raise ValueError('Duplicate calendar date')
        seen.add(day)
        level = int(cell.get('data-level', '-1'))
        if level not in range(5):
            raise ValueError('Unexpected contribution intensity')
        tip = parser.tips.get(cell.get('id'))
        match = re.match(r'^(No|[\d,]+) contributions? on\b', tip or '')
        if not match:
            raise ValueError('Missing or malformed contribution count tooltip')
        count = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
        if not 0 <= count <= 100000 or (level == 0) != (count == 0):
            raise ValueError('Count and intensity disagree')
        if day <= today:
            days.append({'date': day.isoformat(), 'count': count, 'level': level})
    days.sort(key=lambda x: x['date'])
    if not 300 <= len(days) <= 400:
        raise ValueError('Insufficient dated contribution data')
    for before, after in zip(days, days[1:]):
        if date.fromisoformat(after['date']) - date.fromisoformat(before['date']) != timedelta(days=1):
            raise ValueError('Calendar dates are not contiguous')
    if (today - date.fromisoformat(days[-1]['date'])).days > 14:
        raise ValueError('Public calendar is stale; retain previous artwork')
    return days

def fetch_calendar(username):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,38}', username):
        raise ValueError('Invalid GitHub username')
    req = Request(f'https://github.com/users/{username}/contributions', headers={
        'User-Agent': 'ControlProfileActivity/1.0', 'Accept': 'text/html', 'Accept-Language': 'en-US'})
    with urlopen(req, timeout=30) as response:
        body = response.read(4_000_001)
    if len(body) > 4_000_000:
        raise ValueError('Unexpected calendar response size')
    return body.decode('utf8')

def render_landscape(data):
    # Supersampling gives crisp physical faces and stable typography at README scale.
    scale, width, height = 2, 1200, 660
    image = Image.new('RGB', (width*scale, height*scale), INK)
    draw = ImageDraw.Draw(image)
    def text(x, y, value, size=18, color=PAPER, bold=False):
        draw.text((x*scale,y*scale), value, font=font(size*scale,bold), fill=color)
    def poly(points, fill, outline=None):
        draw.polygon([(int(x*scale),int(y*scale)) for x,y in points], fill=fill, outline=outline)
    text(40,25,'PUBLIC ACTIVITY / A CONCRETE RECORD',15,MUTED,True)
    text(40,63,'THE WORK ACCUMULATES.',43,PAPER,True)
    for x, value, label in [(40,str(data['total']),'PUBLIC CONTRIBUTIONS'),(400,str(data['active_days']),'ACTIVE DAYS'),(745,data['range_end'],'LATEST CALENDAR DAY')]:
        text(x,137,value,32,RED,True)
        text(x,180,label,13,MUTED,True)
    start = date.fromisoformat(data['range_start'])
    start -= timedelta(days=(start.weekday()+1)%7)
    tiles=[]
    # Seven weekdays recede diagonally; chronological weeks advance to the right.
    for item in data['days']:
        offset=(date.fromisoformat(item['date'])-start).days
        week,weekday=divmod(offset,7)
        x=100+week*18+weekday*12
        y=395+weekday*7-week*1.5
        h=3+item['level']*17
        tiles.append((y,x,weekday,h,item))
    faces=[('#242629','#1b1d20','#303235'),('#5c5550','#3c3936','#877d72'),('#786b5f','#4e453e','#b1a08d'),('#934e44','#613b34','#c87360'),('#b85e50','#7a3c35','#e39476')]
    for y,x,weekday,h,item in sorted(tiles):
        left,right,top=faces[item['level']]
        a,b,c,d=(x,y-h),(x+10,y-h-5),(x+20,y-h),(x+10,y-h+5)
        poly([a,d,(x+10,y+5),(x,y)],left,'#17181a')
        poly([d,c,(x+20,y),(x+10,y+5)],right,'#17181a')
        poly([a,b,c,d],top,'#17181a')
    seen_months=set()
    for item in data['days']:
        day=date.fromisoformat(item['date'])
        key=(day.year,day.month)
        if key not in seen_months:
            seen_months.add(key)
            # Skip a short leading partial month to avoid overlapping labels.
            if day==date.fromisoformat(data['range_start']) and (day+timedelta(days=5)).month!=day.month:
                continue
            week=(day-start).days//7
            text(98+week*18,460-week*1.5,day.strftime('%b').upper(),12,MUTED)
    text(40,528,f"{data['range_start']}  —  {data['range_end']}",16,PAPER)
    text(40,559,'ONE COLUMN / ONE DAY. HEIGHT AND COLOUR / GITHUB INTENSITY LEVEL.',13,MUTED)
    text(40,594,f"REFRESHED {data['refreshed_on']} IST / PUBLIC CALENDAR ONLY",13,MUTED)
    text(810,529,'LESS',12,MUTED)
    for level in range(5):
        x=858+level*28
        draw.rectangle((x*scale,531*scale,(x+20)*scale,551*scale),fill=faces[level][2])
    text(1008,529,'MORE',12,MUTED)
    draw.rectangle((40*scale,631*scale,1160*scale,632*scale),fill='#343638')
    draw.rectangle((40*scale,630*scale,160*scale,633*scale),fill=RED)
    out=io.BytesIO()
    image.resize((width,height),Image.Resampling.LANCZOS).save(out,format='PNG',optimize=True)
    return out.getvalue()

def update(username, output_dir, *, fetcher=fetch_calendar, today=None):
    today = today or datetime.now(IST).date()
    days = parse_calendar(fetcher(username),today)
    data={'username':username,'source':f'https://github.com/users/{username}/contributions',
          'refreshed_on':today.isoformat(),'timezone':'Asia/Calcutta','range_start':days[0]['date'],
          'range_end':days[-1]['date'],'total':sum(x['count'] for x in days),
          'active_days':sum(x['count']>0 for x in days),'days':days}
    png=render_landscape(data)  # All fetch/parse/render work precedes any replacement.
    summary=(f"Public contribution calendar for **{username}**: **{data['total']} contributions**, "
             f"**{data['active_days']} active days**, {data['range_start']} through {data['range_end']}. "
             f"Refreshed {data['refreshed_on']} IST. Heights represent GitHub's intensity levels; "
             "this is activity context, not a measure of engineering quality.\n")
    mobile=render_mobile_landscape(data,png)
    payloads=(json.dumps(data,indent=2).encode()+b'\n',png,summary.encode(),mobile)
    output_dir=Path(output_dir)
    output_dir.mkdir(parents=True,exist_ok=True)
    staged=[]
    try:
        for name,payload in zip(OUTPUTS,payloads):
            with tempfile.NamedTemporaryFile(dir=output_dir,delete=False) as file:
                file.write(payload)
                staged.append((Path(file.name),output_dir/name))
        for temporary,target in staged:
            os.replace(temporary,target)
    finally:
        for temporary,_ in staged:
            temporary.unlink(missing_ok=True)
    return data

def render_mobile_landscape(data,png):
    image=Image.new('RGB',(600,655),INK);draw=ImageDraw.Draw(image)
    def text(x,y,value,size=22,color=PAPER,bold=False):draw.text((x,y),value,font=font(size,bold),fill=color)
    text(28,22,'05 / PUBLIC ACTIVITY',19,MUTED,True)
    text(28,66,'THE WORK',39,PAPER,True)
    text(28,114,'ACCUMULATES.',39,PAPER,True)
    text(28,185,str(data['total']),45,RED,True);text(295,185,str(data['active_days']),45,RED,True)
    text(28,239,'VISIBLE CONTRIBUTIONS',17,MUTED,True);text(295,239,'ACTIVE DAYS',17,MUTED,True)
    chart=Image.open(io.BytesIO(png)).crop((80,220,1140,490)).resize((544,139),Image.Resampling.LANCZOS)
    image.paste(chart,(28,284))
    text(28,439,f"{data['range_start']} — {data['range_end']}",23)
    text(28,484,'ONE COLUMN / ONE DAY',20,MUTED,True)
    text(28,519,'HEIGHT / GITHUB INTENSITY LEVEL',18,MUTED)
    text(28,550,'LESS',15,MUTED)
    for level,color in enumerate(('#303235','#877d72','#b1a08d','#c87360','#e39476')):
        draw.rectangle((82+level*28,551,102+level*28,569),fill=color)
    text(230,550,'MORE',15,MUTED)
    text(28,590,f"REFRESHED {data['refreshed_on']} IST",19,MUTED,True)
    draw.rectangle((28,624,572,625),fill='#343638');draw.rectangle((28,622,110,626),fill=RED)
    buffer=io.BytesIO();image.save(buffer,format='PNG',optimize=True);return buffer.getvalue()

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--username',default='suren1013')
    parser.add_argument('--output-dir',default='assets')
    args=parser.parse_args()
    data=update(args.username,args.output_dir)
    print(f"Validated {len(data['days'])} days / {data['total']} contributions / {data['active_days']} active days")
