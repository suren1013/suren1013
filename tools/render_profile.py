"""Compose original editorial panels around genuine project captures and 3D art."""
import json
import math
import subprocess
import sys
import textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
INK,PAPER,MUTED,RED='#111214','#e5e1d8','#aeaea7','#ca5148'
SELECTED=set(sys.argv[1:])
def font(size,title=False,bold=False):
    name='impact.ttf' if title else ('arialbd.ttf' if bold else 'arial.ttf')
    return ImageFont.truetype('C:/Windows/Fonts/'+name,size)
def text(draw,x,y,value,size=22,color=PAPER,title=False,bold=False):
    draw.text((x,y),value,font=font(size,title,bold),fill=color)
def wrap(draw,value,x,y,width,size=23,color=PAPER,gap=9):
    words=value.split();line='';lines=[]
    f=font(size)
    for word in words:
        trial=(line+' '+word).strip()
        if draw.textlength(trial,font=f)>width and line: lines.append(line);line=word
        else:line=trial
    if line:lines.append(line)
    for line in lines:
        text(draw,x,y,line,size,color);y+=size+gap
    return y
def panel(height,tag,title):
    im=Image.new('RGB',(1200,height),INK);d=ImageDraw.Draw(im)
    d.rectangle((0,0,6,height),fill=RED)
    text(d,40,25,tag,15,MUTED,bold=True)
    text(d,40,65,title,60,title=True)
    return im,d
