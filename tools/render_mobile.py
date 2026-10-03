"""Compact stationary layouts for narrow GitHub README viewports."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets'
INK,PAPER,MUTED,RED='#111214','#e5e1d8','#aeaea7','#ca5148'
def font(size,title=False,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('impact.ttf' if title else 'arialbd.ttf' if bold else 'arial.ttf'),size)
def text(d,x,y,s,size=26,color=PAPER,title=False,bold=False):d.text((x,y),s,font=font(size,title,bold),fill=color)
def wrap(d,s,x,y,w=540,size=28,color=PAPER):
    f=font(size);line='';lines=[]
    for word in s.split():
        trial=(line+' '+word).strip()
        if d.textlength(trial,font=f)>w and line:lines.append(line);line=word
        else:line=trial
    if line:lines.append(line)
    for line in lines:text(d,x,y,line,size,color);y+=size+10
    return y
def start(h,tag,lines):
    im=Image.new('RGB',(600,h),INK);d=ImageDraw.Draw(im);d.rectangle((0,0,5,h),fill=RED)
    text(d,28,22,tag,19,MUTED,bold=True)
    for i,line in enumerate(lines):text(d,28,62+i*58,line,49,title=True)
    return im,d
def photo(im,name,box):
    x,y,w,h=box;pic=ImageOps.contain(Image.open(A/name).convert('RGB'),(w,h),Image.Resampling.LANCZOS)
    im.paste(pic,(x+(w-pic.width)//2,y+(h-pic.height)//2))
def save(name,im):
    d=ImageDraw.Draw(im);d.rectangle((28,im.height-31,572,im.height-30),fill='#343638');d.rectangle((28,im.height-33,110,im.height-29),fill=RED)
    im.save(A/(name+'-mobile.png'),optimize=True)

im,d=start(1110,'01 / PERSONAL DOSSIER',['SURENDHER_R'])
photo(im,'dossier-emblem.png',(28,130,544,345))
y=508
for label,value in [('PRACTICE','Mechanical engineering and computation.'),('CURRENT STUDY','Forced-air cooling for avionics heat sinks.'),('LEARNING','OpenFOAM, numerical methods, and better engineering code.'),('AVAILABLE FOR','Internships and collaborations.')]:
    text(d,28,y,label,20,RED,bold=True);y=wrap(d,value,28,y+33)+27
save('dossier',im)

for name,lines,metrics,stack in [
('casting',['CASTING ASSISTANT'],['06 ALLOYS / 3D RISER SCHEMATIC','MODULUS / YIELD / FEEDING / RISK'],'TypeScript / React / React Three Fiber'),
('clv',['CUSTOMER CLV','DASHBOARD'],['10 CLEANING STEPS / 12 METRICS','07 RFM SEGMENTS'],'Python / Streamlit / Pandas / Plotly'),
('election',['TN ELECTION LIVE'],['234 CONSTITUENCIES / 60s REFRESH','LIVE MAJORITY TRACKING'],'TypeScript / React / Google Cloud Run')]:
    im,d=start(870,'PROJECT FILE / REAL INTERFACE',lines)
    top=190 if len(lines)>1 else 150
    preview='casting-viewport.png' if name=='casting' else name+'-interface.png'
    photo(im,preview,(28,top,544,370))
    y=top+398
    for value in metrics:text(d,28,y,value,23,RED,bold=True);y+=42
    wrap(d,stack,28,y+16,size=25)
    text(d,28,805,'FULL CAPTURE LINK BELOW THE PANEL',18,MUTED,bold=True)
    save(name+'-evidence',im)

im,d=start(1170,'03 / RESEARCH SPOTLIGHT',['THE PHYSICS','COMES FIRST.'])
photo(im,'heat-sink-concept.png',(28,195,544,395))
text(d,28,627,'AVIONICS / FORCED-AIR COOLING',23,RED,bold=True)
y=wrap(d,'How can a physical cooling problem become a useful computational model?',28,675,size=30)
text(d,28,y+22,'CURRENT FOCUS',20,MUTED,bold=True)
y=wrap(d,'Heat transfer, forced-air cooling, and OpenFOAM-based CFD.',28,y+55,size=28)
wrap(d,'Conceptual geometry. Artistic lighting. No simulation results shown.',28,y+32,size=25,color=MUTED)
save('research-spotlight',im)

im,d=start(1310,'04 / METHOD & TOOLS',['QUESTION. MODEL. BUILD.'])
y=149
for n,title,line in [('01','QUESTION','Define the system.'),('02','MODEL','State assumptions.'),('03','SIMULATE','Explore behaviour.'),('04','VALIDATE','Check the result.'),('05','BUILD','Learn and refine.')]:
    d.rectangle((28,y,572,y+82),fill='#252628');text(d,42,y+19,n,32,RED,title=True)
    text(d,113,y+10,title,29,title=True);text(d,113,y+47,line,25,MUTED);y+=98
y+=18
for title,value in [('ENGINEERING','OpenFOAM / ANSYS / SolidWorks / CFD / FEA / Heat Transfer'),('CODE','Python / TypeScript / JavaScript / React / Next.js / Java'),('TOOLS','Git / GitHub / VS Code / LangChain')]:
    text(d,28,y,title,27,RED,title=True);y=wrap(d,value,28,y+40,size=27)+28
save('method-board',im)

im,d=start(540,'06 / OPEN TO COLLABORATION',["LET'S BUILD",'SOMETHING USEFUL.'])
wrap(d,'Thermal engineering / CFD / engineering software / applied AI',28,232,size=30)
wrap(d,'Start with the problem, the inputs, and the outcome you want to reach.',28,382,size=25,color=MUTED)
save('contact-board',im)
print('Rendered compact stationary variants for all seven editorial panels.')
