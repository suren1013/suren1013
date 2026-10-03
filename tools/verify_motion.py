"""Check actual GIF frames for stationary reading areas and seamless sweep motion."""
from pathlib import Path
from PIL import Image,ImageSequence
import hashlib

ASSETS=Path(__file__).resolve().parents[1]/'assets'
for name in ('dossier','casting-evidence','clv-evidence','election-evidence','research-spotlight','method-board','contact-board'):
    image=Image.open(ASSETS/(name+'.gif'))
    hashes=set();durations=[];positions=[]
    for frame in ImageSequence.Iterator(image):
        rgb=frame.convert('RGB')
        hashes.add(hashlib.sha256(rgb.crop((0,0,image.width,image.height-45)).tobytes()).hexdigest())
        durations.append(frame.info.get('duration'))
        y=image.height-32
        pixels=[x for x in range(20,image.width-20) if rgb.getpixel((x,y))[0]>150 and rgb.getpixel((x,y))[0]>rgb.getpixel((x,y))[1]*1.5]
        if not pixels: raise AssertionError(name+': sweep not visible')
        positions.append(sum(pixels)/len(pixels))
    assert len(hashes)==1, name+': reading area changes between frames'
    # GIF encoders coalesce identical positions during a smooth turn-around.
    # Their combined hold must preserve the original 50ms sampling and 12s cycle.
    assert sum(durations)==12000 and all(d and d%50==0 for d in durations), name+': inconsistent frame cadence'
    steps=[abs(b-a) for a,b in zip(positions,positions[1:]+positions[:1])]
    assert max(steps)<=15, name+': abrupt sweep or loop jump'
    print(f'{name}: fixed reading area, 12s loop on a 50ms grid, max sweep step {max(steps):.1f}px')