def paste_contain(im,name,box):
    src=Image.open(ASSETS/name).convert('RGB')
    x,y,w,h=box;pic=ImageOps.contain(src,(w,h),Image.Resampling.LANCZOS)
    im.paste(pic,(x+(w-pic.width)//2,y+(h-pic.height)//2))
def finish(name,im,phase=0):
    if SELECTED and name not in SELECTED:
        return
    d=ImageDraw.Draw(im);h=im.height
    d.rectangle((40,h-31,1160,h-30),fill='#343638')
    still=im.copy();ImageDraw.Draw(still).rectangle((40,h-33,155,h-29),fill=RED)
    still.save(ASSETS/(name+'.png'),optimize=True)
    # Reuse a fixed palette: typography and photos cannot flicker between frames.
    sample=still.quantize(colors=256)
    frames=[]
    for frame in range(240):
        current=im.copy();d=ImageDraw.Draw(current)
        x=40+1005*(1-math.cos(math.tau*(frame/240+phase)))/2
        d.rectangle((int(x),h-33,int(x)+115,h-29),fill=RED)
        frames.append(current.quantize(palette=sample,dither=Image.Dither.NONE))
    frames[0].save(ASSETS/(name+'.gif'),save_all=True,append_images=frames[1:],duration=50,loop=0,optimize=True,disposal=1)
    print('Rendered',name)

im,d=panel(590,'01 / PERSONAL DOSSIER','SURENDHER_R')
paste_contain(im,'dossier-emblem.png',(35,145,450,380))
text(d,515,158,'MECHANICAL ENGINEERING / COMPUTATION',17,RED,bold=True)
rows=[('PRACTICE','Physical problems into models, simulations, and useful tools.'),('CURRENT STUDY','Forced-air cooling for avionics heat sinks.'),('LEARNING','OpenFOAM, numerical methods, and better engineering code.'),('AVAILABLE FOR','Internships and collaborations.')]
y=204
for label,value in rows:
    text(d,515,y,label,14,MUTED,bold=True)
    y=wrap(d,value,515,y+23,610,24)+18
finish('dossier',im,0)

projects=[
('casting','01 / PROJECT FILE / ENGINEERING SOFTWARE','CASTING ASSISTANT','casting-viewport.png',[('06','ALLOYS'),('3D','RISER SCHEMATIC'),('MODULUS','YIELD / FEEDING / RISK')],'TYPESCRIPT / REACT / REACT THREE FIBER','REAL INTERFACE / LOCAL DEFAULT EXAMPLE'),
('clv','02 / PROJECT FILE / CUSTOMER ANALYTICS','CUSTOMER CLV DASHBOARD','clv-interface.png',[('10','CLEANING STEPS'),('12','CUSTOMER METRICS'),('07','RFM SEGMENTS')],'PYTHON / STREAMLIT / PANDAS / PLOTLY','REAL INTERFACE / BUNDLED PUBLIC DEMO DATA'),
('election','03 / PROJECT FILE / LIVE SYSTEMS','TN ELECTION LIVE','election-interface.png',[('234','CONSTITUENCIES'),('60s','REFRESH INTERVAL'),('LIVE','MAJORITY TRACKING')],'TYPESCRIPT / REACT / GOOGLE CLOUD RUN','REAL INTERFACE / DEPLOYED APPLICATION / CAPTURED 2026-10-04')]
for i,(name,tag,title,image,metrics,stack,note) in enumerate(projects):
    if not (ASSETS/image).exists(): raise RuntimeError('Missing genuine screenshot: '+image)
    im,d=panel(830,tag,title)
    d.rectangle((40,154,1160,625),fill='#090a0b',outline='#343638',width=1)
    paste_contain(im,image,(41,155,1118,469))
    text(d,40,643,note,14,MUTED,bold=True)
    for j,(value,label) in enumerate(metrics):
        x=40+j*380;text(d,x,677,value,40,RED,title=True);text(d,x,724,label,14,MUTED,bold=True)
    text(d,40,767,stack,15,PAPER,bold=True)
    finish(name+'-evidence',im,0.11+i*0.13)

im,d=panel(680,'03 / RESEARCH SPOTLIGHT / THERMAL ENGINEERING','THE PHYSICS COMES FIRST.')
paste_contain(im,'heat-sink-concept.png',(20,145,655,465))
text(d,704,169,'AVIONICS / FORCED-AIR COOLING',19,RED,bold=True)
y=wrap(d,'How can a physical cooling problem become a useful computational model?',704,214,450,27)
text(d,704,y+25,'CURRENT FOCUS',14,MUTED,bold=True)
y=wrap(d,'Heat transfer, forced-air cooling, and OpenFOAM-based CFD.',704,y+50,440,24)
text(d,704,y+22,'LOOKING AHEAD',14,MUTED,bold=True)
wrap(d,'Thermal management, fluid mechanics, structures, and space systems.',704,y+47,440,23)
text(d,40,620,'CONCEPTUAL GEOMETRY / ORIGINAL 3D ILLUSTRATION / NO SIMULATION RESULTS SHOWN',14,MUTED,bold=True)
finish('research-spotlight',im,0.55)

im,d=panel(675,'04 / METHOD & TOOLS / AN ENGINEERING WORKFLOW','QUESTION. MODEL. BUILD.')
stages=[('01','QUESTION','Define the system.'),('02','MODEL','State assumptions.'),('03','SIMULATE','Explore behaviour.'),('04','VALIDATE','Check the result.'),('05','BUILD','Learn and refine.')]
for i,(number,title,line) in enumerate(stages):
    x=40+i*227;d.rectangle((x,156,x+208,292),fill='#252628')
    d.rectangle((x,156,x+208,158),fill=RED)
    text(d,x+15,175,number,29,RED,title=True);text(d,x+15,218,title,24,title=True)
    text(d,x+15,261,line,17,MUTED)
text(d,40,328,'ENGINEERING + CODE + TOOLS',17,MUTED,bold=True)
cols=[('ENGINEERING',['OpenFOAM / ANSYS / SolidWorks','CFD / FEA / Heat Transfer']),('CODE',['Python / TypeScript / JavaScript','React / Next.js / Java']),('TOOLS',['Git / GitHub / VS Code','LangChain'])]
for i,(title,lines) in enumerate(cols):
    x=40+i*380;text(d,x,378,title,29,RED,title=True)
    for j,line in enumerate(lines):text(d,x,426+j*36,line,20)
wrap(d,'Make assumptions visible. Build the smallest useful version. Validate it, then improve the model.',40,534,1080,25)
finish('method-board',im,0.71)

im,d=panel(360,'06 / OPEN TO INTERNSHIPS & COLLABORATIONS',"LET'S BUILD SOMETHING USEFUL.")
wrap(d,'Thermal engineering / CFD / engineering software / applied AI',40,172,1090,27)
text(d,40,248,'START WITH THE PROBLEM, THE INPUTS, AND THE OUTCOME YOU WANT TO REACH.',17,MUTED,bold=True)
finish('contact-board',im,0.86)
